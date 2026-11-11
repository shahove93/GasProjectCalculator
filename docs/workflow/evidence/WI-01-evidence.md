# WI-01 evidence — packaged desktop app and native window (R2)

Status: implementer evidence only. This is **not** project PASS and not acceptance;
independent R2 Codex review follows.

## Baseline and working tree

- Repository: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/windows-installer`
- Baseline commit: `22133a13da0ccb70fc70b93c18529581ad7e43a1`
- Pre-existing uncommitted planning docs (approved, preserved, not edited by WI-01):
  `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, `ROADMAP.md`,
  `docs/workflow/APPROVALS.md`, `docs/workflow/HISTORY.md`,
  `docs/workflow/STATE.md`, plus untracked `docs/workflow/WINDOWS-INSTALLER-BRIEF.md`
  and `docs/workflow/tasks/`.
- WI-01 changes are listed in `logs/WI-01-status.txt` and
  `logs/WI-01-diff-stat.txt`; the tracked code diff is in
  `logs/WI-01-code-diff.txt` (only `.gitignore` and `app/main.py`).

## Environment

- Windows x64, Python 3.12.4 (`.venv/Scripts/python.exe`)
- WebView2 runtime 157.0.4341.42
- PyInstaller 6.22.3, pywebview 6.2.1, pythonnet 3.2.1, clr_loader 0.3.1
  (installed into the project venv only; pinned in `requirements-desktop.txt`)
- Existing user developer server on port 8000 (PID 12888, `0.0.0.0:8000`) was
  never bound by this work and was not stopped. All packaged runs selected
  `127.0.0.1:8001`.

## What changed

New files:

- `app/desktop_launcher.py` — loopback port selection, in-process uvicorn
  backend thread, bounded readiness probe, pywebview EdgeChromium window,
  backend shutdown, native error dialog, diagnostics flags.
- `app/resources.py` — resolves `frontend/index.html` from source or from the
  PyInstaller bundle (`sys._MEIPASS`).
- `desktop_app.py` — PyInstaller entry point.
- `packaging/GasProjectCalculator.spec` — PyInstaller onedir, `console=False`.
- `packaging/build.ps1` — reproducible build and SHA256 output.
- `packaging/README.md` — build/run/diagnostics usage.
- `requirements-desktop.txt` — pinned desktop dependencies.
- `tests/test_desktop_launcher.py` — 12 tests for launcher helpers (no GUI).
- `docs/workflow/evidence/WI-01-*` — this pack.

Modified:

- `app/main.py` — `GET /` now serves `FileResponse(str(frontend_index_path()))`.
  Endpoints, models, calculations and contracts are untouched.
- `.gitignore` — ignores `build/`, `dist/`, `*.spec.bak`.

Not edited: `AGENTS.md`, `ARCHITECTURE.md`, `VISION.md`, `ROADMAP.md`,
`docs/workflow/APPROVALS.md`, `docs/workflow/STATE.md`,
`docs/workflow/HISTORY.md`, `docs/workflow/MODEL-ROUTING.md`.
No commit, push, merge, deploy, signing or global config change was made.

## Design summary

- The backend is an in-process `uvicorn.Server` in a daemon thread; there is no
  child backend process to orphan.
- A listening socket is pre-bound on `127.0.0.1` before uvicorn starts. Ports
  are probed with a connect test (detects wildcard listeners such as the user's
  `0.0.0.0:8000` on Windows), then bound with `SO_EXCLUSIVEADDRUSE`. Candidate
  ports start at 8000 and skip busy ones; if all are busy, an ephemeral
  loopback port is used.
- The window is created only after `GET /` returns HTTP 200; readiness timeout
  is 30 s.
- Closing the window returns from `webview.start`; the launcher sets
  `should_exit`, joins the backend thread and closes the socket.
- Launch failures show a native `MessageBoxW` with an understandable Russian
  message and log path; the process exits 1. Diagnostics flags:
  `--port-file`, `--auto-close-seconds`, `--log-file`, `--preferred-port`,
  `--simulate-startup-failure`, `--no-error-dialog`.

## Acceptance checklist evidence

Artifact (final build):

- Path: `D:\Antigravity\GasProjectCalculator\dist\GasProjectCalculator\GasProjectCalculator.exe`
- SHA256: `36A21986EB9A55F1D5309C7AA3E22EDD7EE9F12418B4EC4C27D051B9F77177CC`
- Size: 6 831 548 bytes; onedir contains 102 files / 33 769 456 bytes total.
- File hashes of source/spec/test files: `logs/WI-01-file-hashes.txt`.

