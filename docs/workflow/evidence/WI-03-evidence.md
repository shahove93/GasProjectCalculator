# WI-03 evidence — user and developer documentation (R0)

Status: implementer evidence only. This is **not** project PASS and not acceptance;
independent routed review follows. No commit, push, merge, deploy, signing or
release was performed.

## Baseline and working tree

- Repository: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/windows-installer`
- Baseline commit: `144a75c` (`feat(installer): add per-user Inno Setup installer (WI-02)`)
- Pre-existing uncommitted planning/workflow changes were preserved and **not
  edited by WI-03**: `AGENTS.md`, `ARCHITECTURE.md`, `ROADMAP.md`,
  `docs/workflow/APPROVALS.md`, `docs/workflow/HISTORY.md`,
  `docs/workflow/STATE.md`, `docs/workflow/tasks/WI-02.md`,
  `docs/workflow/tasks/WI-03.md`, untracked
  `docs/workflow/WINDOWS-INSTALLER-BRIEF.md`.
  `README.md` was also already modified before WI-03 (stale sentence saying the
  installer "will be attached later"); that sentence was replaced by this task.
- WI-03 change set: `README.md` **only**, plus new `docs/workflow/evidence/WI-03-*`.
  No application code, tests or planning/status document was edited.

## Artifact re-verification (fresh, this task)

Command and raw output:

```powershell
Get-FileHash installer\Output\GasProjectCalculator-Setup-1.0.0.exe -Algorithm SHA256
(Get-Item installer\Output\GasProjectCalculator-Setup-1.0.0.exe).Length

Algorithm : SHA256
Hash      : 2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F
Path      : D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe

15256037
```

This matches the TASK-specified artifact and `WI-02-evidence.md`.

## README changes

- New top-level `## Установка на Windows` section: exact local installer path,
  size and SHA256; per-user install with no admin rights; launch from Start Menu
  and the optional (unchecked by default) Desktop shortcut; unsigned local
  artifact and possible SmartScreen warning; localhost-only backend; closing the
  window stops the app; user files stored outside the install directory;
  `### Удаление`; `### Доказательства` linking WI-01/WI-02/WI-03 evidence.
- Existing developer content moved under `## Для разработчика (запуск из
  исходного кода)` with unchanged commands for venv, pip, uvicorn, browser URL
  and tests; the old source-run section became
  `### Запуск из исходного кода на другом компьютере` and its stale
  "installer will be attached later" sentence was removed.
- New `## Устранение неполадок и данные пользователя`: WebView2/antivirus
  launch-failure guidance, log path, localhost/port behavior, install directory
  and user-data location.
- Calculator documentation, business rules, examples, screenshots and API
  endpoints were left intact; only the "Работает в браузере" bullet was reworded
  to state that the same UI opens in the app window or in a browser when running
  from source.

## Frozen acceptance checklist evidence

| ID | Result | Evidence |
| --- | --- | --- |
| D1 | PASS (implementer) | README `## Установка на Windows` step 1 contains the exact path `D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe`, size `15 256 037` and SHA256 `2973278F…37428F`; re-verified above and in `logs/WI-02-installer-info.txt`, `logs/WI-02-build.txt`. |
| D2 | PASS (implementer) | README states "Python и командная строка не нужны" for installed users and gives a GUI-only flow. Supported by tested Python-free launches: WI-01 W2 and WI-02 I5 (`PATH=C:\Windows\System32;C:\Windows`, `python` not found) in `logs/WI-01-packaged-run.txt`, `logs/WI-02-runtime-a.txt`. |
| D3 | PASS (implementer) | Developer commands preserved verbatim under `## Для разработчика`: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`, `http://127.0.0.1:8000/`, `.\.venv\Scripts\python.exe -m unittest discover -s tests`, plus the source-run section. Developer uvicorn path evidence: `logs/WI-01-dev-uvicorn.txt`, `logs/WI-02-unittest.txt` (146 tests OK). |
| D4 | PASS (implementer) | README states localhost-only `127.0.0.1`, window close stops the app/releases the port, install dir `%LOCALAPPDATA%\Programs\GasProjectCalculator`, user files in `%LOCALAPPDATA%\GasProjectCalculator` preserved on uninstall. Matches WI-01 W3/W7 (`logs/WI-01-packaged-run.txt`, `logs/WI-01-visual-run.txt`) and WI-02 I8/I9/I11 (`logs/WI-02-runtime-a.txt`, `logs/WI-02-uninstall-a.txt`, `logs/WI-02-uninstall-b.txt`, `logs/WI-02-markers.txt`). The uninstall route through Windows Settings → Apps is the standard registration of the same tested Inno uninstaller (`unins000.exe`); the silent UI-independent uninstall was executed and logged in WI-02. |
| D5 | PASS (implementer, scoped) | WI-03 edited only `README.md`; evidence files added under `docs/workflow/evidence/WI-03-*`. `git diff --name-only -- README.md` → `README.md`. Other modified planning files in `git status` pre-date WI-03 and were preserved untouched (see baseline list). No writes to `AGENTS.md`, `ARCHITECTURE.md`, `VISION.md`, `ROADMAP.md`, `APPROVALS.md`, `STATE.md`, `HISTORY.md`, `MODEL-ROUTING.md` or application code. |

## Disagreements between README text and tested behavior

- None found. Two points are intentionally scoped:
  - First launch needs the Microsoft Edge WebView2 Runtime; this is documented as
    a troubleshooting condition, not claimed as preinstalled by the installer.
  - The "Settings → Apps" uninstall path was not click-tested via GUI; the same
    Inno uninstaller was exercised silently in WI-02. The README describes the
    normal Windows uninstall route and the behavior verified by that uninstaller.
- `WI02-R1-F1` (MINOR backlog) is not addressed or claimed as fixed by WI-03.

## Limitations

- Documentation-only change; no installer, runtime or test suite was re-run for
  WI-03 (no basis under review policy to repeat already evidenced checks).
- The installer remains an unsigned local artifact and was not published or
  committed (`installer/Output/` is git-ignored).
- A worker success assertion is not acceptance; independent routed review is
  required.
