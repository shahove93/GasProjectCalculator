"""Launch the FastAPI backend and native pywebview window.

Design notes
------------
* The backend is an in-process ``uvicorn.Server`` running in a daemon thread,
  so no child process can be orphaned when the window closes.
* A bound listening socket on ``127.0.0.1`` is created *before* uvicorn starts.
  This both selects a free port and removes the bind race; the port is never
  exposed on a non-loopback interface.
* A small local splash window is shown while the backend starts.  It is loaded
  from ``frontend/splash.html`` through a ``file://`` URI, has no network
  dependencies and never adds an artificial delay: it closes as soon as
  ``GET /`` answers with HTTP 200.
* The main window is created hidden after readiness, then the splash is closed
  and the main window is shown, so the application window only appears once the
  backend is ready.
* Closing the main window returns from ``webview.start``, after which the
  backend is asked to stop and the thread is joined.

Diagnostics hooks (used by automated evidence, no effect on normal use):

    --port-file PATH             write JSON with the chosen host/port once ready
    --auto-close-seconds SECONDS close the main window automatically
    --log-file PATH              override the rotating log destination
    --preferred-port PORT        first candidate port (default 8000)
    --simulate-startup-failure   raise after the splash is shown to exercise the
                                 failure path
    --no-error-dialog            suppress the native message box (automation only)
    --splash-hold-seconds N      hold the visible splash for N s after readiness
                                 (screenshot evidence only)
    --force-reduced-motion       load the splash with reduced-motion styling
                                 (screenshot evidence only)
    --eval-bridge PATH           diagnostic: watch a JSON command file and
                                 evaluate its ``script`` in the real native
                                 window, writing ``PATH.result.json``.  Used by
                                 RD-05 browser-evidence automation only.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import socket
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path
from typing import Sequence

HOST = "127.0.0.1"
DEFAULT_PREFERRED_PORT = 8000
PORT_SCAN_LIMIT = 50
READY_TIMEOUT_SECONDS = 30.0
READY_POLL_INTERVAL_SECONDS = 0.1

# Branding / native window geometry (logical pixels).
APP_TITLE = "СС.Расчет"
APP_WIDTH = 800
APP_HEIGHT = 540
APP_MIN_SIZE = (760, 520)

# Local startup splash window.
SPLASH_WIDTH = 560
SPLASH_HEIGHT = 450
SPLASH_BACKGROUND = "#081e2b"

logger = logging.getLogger("gasproject.desktop")


class BackendReadinessError(RuntimeError):
    """Raised when the local backend does not answer within the timeout."""


# ---------------------------------------------------------------------------
# Port selection / socket helpers (unit-testable without a GUI)
# ---------------------------------------------------------------------------


def _loopback_port_in_use(port: int, host: str = HOST, timeout: float = 0.25) -> bool:
    """Return True when something already accepts connections on ``host:port``.

    A plain ``bind`` is not enough on Windows: if another process bound the
    wildcard address (``0.0.0.0:8000``) first, a later bind to
    ``127.0.0.1:8000`` can still succeed.  An active connect probe detects the
    existing listener and lets us skip that port.
    """

    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.settimeout(timeout)
    try:
        result = probe.connect_ex((host, int(port)))
    except OSError:
        return True
    finally:
        probe.close()
    # 0 == connected (busy); WSAETIMEDOUT/ETIMEDOUT == listener did not answer
    # in time but is present, so treat it as busy too.
    return result in (0, getattr(socket, "WSAETIMEDOUT", 10060))


def bind_local_socket(port: int, host: str = HOST) -> socket.socket | None:
    """Bind a listening-capable TCP socket to ``host:port``.

    Returns ``None`` when the port is unavailable.  No ``SO_REUSEADDR`` is
    used: on Windows it would allow binding a port another process already
    owns and defeat conflict detection.  ``SO_EXCLUSIVEADDRUSE`` keeps other
    processes from sharing the chosen port afterwards.
    """

    port = int(port)
    if port != 0 and _loopback_port_in_use(port, host):
        return None

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", None)
    if exclusive is not None:
        try:
            sock.setsockopt(socket.SOL_SOCKET, exclusive, 1)
        except OSError:  # pragma: no cover - older Windows / unsupported
            pass
    try:
        sock.bind((host, port))
    except OSError:
        sock.close()
        return None
    return sock


def is_port_available(port: int, host: str = HOST) -> bool:
    sock = bind_local_socket(port, host)
    if sock is None:
        return False
    sock.close()
    return True


def select_backend_socket(
    preferred_port: int = DEFAULT_PREFERRED_PORT,
    host: str = HOST,
    scan_limit: int = PORT_SCAN_LIMIT,
) -> tuple[socket.socket, int]:
    """Return a bound loopback socket and its port.

    Tries ``preferred_port`` onward so a busy developer server (or any other
    application) is skipped safely.  If the whole scan range is busy an
    ephemeral port is requested from the OS.
    """

    if not 1 <= int(preferred_port) <= 65535:
        raise ValueError(f"preferred_port must be in 1..65535, got {preferred_port!r}")
    if not 1 <= int(scan_limit) <= 65535:
        raise ValueError(f"scan_limit must be in 1..65535, got {scan_limit!r}")

    start = int(preferred_port)
    stop = min(start + int(scan_limit), 65536)
    for port in range(start, stop):
        sock = bind_local_socket(port, host)
        if sock is not None:
            return sock, port

    sock = bind_local_socket(0, host)
    if sock is None:  # pragma: no cover - would mean the OS cannot bind at all
        raise OSError("No free TCP port could be bound on 127.0.0.1")
    return sock, int(sock.getsockname()[1])


def backend_url(port: int, host: str = HOST) -> str:
    return f"http://{host}:{int(port)}/"


# ---------------------------------------------------------------------------
# Readiness probe
# ---------------------------------------------------------------------------


def wait_for_backend(
    url: str,
    timeout: float = READY_TIMEOUT_SECONDS,
    interval: float = READY_POLL_INTERVAL_SECONDS,
) -> float:
    """Poll ``url`` until it answers 2xx, returning elapsed seconds.

    Raises :class:`BackendReadinessError` after a bounded wait; the window is
    never created in that case.
    """

    started = time.monotonic()
    deadline = started + max(0.0, float(timeout))
    last_error: Exception | None = None

    while True:
        try:
            with urllib.request.urlopen(url, timeout=max(0.5, interval)) as response:
                response.read(1)
                if 200 <= int(response.status) < 300:
                    return time.monotonic() - started
        except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as exc:
            last_error = exc

        if time.monotonic() >= deadline:
            raise BackendReadinessError(
                f"Backend did not become ready at {url} within {timeout:.1f}s. "
                f"Last error: {last_error}"
            ) from last_error
        time.sleep(interval)


# ---------------------------------------------------------------------------
# Backend lifecycle
# ---------------------------------------------------------------------------


def start_backend(app, sock: socket.socket, port: int, host: str = HOST):
    """Start uvicorn on the pre-bound ``sock`` and wait for readiness.

    Returns ``(server, thread, elapsed_seconds)``.
    """

    import uvicorn

    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        log_config=None,
        access_log=False,
        lifespan="on",
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(
        target=server.run,
        kwargs={"sockets": [sock]},
        name="gasproject-backend",
        daemon=True,
    )
    thread.start()
    elapsed = wait_for_backend(backend_url(port, host))
    logger.info(
        "Backend ready at %s after %.2fs (thread=%s pid=%s)",
        backend_url(port, host),
        elapsed,
        thread.name,
        os.getpid(),
    )
    return server, thread, elapsed


def stop_backend(server, thread, timeout: float = 10.0) -> bool:
    """Ask the in-process uvicorn server to stop and join its thread."""

    if server is not None:
        server.should_exit = True
    if thread is not None:
        thread.join(timeout)
        if thread.is_alive() and server is not None:
            server.force_exit = True
            thread.join(5.0)
    alive = bool(thread is not None and thread.is_alive())
    if alive:
        logger.error("Backend thread did not stop within %.1fs", timeout)
    else:
        logger.info("Backend stopped; no listener remains")
    return not alive


# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------


def splash_url(reduced_motion: bool = False) -> str:
    """Return the local ``file://`` URI of the splash page.

    The splash is a plain local file.  No HTTP server is involved, so the
    startup screen cannot depend on the network.  ``reduced_motion`` appends a
    diagnostic query flag that the page honours for screenshot evidence; normal
    launches rely on the OS ``prefers-reduced-motion`` media query.
    """

    from app.resources import splash_page_path

    uri = splash_page_path().as_uri()
    if reduced_motion:
        uri += "?reduced-motion=1"
    return uri


def create_main_window(url: str, hidden: bool = False):
    """Create the branded native application window."""

    import webview

    return webview.create_window(
        APP_TITLE,
        url=url,
        width=APP_WIDTH,
        height=APP_HEIGHT,
        min_size=APP_MIN_SIZE,
        hidden=hidden,
    )


def create_splash_window(reduced_motion: bool = False):
    """Create the frameless local startup splash window."""

    import webview

    return webview.create_window(
        APP_TITLE,
        url=splash_url(reduced_motion=reduced_motion),
        width=SPLASH_WIDTH,
        height=SPLASH_HEIGHT,
        min_size=(SPLASH_WIDTH, SPLASH_HEIGHT),
        frameless=True,
        easy_drag=False,
        resizable=False,
        on_top=True,
        background_color=SPLASH_BACKGROUND,
    )


def _start_auto_close(window, auto_close_seconds: float | None) -> None:
    """Diagnostic: destroy ``window`` after N seconds, without blocking exit."""

    if not auto_close_seconds or auto_close_seconds <= 0:
        return

    def _auto_close() -> None:
        logger.info("Auto-close: waiting %.2fs before closing window", auto_close_seconds)
        time.sleep(float(auto_close_seconds))
        try:
            logger.info("Auto-close: destroying window")
            window.destroy()
        except Exception:  # pragma: no cover - window may already be gone
            logger.exception("Auto-close could not destroy the window")

    threading.Thread(target=_auto_close, name="gasproject-auto-close", daemon=True).start()


def _start_eval_bridge(window, command_path: Path) -> None:
    """Diagnostic: evaluate scripts from a local JSON command file.

    The command file holds ``{"id": <n>, "script": "<js>"}``.  When ``id``
    changes, the script runs in the real native WebView2 window and the result
    is written next to the command file as ``<name>.result.json``.  This is an
    inert local evidence hook: it does nothing unless ``--eval-bridge`` is
    passed, and it never adds network access or changes product behaviour.
    """

    command_path = Path(command_path)
    result_path = command_path.with_name(command_path.name + ".result.json")
    stop = threading.Event()
    last_id: object = None

    window.events.closed += lambda: stop.set()

    def _loop() -> None:
        nonlocal last_id
        if not window.events.loaded.wait(20):
            logger.error("[eval-bridge] window did not load; bridge inactive")
            return
        logger.info("[eval-bridge] active at %s", command_path)
        while not stop.is_set():
            try:
                if command_path.is_file():
                    data = json.loads(command_path.read_text(encoding="utf-8"))
                    command_id = data.get("id")
                    script = data.get("script")
                    if command_id != last_id and isinstance(script, str):
                        last_id = command_id
                        try:
                            result = window.evaluate_js(script)
                            payload = {"id": command_id, "ok": True, "result": result}
                        except Exception as exc:  # noqa: BLE001 - diagnostic boundary
                            payload = {"id": command_id, "ok": False, "error": repr(exc)}
                        result_path.write_text(
                            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
                        )
                        logger.info(
                            "[eval-bridge] id=%s ok=%s", command_id, payload["ok"]
                        )
            except (OSError, ValueError):
                logger.exception("[eval-bridge] command read failed")
            time.sleep(0.05)
        logger.info("[eval-bridge] stopped")

    threading.Thread(
        target=_loop, name="gasproject-eval-bridge", daemon=True
    ).start()


# ---------------------------------------------------------------------------
# Diagnostics / error presentation
# ---------------------------------------------------------------------------


def default_log_path() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home())
    return Path(base) / "GasProjectCalculator" / "logs" / "desktop.log"


def configure_logging(log_path: Path) -> logging.Handler:
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    )
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    if sys.stderr is not None:
        stream = logging.StreamHandler(sys.stderr)
        stream.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        root.addHandler(stream)
    return handler


def _ensure_standard_streams() -> None:
    # Windowed (console=False) builds have sys.stdout/stderr set to None.
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")


def write_port_file(
    path: Path,
    port: int,
    host: str = HOST,
    status: str = "ready",
    error: str | None = None,
) -> None:
    """Atomically write a small JSON status file for automation."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": status,
        "host": host,
        "port": int(port),
        "url": backend_url(port, host),
        "pid": os.getpid(),
    }
    if error:
        payload["error"] = error
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


