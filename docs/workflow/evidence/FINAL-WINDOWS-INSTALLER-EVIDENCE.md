# FINAL verification evidence — integrated Windows installer stage (R0)

Status: verification-worker evidence only. This is **NOT** project PASS and **not**
stage acceptance. The coordinator records the R0 checklist acceptance and Codex
performs the final R3 stage acceptance afterwards.

This verification made **no product change**: no application code, packaging,
installer script, test, requirement, README or planning document was edited,
rebuilt or re-run beyond the read-only checks below. No commit, push, merge,
deploy, signing or publication was performed. New files are evidence only.

## Final revision and baseline

- Repository / worktree: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/windows-installer`
- Final revision (HEAD): `9eaed0a1c58c07ae2ec55e1c8d02eec3a4b30fa8` (`9eaed0a`) —
  `docs(readme): document Windows installer and developer path (WI-03)`
- Accepted stage commits:
  - WI-01 `7fab9606ae4f704fe82cafa1caa1e4091b175533` (`7fab960`)
  - WI-02 `144a75c2b54c1393fdb005d96cee2303bcf07dd1` (`144a75c`)
  - WI-03 `9eaed0a1c58c07ae2ec55e1c8d02eec3a4b30fa8` (`9eaed0a`)
- Verification date: 2026-11-11.
- Raw commands/exit codes/outputs: `docs/workflow/evidence/logs/FINAL-*-2026-11-11.txt`
  (see the log index at the end).

## Verification environment

- Windows x64, Windows PowerShell 5.1, Python 3.12.4 in project venv
  (`.venv\Scripts\python.exe`).
- Evidence was **reused**: WI-01, WI-02 and WI-03 artifacts/checks were not
  rebuilt, and install/uninstall was not repeated, because `git diff` proves no
  source/packaging/installer/test change occurred after the accepted WI-02
  artifact.

## Required checks — exact commands and results

All commands were run with CWD `D:\Antigravity\GasProjectCalculator`.

### 1. Integrated diff since accepted WI-02 artifact

| Item | Value |
| --- | --- |
| Command | `git diff 144a75c..9eaed0a --stat` and `git diff 144a75c..9eaed0a --name-only` |
| Exit code | `0` |
| Result | Only 3 files: `README.md`, `docs/workflow/evidence/WI-03-evidence.md`, `docs/workflow/reviews/WI-03-review.md` (196 insertions, 7 deletions). |
| Product-path probe | `git diff 144a75c..9eaed0a --name-only -- app packaging installer tests requirements.txt requirements-desktop.txt` → **no files** |
| Log | `logs/FINAL-git-diff-2026-11-11.txt` |

Conclusion: between the accepted WI-02 commit and the final WI-03 commit there is
**no** change to application code, packaging, installer scripts, tests or
requirements — only README/evidence/review documentation.

Final working tree: tracked modifications are pre-existing, preserved planning
documents only (`AGENTS.md`, `ARCHITECTURE.md`, `ROADMAP.md`,
`docs/workflow/APPROVALS.md`, `docs/workflow/HISTORY.md`,
`docs/workflow/STATE.md`, `docs/workflow/tasks/WI-02.md`,
`docs/workflow/tasks/WI-03.md`) plus untracked
`docs/workflow/WINDOWS-INSTALLER-BRIEF.md`, `docs/workflow/tasks/FINAL-VERIFY.md`
and the new `FINAL-*` evidence. A scoped status of product paths
(`app`, `packaging`, `installer`, `tests`, `requirements*.txt`) is **clean**.
Log: `logs/FINAL-worktree-2026-11-11.txt`.

### 2. Installer artifact path, size and hash (re-verified, not trusted)

| Item | Value |
| --- | --- |
| Path | `D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe` |
| Exists | `True` |
| Size | `15 256 037` bytes |
| SHA256 | `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F` |
| Matches expected | **Yes** (path, size and hash all match the TASK baseline and WI-02 evidence) |
| Log | `logs/FINAL-artifact-2026-11-11.txt` |

### 3. Full test suite on the integrated final state

| Item | Value |
| --- | --- |
| Command | `.\.venv\Scripts\python.exe -m unittest discover -s tests` |
| Exit code | `0` |
| Result | `Ran 146 tests in 2.041s` → `OK` |
| Log | `logs/FINAL-suite-2026-11-11.txt` |

The log contains the exact command, CWD, exit code and raw output. The only
stderr line is a pre-existing benign `StarletteDeprecationWarning` about
`httpx`/`testclient`; it does not affect the result.

### 4. User's developer uvicorn on port 8000 untouched

The user's pre-existing developer server is still listening and was **not**
started, stopped or modified by this verification:

```
LocalAddress  : 0.0.0.0
LocalPort     : 8000
State         : Listen
OwningProcess : 12888
CommandLine   : "C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe"
                -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Log: `logs/FINAL-dev-uvicorn-2026-11-11.txt`.

