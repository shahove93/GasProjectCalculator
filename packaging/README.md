# Desktop packaging (WI-01)

Pinned runtime/build dependencies for the packaged Windows desktop app:

```
pyinstaller==6.22.3
pywebview==6.2.1
pythonnet==3.2.1
clr_loader==0.3.1
```

Install into the project venv only:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-desktop.txt
```

Build the onedir application (PyInstaller, windowed, x64):

```powershell
powershell -ExecutionPolicy Bypass -File packaging\build.ps1
```

Result: `dist\GasProjectCalculator\GasProjectCalculator.exe` plus its `_internal`
directory. Run the exe directly; no Python installation is required.

The launcher binds the FastAPI backend to `127.0.0.1` only, skips busy ports
starting from 8000, waits for `GET /` readiness, then opens the pywebview
EdgeChromium window. Closing the window stops the in-process backend.

Diagnostics flags (do not change normal behavior):

| Flag | Purpose |
| --- | --- |
| `--port-file PATH` | write JSON `{status,host,port,url,pid}` once ready |
| `--auto-close-seconds N` | close the window automatically after N seconds |
| `--log-file PATH` | override the desktop log path |
| `--preferred-port N` | first candidate port (default 8000) |
| `--simulate-startup-failure` | exercise the startup error path |
| `--no-error-dialog` | suppress the native message box (automation) |

Default log: `%LOCALAPPDATA%\GasProjectCalculator\logs\desktop.log`.
