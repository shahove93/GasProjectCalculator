# WI-02 evidence — Inno Setup installer, shortcuts, clean install/uninstall (R2)

Status: implementer evidence only. This is **not** project PASS and not acceptance;
independent risk-routed review follows. No commit, push, merge, deploy, signing or
release was performed.

## Baseline and working tree

- Repository: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/windows-installer`
- Baseline commit: `7fab960` (`feat(desktop): package app with native window and loopback backend (WI-01)`)
- Pre-existing uncommitted planning/workflow changes were preserved and not edited
  by WI-02: `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, `ROADMAP.md`,
  `docs/workflow/APPROVALS.md`, `docs/workflow/HISTORY.md`,
  `docs/workflow/STATE.md`, `docs/workflow/tasks/WI-02.md`, untracked
  `docs/workflow/WINDOWS-INSTALLER-BRIEF.md`.
- WI-02 tracked change: `.gitignore` only (installer output ignore). New untracked
  paths: `installer/` and `docs/workflow/evidence/WI-02-*`.
- No application source, API, calculator, frontend, test or planning file was changed.
  `git status` / `git diff --stat`: `logs/WI-02-status.txt`.

## Environment and toolchain

- Windows x64, Windows PowerShell 5.1, Python 3.12.4 (`.venv/Scripts/python.exe`).
- Packaged onedir reused from WI-01 (not rebuilt):
  `dist\GasProjectCalculator\GasProjectCalculator.exe`,
  SHA256 `36A21986EB9A55F1D5309C7AA3E22EDD7EE9F12418B4EC4C27D051B9F77177CC`.
