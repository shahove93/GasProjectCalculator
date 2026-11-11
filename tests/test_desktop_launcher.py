import http.server
import json
import socket
import tempfile
import threading
import time
import unittest
from pathlib import Path

from app import desktop_launcher
from app.resources import frontend_index_path, splash_page_path


class PortSelectionTests(unittest.TestCase):
    def _hold(self, port: int = 0) -> tuple[socket.socket, int]:
        held = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        held.bind(("127.0.0.1", port))
        held.listen(1)
        return held, held.getsockname()[1]

    def test_selects_next_port_when_preferred_is_busy(self):
        held, busy_port = self._hold()
        self.addCleanup(held.close)

        sock, port = desktop_launcher.select_backend_socket(
            preferred_port=busy_port, scan_limit=10
        )
        self.addCleanup(sock.close)

        self.assertNotEqual(port, busy_port)
        self.assertEqual(sock.getsockname()[0], "127.0.0.1")
        self.assertGreater(port, busy_port)

    def test_selects_next_port_when_wildcard_listener_is_busy(self):
        held = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        held.bind(("0.0.0.0", 0))
        held.listen(1)
        self.addCleanup(held.close)
        busy_port = held.getsockname()[1]

        sock, port = desktop_launcher.select_backend_socket(
            preferred_port=busy_port, scan_limit=10
        )
        self.addCleanup(sock.close)

        self.assertNotEqual(port, busy_port)
        self.assertEqual(sock.getsockname()[0], "127.0.0.1")

    def test_selected_socket_is_bound_to_loopback_only(self):
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        probe.bind(("127.0.0.1", 0))
        free_port = probe.getsockname()[1]
        probe.close()

        sock, _ = desktop_launcher.select_backend_socket(
            preferred_port=free_port, scan_limit=10
        )
        self.addCleanup(sock.close)
        self.assertEqual(sock.getsockname()[0], "127.0.0.1")

    def test_invalid_preferred_port_is_rejected(self):
        with self.assertRaises(ValueError):
            desktop_launcher.select_backend_socket(preferred_port=0)
        with self.assertRaises(ValueError):
            desktop_launcher.select_backend_socket(preferred_port=70000)

    def test_is_port_available_reflects_held_port(self):
        held, busy_port = self._hold()
        self.addCleanup(held.close)
        self.assertFalse(desktop_launcher.is_port_available(busy_port))
        self.assertTrue(desktop_launcher.is_port_available(0))


class _OkHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - stdlib naming
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # silence test output
        pass


class ReadinessTests(unittest.TestCase):
    def test_waits_for_backend_until_ready(self):
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _OkHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)

        port = server.server_address[1]
        elapsed = desktop_launcher.wait_for_backend(
            desktop_launcher.backend_url(port), timeout=5.0, interval=0.05
        )
        self.assertGreaterEqual(elapsed, 0.0)

    def test_timeout_is_bounded_and_raises(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()  # port is now closed

        started = time.monotonic()
        with self.assertRaises(desktop_launcher.BackendReadinessError):
            desktop_launcher.wait_for_backend(
                desktop_launcher.backend_url(port), timeout=0.3, interval=0.05
            )
        self.assertLess(time.monotonic() - started, 5.0)


class DiagnosticsTests(unittest.TestCase):
    def test_port_file_is_written_atomically(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "port.json"
            desktop_launcher.write_port_file(path, 12345)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["port"], 12345)
            self.assertEqual(payload["host"], "127.0.0.1")
            self.assertEqual(payload["status"], "ready")
            self.assertFalse(path.with_name(path.name + ".tmp").exists())

    def test_failure_port_file_has_status_and_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "port.json"
            desktop_launcher.write_port_file(
                path, 0, status="failed", error="boom"
            )
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "failed")
            self.assertEqual(payload["error"], "boom")

    def test_error_message_is_understandable(self):
        message = desktop_launcher.build_launch_error_message(
            RuntimeError("WebView2 runtime missing"), Path("desktop.log")
        )
        self.assertIn("WebView2", message)
        self.assertIn("WebView2 runtime missing", message)
        self.assertIn("desktop.log", message)
        self.assertNotIn("Traceback", message)

    def test_error_message_uses_brand(self):
        message = desktop_launcher.build_launch_error_message(
            RuntimeError("boom"), Path("desktop.log")
        )
        self.assertIn("СС.Расчет", message)
        self.assertIn("Причина: boom", message)

    def test_stop_backend_requests_exit_and_joins(self):
        class FakeServer:
            should_exit = False
            force_exit = False

        class FakeThread:
            def __init__(self):
                self.joined = False
                self._alive = True

            def join(self, timeout=None):
                self.joined = True
                self._alive = False

            def is_alive(self):
                return self._alive

        server = FakeServer()
        thread = FakeThread()
        self.assertTrue(desktop_launcher.stop_backend(server, thread, timeout=0.1))
        self.assertTrue(server.should_exit)
        self.assertTrue(thread.joined)


class ResourceTests(unittest.TestCase):
    def test_frontend_index_resolves_from_source(self):
        path = frontend_index_path()
        self.assertTrue(path.is_file(), path)
        self.assertEqual(path.name, "index.html")

    def test_splash_page_resolves_from_source(self):
        path = splash_page_path()
        self.assertTrue(path.is_file(), path)
        self.assertEqual(path.name, "splash.html")


class BrandingGeometryTests(unittest.TestCase):
    def test_app_title_is_exact_brand(self):
        self.assertEqual(desktop_launcher.APP_TITLE, "СС.Расчет")

    def test_window_geometry_matches_approved_design(self):
        self.assertEqual(desktop_launcher.APP_WIDTH, 1050)
        self.assertEqual(desktop_launcher.APP_HEIGHT, 740)
        self.assertEqual(desktop_launcher.APP_MIN_SIZE, (860, 620))


class SplashTests(unittest.TestCase):
    def setUp(self):
        self.path = splash_page_path()
        self.html = self.path.read_text(encoding="utf-8")

    def test_splash_is_russian_local_page(self):
        self.assertIn('lang="ru"', self.html)
        self.assertIn("СС.Расчет", self.html)
        self.assertIn("Запуск приложения", self.html)

    def test_splash_has_no_network_references(self):
        for marker in ("http://", "https://", "//cdn", "@import", "fonts."):
            self.assertNotIn(marker, self.html)

    def test_splash_emblem_is_a_local_file(self):
        self.assertIn('src="assets/company-emblem.png"', self.html)
        asset = self.path.parent / "assets" / "company-emblem.png"
        self.assertTrue(asset.is_file(), asset)

    def test_splash_respects_reduced_motion(self):
        self.assertIn("prefers-reduced-motion: reduce", self.html)
        self.assertIn("animation: none", self.html)
        self.assertIn('data-reduced-motion="true"', self.html)

    def test_splash_animates_gas_flow_to_house(self):
        self.assertIn("@keyframes gas-flow", self.html)
        self.assertIn("class=\"gas", self.html)
        self.assertIn("class=\"house\"", self.html)

    def test_splash_url_is_local_file_uri(self):
        uri = desktop_launcher.splash_url()
        self.assertTrue(uri.startswith("file://"), uri)
        self.assertTrue(uri.endswith("splash.html"), uri)

    def test_splash_url_diagnostic_reduced_motion_flag(self):
        uri = desktop_launcher.splash_url(reduced_motion=True)
        self.assertTrue(uri.endswith("splash.html?reduced-motion=1"), uri)


if __name__ == "__main__":
    unittest.main()