### 5. README installer path/hash and developer path

| Item | Result |
| --- | --- |
| Installer section states Python and a command line are not needed for ordinary users | Confirmed |
| Exact artifact path | README line 12: `D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe` |
| Exact size | README line 13: `15 256 037` bytes |
| Exact SHA256 | README line 14: `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F` |
| Developer path preserved | Confirmed: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` (140), `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload` (146), `http://127.0.0.1:8000/` (154), `.\.venv\Scripts\python.exe -m unittest discover -s tests` (160), source-run uvicorn (177) |
| Log | `logs/FINAL-readme-2026-11-11.txt` |

README path, size and hash match the re-verified artifact exactly.

## Frozen stage checklist → accepted evidence map

Chart of the approved stage checklist (ROADMAP steps 8–9; AGENTS.md Windows
installer stage) to the accepted evidence. All referenced evidence was produced
during the accepted WI-01/WI-02/WI-03 work; this verification reused it.

| # | Checklist item | Accepted evidence | Status |
| --- | --- | --- | --- |
| 1 | Clean x64 build (PyInstaller onedir, native window, no console) | WI-01 W1–W2: `packaging/build.ps1` exit 0, PyInstaller 6.22.3, artifact `dist\GasProjectCalculator\GasProjectCalculator.exe` SHA256 `36A21986…77CC`, PE subsystem 2 `WINDOWS_GUI`; `logs/WI-01-build.txt`, `logs/WI-01-packaged-run.txt`, `WI-01-packaged-window.png` | PASS (accepted) |
| 2 | Installer + Start Menu shortcut + optional Desktop shortcut | WI-02 I1–I4: Inno Setup 6.4.1 build exit 0; silent HKCU install exit 0; Start Menu shortcut always present with correct target/args; Desktop shortcut present only with `/TASKS="desktopicon"` (unchecked by default); `logs/WI-02-build.txt`, `logs/WI-02-install-a.txt`, `logs/WI-02-install-b.txt`, `logs/WI-02-inno-install-a.txt`, `logs/WI-02-inno-install-b.txt` | PASS (accepted) |
| 3 | No Python/terminal prerequisite | WI-01 W2 and WI-02 I5: installed/packaged exe launched with `PATH=C:\Windows\System32;C:\Windows` (`python` not found) and no console; `logs/WI-01-packaged-run.txt`, `logs/WI-02-runtime-a.txt`; README states Python/CLI not needed | PASS (accepted) |
| 4 | First-launch readiness before window | WI-02 I6: `status=ready` written before native window observed, log order `Backend ready 0.75s` → `Wrote port file` → `Creating native window`; WI-01 W5; `logs/WI-02-runtime-a.txt`, `logs/WI-01-packaged-run.txt` | PASS (accepted) |
| 5 | All three modes (GSN, GSV, combined) | WI-01 W6 and WI-02 I7 against packaged/installed backend: GSN `subtotal=125000 vat=6250 total=131250`; GSV `subtotal=100500 vat=5025 total=105525`; combined `subtotal=139000 vat=6950 total=145950`; `logs/WI-01-packaged-run.txt`, `logs/WI-02-runtime-a.txt`, baseline `logs/WI-01-baseline-api.txt` | PASS (accepted) |
| 6 | Localhost-only binding + port conflict handling | WI-01 W3–W4 and WI-02 I8: only `127.0.0.1` listener (no `0.0.0.0`); busy `8123`/user `8000` skipped; installed app used `127.0.0.1:8124`; `logs/WI-01-packaged-run.txt`, `logs/WI-02-runtime-a.txt` | PASS (accepted) |
| 7 | Window close exits backend / releases port | WI-01 W7 and WI-02 I9: exit code 0, no listener on used port, no child processes; `logs/WI-01-packaged-run.txt`, `logs/WI-01-visual-run.txt`, `logs/WI-02-runtime-a.txt` | PASS (accepted) |
| 8 | Understandable failure (WebView2/antivirus) | WI-01 W8 and WI-02 I10: native Russian message dialog, exit code 1, `status=failed`; screenshots `WI-01-launch-error.png`; `logs/WI-01-error-run.txt`, `logs/WI-02-runtime-a.txt` | PASS (accepted) |
| 9 | Install/uninstall preserves user files | WI-02 I2–I11: two install/uninstall cycles exit 0; both shortcuts and program dir removed; three user markers outside `{app}` (Documents, Desktop, `%LOCALAPPDATA%\GasProjectCalculator`) all preserved; `logs/WI-02-install-a.txt`, `logs/WI-02-install-b.txt`, `logs/WI-02-uninstall-a.txt`, `logs/WI-02-uninstall-b.txt`, `logs/WI-02-markers.txt` | PASS (accepted) |
| 10 | Developer uvicorn path still works | WI-01 W9 developer path verified on `127.0.0.1:8010` (`GET /` 200, GSV total 63000); user server on `0.0.0.0:8000` (PID 12888) untouched; `logs/WI-01-dev-uvicorn.txt`, `logs/WI-02-unittest.txt` (146 OK). This verification re-confirms PID 12888 still listening untouched: `logs/FINAL-dev-uvicorn-2026-11-11.txt` | PASS (accepted + re-confirmed) |
| 11 | README directs users to the installer | WI-03 D1–D5 review PASS; README `## Установка на Windows` step 1 contains exact path/size/SHA256, GUI-only flow, uninstall and troubleshooting sections, and preserves the developer section; `logs/FINAL-readme-2026-11-11.txt`; `docs/workflow/reviews/WI-03-review.md` | PASS (accepted) |