- Task-specified compiler
  `C:\Users\user\AppData\Local\Temp\edr-windows-build\inno\ISCC.exe` is
  **incomplete**: it exists but its directory has no `ISCmplr.dll` and an empty
  `Languages\` folder, so compiling fails with
  `Could not load ISCmplr.dll` (exit 1).
- Working compiler (verified, no installation, no global config/account change):
  `C:\Users\user\AppData\Local\Programs\Antigravity IDE\resources\app\node_modules\innosetup\bin\ISCC.exe`
  — full Inno Setup 6.4.1 distribution with `ISCmplr.dll`. The build script
  validates that `ISCmplr.dll` sits next to a candidate and falls back to this
  location. Toolchain check: `logs/WI-02-toolchain.txt`.

## What changed

New `installer/` (allowed scope):

- `installer/GasProjectCalculator.iss` — per-user, lowest-privilege, x64-only
  Inno Setup script. Installs the complete PyInstaller onedir tree to
  `{localappdata}\Programs\GasProjectCalculator`; always creates the Start Menu
  shortcut; optional unchecked Desktop shortcut task; optional post-install launch;
  no `[UninstallDelete]` entries and no writes to `{app}` for user data.
- `installer/build-installer.ps1` — reproducible build, compiler resolution via
  `-IsccPath` / `$env:ISCC_PATH` / validated fallbacks, artifact SHA256.
- `installer/verify-install.ps1` — silent install, installed-file list, shortcut
  target/args verification, expected optional-Desktop behavior.
- `installer/verify-runtime.ps1` — Python-free PATH launch, PE subsystem, occupied
  port, loopback-only listener, readiness/window order, three modes, close/shutdown,
  native launch-failure dialog.
- `installer/verify-uninstall.ps1` — silent uninstall, program/shortcut removal,
  user marker preservation.

Modified:

- `.gitignore` — added `installer/Output/` and `installer/*.log`.

Not edited: application code, tests, `VISION.md`, `ARCHITECTURE.md`, `ROADMAP.md`,
`AGENTS.md`, `docs/workflow/*` planning/status documents. No commit.

## Installer artifact (I1)

- Exact build command (CWD `D:\Antigravity\GasProjectCalculator`):
  `powershell -NoProfile -ExecutionPolicy Bypass -File installer\build-installer.ps1`
- Exit code: `0`.
- Compiler: Inno Setup 6.4.1; full build log: `logs/WI-02-build.txt`.
- Artifact:
  `D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe`
- Size: `15 256 037` bytes.
- **SHA256: `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`**
- Note: `installer/Output/` is git-ignored; this is a local artifact for hand-off,
  not published or committed.

## Frozen acceptance checklist evidence

| ID | Result | Evidence |
| --- | --- | --- |
| I1 | PASS (implementer) | Build command above, exit 0, Inno Setup 6.4.1, log `logs/WI-02-build.txt`; artifact path/size/SHA256 above; `logs/WI-02-installer-info.txt`. |
| I2 | PASS | `logs/WI-02-install-a.txt`: `GasProjectCalculator-Setup-1.0.0.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /LOG=... /TASKS="desktopicon"`, exit code 0; 104 installed files, 37 343 956 bytes; installed exe SHA256 matches WI-01. Inno log confirms `Administrative install mode: No`, `HKCU` (`logs/WI-02-inno-install-a.txt`). |
| I3 | PASS | Start Menu shortcut always present: `C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\GasProjectCalculator.lnk`; target `...\Local\Programs\GasProjectCalculator\GasProjectCalculator.exe`; arguments empty; working dir the install dir. Both installs A and B: `logs/WI-02-install-a.txt`, `logs/WI-02-install-b.txt`. |
| I4 | PASS | With `/TASKS="desktopicon"`: `C:\Users\user\Desktop\GasProjectCalculator.lnk` exists with the same target (`logs/WI-02-install-a.txt`). Without the task (`/VERYSILENT`, no `/TASKS`): shortcut absent while the Start Menu shortcut exists (`logs/WI-02-install-b.txt`). Task is unchecked by default in the `.iss`. |
| I5 | PASS | Installed exe launched with `PATH=C:\Windows\System32;C:\Windows`; `python` not found; PE subsystem `2 WINDOWS_GUI (no console)`; application launched and answered HTTP. `logs/WI-02-runtime-a.txt`. |
| I6 | PASS | Port file `status=ready` written 2026-11-11T19:05:53.641; native window `MainWindowTitle: GasProjectCalculator — расчёт стоимости проекта` observed 19:05:54.275 (after readiness). Launcher log order: `Backend ready ... 0.75s` → `Wrote port file` → `Creating native window`. `logs/WI-02-runtime-a.txt`. |
| I7 | PASS | Against installed backend on `http://127.0.0.1:8124`: GSN `subtotal=125000 vat=6250.0 total=131250.0`; GSV `subtotal=100500 vat=5025 total=105525`; combined `subtotal=139000 vat=6950 total=145950` (raw responses and request bodies in `logs/WI-02-runtime-a.txt`). Values match WI-01 baseline. |
| I8 | PASS | Test listener held on `127.0.0.1:8123`; application skipped it and used `8124`. `Get-NetTCPConnection -State Listen -OwningProcess <pid>` showed only `127.0.0.1 8124`; no `0.0.0.0` listener. `logs/WI-02-runtime-a.txt`. |
| I9 | PASS | Auto-close test hook destroyed the window at 40 s; process exited `0`, no process remained, no listener on port 8124, no child processes. Log: `Auto-close: destroying window` → `Window closed by user` → `Backend stopped; no listener remains`. `logs/WI-02-runtime-a.txt`. |
| I10 | PASS | Installed exe run with `--simulate-startup-failure`: native dialog observed (`#32770`, title `GasProjectCalculator`), closed via `WM_CLOSE`; process exit code `1`; port file `status=failed`; log records exact message: «Не удалось запустить GasProjectCalculator. … Причина: Diagnostic startup failure requested with --simulate-startup-failure. … Подробности записаны в журнал: …». `logs/WI-02-runtime-a.txt`. |
| I11 | PASS | Three user markers created before install outside `{app}` (Documents, Desktop, `%LOCALAPPDATA%\GasProjectCalculator`; `logs/WI-02-markers.txt`). After silent uninstall: installed exe/dir removed, Start Menu and Desktop shortcuts removed, all three markers still present, user data directory preserved. Both cycles: `logs/WI-02-uninstall-a.txt`, `logs/WI-02-uninstall-b.txt`; Inno uninstall logs `logs/WI-02-inno-uninstall-a.txt`, `logs/WI-02-inno-uninstall-b.txt`. |
| I12 | PASS | `.\.venv\Scripts\python.exe -m unittest discover -s tests` → `Ran 146 tests ... OK`, exit 0 (`logs/WI-02-unittest.txt`). 146 = 134 pre-WI-01 tests + 12 WI-01 launcher tests; the TASK's "134 OK" predates WI-01's added tests. Only `.gitignore` changed in tracked code; no app/API/contract changes. Developer uvicorn path untouched (WI-01 evidence reused). |

## Install / uninstall summary

- Install A (Desktop task): exit 0, 104 files, Start Menu + Desktop shortcuts.
- Runtime tests A: I5–I10 all passed; installed exe SHA256 identical to WI-01.
- Uninstall A: exit 0; install directory and both shortcuts removed; user markers preserved.
- Install B (no Desktop task): exit 0; Start Menu present, Desktop shortcut absent.
- Uninstall B: exit 0; install directory and Start Menu shortcut removed; user markers preserved.
- The user's pre-existing developer server on `0.0.0.0:8000` (PID 12888) was not
  touched; WI-02 used own ports 8123/8124. No global settings, accounts or installed
  system-wide software were changed.

## Raw logs

- `logs/WI-02-build.txt` — full Inno Setup compile log
- `logs/WI-02-toolchain.txt` — specified-vs-working compiler check
- `logs/WI-02-installer-info.txt` — artifact path/size/SHA256
- `logs/WI-02-install-a.txt`, `logs/WI-02-inno-install-a.txt` — install with Desktop task
- `logs/WI-02-runtime-a.txt` — I5–I10 runtime evidence
- `logs/WI-02-uninstall-a.txt`, `logs/WI-02-inno-uninstall-a.txt` — uninstall A
- `logs/WI-02-install-b.txt`, `logs/WI-02-inno-install-b.txt` — install without Desktop task
- `logs/WI-02-uninstall-b.txt`, `logs/WI-02-inno-uninstall-b.txt` — uninstall B
- `logs/WI-02-markers.txt` — user marker creation/hashes
- `logs/WI-02-unittest.txt` — full suite
- `logs/WI-02-status.txt` — final git status/diff stat

## Reused WI-01 evidence

The installed executable is byte-identical to the WI-01 artifact
(SHA256 `36A21986…77CC`), so the WI-01 native-window screenshot
(`WI-01-packaged-window.png`) and launch-error screenshot
(`WI-01-launch-error.png`) describe the same binary. WI-02 additionally observed
the installed native window (handle/title) and the installed error dialog (handle
plus exact logged message) directly.

## NOT_RUN / limitations

- Clean second Windows x64 machine or VM was not available; install/uninstall were
  verified on this machine only.
- Code signing, auto-update, telemetry, cloud, GitHub Release/publication,
  push/merge/deploy were **not** performed (out of scope).
- No installer screenshot or UI click-through of every control was captured; the
  three modes were proven via exact HTTP requests/responses against the installed
  backend and the native window was observed programmatically.
- Inno Setup compiler distribution used was the local Antigravity-bundled full
  Inno Setup 6.4.1 because the TASK-specified portable directory lacks
  `ISCmplr.dll`; this is a toolchain deviation to note for review.
- The installer is unsigned; Windows SmartScreen may warn on first launch on a
  different machine.
- First launch on a target machine still requires the Microsoft Edge WebView2
  Runtime (Windows OS component); the existing understandable error dialog covers
  its absence.
- User marker files created for I11 remain in Documents, Desktop and
  `%LOCALAPPDATA%\GasProjectCalculator` intentionally so a reviewer can confirm
  they survived uninstall; they can be deleted manually.
- A worker success assertion is not acceptance; independent routed review is required.
