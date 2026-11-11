# Windows installer stage — R3 final stage acceptance

## Role and scope

You are the Codex final stage acceptance reviewer (R3, `gpt-6-astra` high). This
is the independent stage acceptance for the user-approved **Windows installer**
stage, not a per-TASK correction. Inspect the actual integrated diff and evidence,
map delivered behavior to the approved requirements/architecture/roadmap, and
return one bounded verdict. Do not edit files, commit, push, merge, deploy or
publish. Do not rerun already-proven commands unless an artifact is missing or
ambiguous; reuse complete evidence under the review policy.

- Repository/worktree: `D:/Antigravity/GasProjectCalculator`, branch
  `feature/windows-installer`.
- Stage baseline: `22133a13da0ccb70fc70b93c18529581ad7e43a1` (`22133a1`,
  `feature/gsv` HEAD before the stage).
- Final revision: `3d291e9082342e30759a6cbec7ab1f7c230cc7a7` (`3d291e9`).
- Stage commits: WI-01 `7fab960`, WI-02 `144a75c`, WI-03 `9eaed0a`, docs/state
  `3d291e9`.
- Approval: `docs/workflow/APPROVALS.md` (2026-11-11 Windows installer), with
  ARCHITECTURE SHA256 `259604B4…3375` and ROADMAP SHA256 `78796A2C…FA7F`.
- Stage authority: `AGENTS.md`, `ARCHITECTURE.md` section «Отдельное
  Windows-приложение и установщик», `ROADMAP.md` steps 8–9.

## Required independent assessment

1. **Scope compliance.** The stage diff `git diff 22133a1..3d291e9` contains only
   packaging/launcher/window/installer config, scoped dependencies, tests for
   launcher helpers, README/docs/evidence, and the approved planning documents.
   No change to VISION.md, GSV requirements/business rules, calculation/API
   contracts or developer uvicorn behavior. No code signing, auto-update,
   telemetry, cloud, push, merge, deploy, GitHub Release/publication, global
   config/account change or user-data deletion.
2. **Frozen checklist** (from AGENTS.md / ROADMAP / ARCHITECTURE):
   clean x64 build; installer installs and creates Start Menu and optional
   Desktop shortcuts; no Python/terminal prerequisite; first launch waits for
   backend readiness; GSN/GSV/combined all calculate; bind localhost only and
   handle port conflict safely; closing the window exits the backend; understandable
   launch failure; install/uninstall does not delete user files; developer uvicorn
   path still works; README directs users to the installer after the artifact exists.
3. **Evidence sufficiency.** Verify the TASK reviews/records and evidence packs
   substantiate the checklist, and that the final integrated evidence
   (`docs/workflow/evidence/FINAL-WINDOWS-INSTALLER-EVIDENCE.md`) is consistent
   with the actual commits/artifact. The artifact is local and git-ignored:
   `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`, 15 256 037 bytes,
   SHA256 `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`.
4. **Correctness of accounting.** Codex calls used: WI-01 1, WI-02 1, WI-03 0,
   FINAL verification 0; this is the stage-acceptance call 1. R2 caps 4 calls/3M
   each; R3 cap 6 calls/5M.

## Inputs

- `docs/workflow/tasks/WI-01.md`, `WI-02.md`, `WI-03.md`, `FINAL-VERIFY.md`
- `docs/workflow/reviews/WI-01-review.md`, `WI-02-review.md`, `WI-03-review.md`
- `docs/workflow/evidence/WI-01-evidence.md`, `WI-02-evidence.md`,
  `WI-03-evidence.md`, `FINAL-WINDOWS-INSTALLER-EVIDENCE.md`
- raw logs under `docs/workflow/evidence/logs/WI-01-*`, `WI-02-*`, `FINAL-*`
- screenshots `docs/workflow/evidence/WI-01-packaged-window.png`,
  `WI-01-launch-error.png`
- README.md

## Known limitations / backlog (assess, do not silently expand scope)

- `WI02-R1-F1` **MINOR** backlog: `installer/verify-runtime.ps1` recursively
  deletes a caller-supplied `WorkDir` after only `GetFullPath`; verification
  helper hardening, not a product runtime defect, not claimed fixed.
- Clean second Windows x64 machine/VM unavailable; build/install/runtime verified
  on this machine only.
- Installer is unsigned (SmartScreen may warn); local artifact only.
- First launch requires the Microsoft Edge WebView2 Runtime; absence is covered by
  the tested understandable failure dialog.
- Toolchain deviation accepted in WI-02: the originally noted portable ISCC
  lacked `ISCmplr.dll`; a validated local full Inno Setup 6.4.1 was used without
  system installation.

## Verdict format

Return exactly one bounded verdict:

1. `PASS` or `FAIL` (or `BLOCKED` with the missing prerequisite).
2. For FAIL/BLOCKED: findings `WI-STAGE-R1-Fn` with severity
   (BLOCKER/MAJOR/MINOR/NIT), criterion, location, observed vs expected,
   reproduction/evidence, and closure requirement.
3. Checklist items verified from evidence vs. reran yourself.
4. Confirm or correct the recorded accounting/scope statements.
5. End your turn after the verdict; no file edits and no dispatch.