## NOT_RUN (deliberately, per task and review policy)

- Application and installer were **not** rebuilt: no change after the accepted
  WI-02 artifact.
- Install/uninstall was **not** repeated: WI-02 evidence is accepted and no real
  evidence gap was found.
- Clean second Windows x64 machine/VM validation was **not** available.
- Code signing, auto-update, telemetry, GitHub Release/publication, push, merge
  and deploy were **not** performed.
- GUI click-through of the Windows "Settings → Apps" uninstall route was **not**
  re-run; the same Inno `unins000.exe` was silently exercised in WI-02.
- This worker did **not** run browser UI verification for this stage (UI/browser
  behavior belongs to the previously accepted GSV stage).

## Residual risks / backlog

1. `WI02-R1-F1` **MINOR** (open, kept in `FINAL-REPORT`): `installer/verify-runtime.ps1`
   recursively deletes a caller-supplied `WorkDir` after only `GetFullPath`; a
   verification helper should own/validate a dedicated scratch directory and
   refuse unrelated existing directories. Not a product runtime defect; not
   claimed fixed by WI-03.
2. Second-machine validation is unavailable: build/install/runtime were verified
   on this Windows x64 machine only. The installer remains a local artifact.
3. The installer is **unsigned**; Windows SmartScreen may warn on first launch,
   especially on another machine. Documented in README.
4. First launch requires the Microsoft Edge WebView2 Runtime (OS component).
   Its absence is covered by the tested understandable failure dialog.
5. `installer/Output/` is git-ignored; the artifact is for local hand-off and was
   not published or committed.

## No-product-change statement

No product change was made by this verification. Only new evidence files were
added under `docs/workflow/evidence/` (`FINAL-WINDOWS-INSTALLER-EVIDENCE.md` and
`logs/FINAL-*-2026-11-11.txt`). No code, packaging, installer, test,
requirement, README or planning document was modified; no commit, push, merge,
deploy or publication occurred.

## Log index

| Log | Content |
| --- | --- |
| `logs/FINAL-git-diff-2026-11-11.txt` | Branch/HEAD/commit SHAs, `git diff 144a75c..9eaed0a --stat` and `--name-only`, product-path probe |
| `logs/FINAL-artifact-2026-11-11.txt` | Installation artifact `Test-Path`, size, SHA256 |
| `logs/FINAL-suite-2026-11-11.txt` | Full suite command, CWD, exit code and raw output (146 OK) |
| `logs/FINAL-dev-uvicorn-2026-11-11.txt` | Port 8000 listener and process command line (untouched) |
| `logs/FINAL-readme-2026-11-11.txt` | README installer section, matched path/hash/developer commands, developer section |
| `logs/FINAL-worktree-2026-11-11.txt` | `git status`, product-path scoped status and tracked diff stat |