def build_launch_error_message(exc: BaseException, log_path: Path | str) -> str:
    detail = str(exc).strip() or exc.__class__.__name__
    return (
        "Не удалось запустить СС.Расчет.\n\n"
        f"Причина: {detail}\n\n"
        "Проверьте, что установлен компонент Microsoft Edge WebView2 Runtime "
        "и что антивирус не блокирует приложение, затем повторите запуск.\n\n"
        f"Подробности записаны в журнал:\n{log_path}"
    )


def show_native_error(message: str, title: str = APP_TITLE) -> None:
    """Show a native error message box; never lets the UI path crash."""

    logger.error("Launch failure dialog: %s", message.replace("\n", " | "))
    try:
        import ctypes

        # MB_OK | MB_ICONERROR | MB_SETFOREGROUND | MB_TOPMOST
        ctypes.windll.user32.MessageBoxW(
            None, message, title, 0x00000010 | 0x00010000 | 0x00040000
        )
    except Exception:  # pragma: no cover - only on non-Windows / API failure
        logger.exception("Could not display the native error dialog")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


class _LaunchState:
    """Mutable state shared between the GUI loop and the startup worker."""

    def __init__(self) -> None:
        self.error: BaseException | None = None
        self.server = None
        self.thread = None
        self.sock: socket.socket | None = None
        self.port: int | None = None