| ID | Result | Evidence |
| --- | --- | --- |
| W1 | PASS (build) | `packaging/build.ps1`, CWD `D:\Antigravity\GasProjectCalculator`, exit 0, PyInstaller 6.22.3, artifact above. Log: `logs/WI-01-build.txt`. |
| W2 | PASS | Launched exe with `PATH=C:\Windows\System32;C:\Windows` (`python` not found) and no console. PE subsystem = 2 (WINDOWS_GUI). Process `GasProjectCalculator`, native window title observed. Window screenshot: `WI-01-packaged-window.png`. Log: `logs/WI-01-packaged-run.txt`. |
| W3 | PASS | For packaged PID 18140: `Get-NetTCPConnection -State Listen -OwningProcess <pid>` showed only `127.0.0.1:8001`; no `0.0.0.0` listener. Evidence in `logs/WI-01-packaged-run.txt`. |
| W4 | PASS | User port `0.0.0.0:8000` (PID 12888) was occupied; packaged app selected `127.0.0.1:8001`. Evidence in `logs/WI-01-packaged-run.txt`. Unit test also covers a held wildcard listener. |
| W5 | PASS | Launcher log order: backend ready after 0.17–0.73 s (`GET /` readiness probe) → port file written → `Creating native window`. Evidence in `logs/WI-01-packaged-run.txt`, `logs/WI-01-visual-run.txt`. |
| W6 | PASS | Same bodies against packaged backend: GSN `subtotal=125000 vat=6250 total=131250`; GSV `subtotal=100500 vat=5025 total=105525`; combined `subtotal=139000 vat=6950 total=145950`. Baseline in-process results match exactly: `logs/WI-01-baseline-api.txt`; packaged run: `logs/WI-01-packaged-run.txt`. |
| W7 | PASS | Auto-close run: process exited 0, port 8001 no longer listening, no child processes. Manual `WM_CLOSE` run: exited 0, port released. Evidence: `logs/WI-01-packaged-run.txt`, `logs/WI-01-visual-run.txt`. |
| W8 | PASS | Simulated startup failure shows native dialog titled `GasProjectCalculator`; message text (from implementation) is: «Не удалось запустить GasProjectCalculator. Причина: Diagnostic startup failure requested with --simulate-startup-failure. Проверьте, что установлен компонент Microsoft Edge WebView2 Runtime и что антивирус не блокирует приложение, затем повторите запуск. Подробности записаны в журнал: …». Exit code 1, failed port-file status. Screenshot: `WI-01-launch-error.png`; logs: `logs/WI-01-error-run.txt`. |
| W9 | PASS | `.\.venv\Scripts\python.exe -m unittest discover -s tests` → `Ran 146 tests ... OK`, exit 0 (134 existing + 12 new launcher tests). Log: `logs/WI-01-unittest.txt`. Developer uvicorn path verified separately on `127.0.0.1:8010` (`GET /` 200, GSV total 63000, stopped afterwards): `logs/WI-01-dev-uvicorn.txt`. User server on 8000 remained PID 12888. |
| W10 | PASS | `logs/WI-01-code-diff.txt`: only `/` file-path resolution changed; no endpoint/model/calculation edits. Existing tests unmodified. |

## Raw logs and files

- `logs/WI-01-build.txt` — full PyInstaller build log
- `logs/WI-01-unittest.txt` — full suite
- `logs/WI-01-unit-launcher.txt` — focused launcher unit tests
- `logs/WI-01-packaged-run.txt` — packaged run, W2–W7 raw output
- `logs/WI-01-visual-run.txt` — window screenshot + manual close run
- `logs/WI-01-error-run.txt` — W8 failure path
- `logs/WI-01-dev-uvicorn.txt` — developer uvicorn regression
- `logs/WI-01-baseline-api.txt` — in-process baseline API results
- `logs/WI-01-status.txt`, `logs/WI-01-diff-stat.txt`, `logs/WI-01-code-diff.txt`
- `logs/WI-01-file-hashes.txt`
- `WI-01-packaged-window.png`, `WI-01-launch-error.png`

## Skips, limitations and risks

- Windows installer packaging/install/uninstall and shortcut creation are WI-02
  scope and were **not** run here.
- Code signing, updating, telemetry, push/merge/release were not performed.
- The build was verified on this Windows x64 machine only; a clean second
  machine was not available.
- PyInstaller printed benign warnings (`pycparser.lextab`, `pycparser.yacctab`,
  `tzdata` missing) and PowerShell surfaced native stderr as an error record;
  the build exited 0 and the artifact runs.
- The error screenshot shows the dialog partially overlapped by another
  foreground window in this desktop session; the exact dialog text and exit
  behavior are also captured in `logs/WI-01-error-run.txt`.
- A worker success assertion is not acceptance; independent routed review is
  required.