def _run_startup(
    state: _LaunchState,
    splash,
    preferred_port: int,
    port_file: Path | None,
    auto_close_seconds: float | None,
    log_path: Path,
    simulate_startup_failure: bool,
    show_error_dialog: bool,
    splash_hold_seconds: float | None,
    eval_bridge: Path | None,
) -> None:
    """Start the backend while the splash is visible, then reveal the window.

    Runs in the non-daemon thread created by ``webview.start(func=...)`` so the
    GUI loop stays responsive and the splash can paint.  Every failure is
    handled here: the splash is closed, a Russian error is shown and the
    backend is stopped by the caller's ``finally`` block.
    """

    try:
        # Never start the backend before the splash has actually been shown:
        # the evidence order is splash visible -> backend starting -> ready.
        if not splash.events.shown.wait(10):
            raise RuntimeError("Окно заставки не появилось в течение 10 секунд.")
        logger.info("[splash] splash window shown; starting backend")

        if simulate_startup_failure:
            raise RuntimeError(
                "Диагностический сбой запуска (--simulate-startup-failure)."
            )

        # Imported lazily so helper tests do not need FastAPI.
        from app.main import app
        from app.resources import frontend_index_path

        logger.info("Frontend resource: %s", frontend_index_path())
        sock, chosen_port = select_backend_socket(preferred_port)
        state.sock, state.port = sock, chosen_port
        logger.info(
            "Selected loopback port %s (preferred %s); socket bound on %s",
            chosen_port,
            preferred_port,
            HOST,
        )

        server, thread, elapsed = start_backend(app, sock, chosen_port)
        state.server, state.thread = server, thread
        if port_file:
            write_port_file(port_file, chosen_port)
            logger.info("Wrote port file: %s", port_file)

        logger.info(
            "[splash] backend ready after %.2fs; preparing main window", elapsed
        )

        import webview

        # Create the window hidden, close the splash, then reveal the window:
        # the application window becomes visible only after readiness.
        window = create_main_window(backend_url(chosen_port), hidden=True)
        logger.info(
            "[window] main window created: title=%r width=%s height=%s min_size=%s",
            APP_TITLE,
            APP_WIDTH,
            APP_HEIGHT,
            APP_MIN_SIZE,
        )

        if splash_hold_seconds and splash_hold_seconds > 0:
            logger.info(
                "[splash] diagnostic hold %.2fs before closing the splash",
                splash_hold_seconds,
            )
            time.sleep(float(splash_hold_seconds))

        splash.destroy()
        splash.events.closed.wait(5.0)
        logger.info("[splash] splash closed after backend readiness")

        window.show()
        logger.info("[window] main window shown after backend readiness")
        window.events.closed += lambda: logger.info("[window] main window closed")
        _start_auto_close(window, auto_close_seconds)
        if eval_bridge:
            _start_eval_bridge(window, eval_bridge)
            logger.info("[eval-bridge] watching %s", eval_bridge)
    except BaseException as exc:  # noqa: BLE001 - worker boundary
        state.error = exc
        logger.error("[startup] launch failed: %s", exc)
        logger.debug("%s", traceback.format_exc())
        if port_file:
            try:
                write_port_file(
                    port_file,
                    state.port or 0,
                    status="failed",
                    error=str(exc),
                )
            except OSError:
                logger.exception("Could not write failure port file")

        # Splash lifecycle on failure: close it before presenting the error.
        try:
            # Let the local splash finish loading so closing it does not abort
            # WebView2 initialization (bounded; does not affect normal use).
            splash.events.loaded.wait(3.0)
            splash.destroy()
            splash.events.closed.wait(5.0)
            logger.info("[splash] splash closed after startup failure")
        except Exception:  # pragma: no cover - splash may already be gone
            logger.exception("Could not close the splash window")

        message = build_launch_error_message(exc, log_path)
        logger.error(
            "Launch failure message: %s", message.replace("\n", " | ")
        )
        if show_error_dialog:
            show_native_error(message)


def launch(
    preferred_port: int = DEFAULT_PREFERRED_PORT,
    port_file: Path | None = None,
    auto_close_seconds: float | None = None,
    log_path: Path | str | None = None,
    simulate_startup_failure: bool = False,
    show_error_dialog: bool = True,
    splash_hold_seconds: float | None = None,
    force_reduced_motion: bool = False,
    eval_bridge: Path | None = None,
) -> int:
    """Run the full desktop lifecycle and return a process exit code."""

    log_path = Path(log_path) if log_path else default_log_path()
    state = _LaunchState()

    try:
        import webview

        from app.resources import splash_page_path

        logger.info("Splash resource: %s", splash_page_path())
        splash = create_splash_window(reduced_motion=force_reduced_motion)
        logger.info(
            "[splash] splash window created: %sx%s uri=%s reduced_motion=%s",
            SPLASH_WIDTH,
            SPLASH_HEIGHT,
            splash_url(reduced_motion=force_reduced_motion),
            force_reduced_motion,
        )
        splash.events.shown += lambda: logger.info("[splash] splash window shown event")

        webview.start(
            func=_run_startup,
            args=(
                state,
                splash,
                preferred_port,
                port_file,
                auto_close_seconds,
                log_path,
                simulate_startup_failure,
                show_error_dialog,
                splash_hold_seconds,
                eval_bridge,
            ),
            gui="edgechromium",
        )
        logger.info("Window closed by user")
        return 0 if state.error is None else 1
    except BaseException as exc:  # noqa: BLE001 - top-level launcher boundary
        logger.error("Launch failed: %s", exc)
        logger.debug("%s", traceback.format_exc())
        if port_file:
            try:
                write_port_file(
                    port_file,
                    state.port or 0,
                    status="failed",
                    error=str(exc),
                )
            except OSError:
                logger.exception("Could not write failure port file")
        message = build_launch_error_message(exc, log_path)
        logger.error("Launch failure message: %s", message.replace("\n", " | "))
        if show_error_dialog:
            show_native_error(message)
        return 1
    finally:
        stop_backend(state.server, state.thread)
        if state.sock is not None:
            try:
                state.sock.close()
            except OSError:
                pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="GasProjectCalculator",
        description="GasProjectCalculator desktop application",
    )
    parser.add_argument(
        "--preferred-port",
        type=int,
        default=DEFAULT_PREFERRED_PORT,
        help="first candidate loopback port (default: 8000)",
    )
    parser.add_argument(
        "--port-file",
        type=Path,
        default=None,
        help="diagnostic: write chosen host/port JSON once the backend is ready",
    )
    parser.add_argument(
        "--auto-close-seconds",
        type=float,
        default=None,
        help="diagnostic: close the window automatically after N seconds",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="diagnostic: override the desktop log path",
    )
    parser.add_argument(
        "--simulate-startup-failure",
        action="store_true",
        help="diagnostic: exercise the startup error path",
    )
    parser.add_argument(
        "--no-error-dialog",
        action="store_true",
        help="diagnostic: do not show the native error dialog",
    )
    parser.add_argument(
        "--splash-hold-seconds",
        type=float,
        default=None,
        help="diagnostic: keep the splash visible N seconds after readiness",
    )
    parser.add_argument(
        "--force-reduced-motion",
        action="store_true",
        help="diagnostic: load the splash with reduced-motion styling",
    )
    parser.add_argument(
        "--eval-bridge",
        type=Path,
        default=None,
        help="diagnostic: evaluate scripts from a local JSON command file",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    _ensure_standard_streams()
    args = build_parser().parse_args(argv)
    log_path = args.log_file if args.log_file else default_log_path()
    configure_logging(log_path)
    logger.info("=== GasProjectCalculator desktop launcher starting (pid=%s) ===", os.getpid())
    try:
        exit_code = launch(
            preferred_port=args.preferred_port,
            port_file=args.port_file,
            auto_close_seconds=args.auto_close_seconds,
            log_path=log_path,
            simulate_startup_failure=args.simulate_startup_failure,
            show_error_dialog=not args.no_error_dialog,
            splash_hold_seconds=args.splash_hold_seconds,
            force_reduced_motion=args.force_reduced_motion,
            eval_bridge=args.eval_bridge,
        )
    except BaseException:  # pragma: no cover - defensive top-level boundary
        logger.exception("Unhandled launcher error")
        return 1
    logger.info("=== GasProjectCalculator desktop launcher exiting with code %s ===", exit_code)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
