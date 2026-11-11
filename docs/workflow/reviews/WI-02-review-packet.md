# WI-02 R2 Codex review packet

## Task

Independent acceptance review of logical TASK **WI-02 — Inno Setup installer,
shortcuts, clean install/uninstall**, risk class **R2**. You are the Codex
reviewer. Inspect the actual diff and supplied evidence, map them to the frozen
checklist, and return one verdict. Do not implement, edit files, commit, push or
expand the checklist.

- Frozen checklist: `docs/workflow/tasks/WI-02.md` (section "Frozen acceptance
  checklist").
- Baseline commit: `7fab9606ae4f704fe82cafa1caa1e4091b175533` (WI-01 PASS commit).
- Branch/worktree: `feature/windows-installer`,
  `D:/Antigravity/GasProjectCalculator`.
- Cycle: C1 first full review. Codex calls used for WI-02 before this review: 0.

## Review scope (product diff)

Review only:

- `installer/GasProjectCalculator.iss`
- `installer/build-installer.ps1`
- `installer/verify-install.ps1`
- `installer/verify-runtime.ps1`
- `installer/verify-uninstall.ps1`
- `.gitignore` installer-output additions
- Evidence `docs/workflow/evidence/WI-02-evidence.md` and
  `docs/workflow/evidence/logs/WI-02-*`

Out of scope and coordinator-owned: `AGENTS.md`, `ARCHITECTURE.md`, `README.md`,
`ROADMAP.md`, `docs/workflow/APPROVALS.md`, `STATE.md`, `HISTORY.md`,
`docs/workflow/tasks/` (including the WI-02 baseline-note edit),
`docs/workflow/WINDOWS-INSTALLER-BRIEF.md`. Do not review them as product changes.

Inspect with, for example:

```powershell
git diff 7fab960 -- .gitignore
git status --short
# read the new installer/ files and the evidence pack
```

## Claimed evidence

- Artifact: `installer\Output\GasProjectCalculator-Setup-1.0.0.exe`,
  15 256 037 bytes, SHA256
  `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`.
- Built with `/VERYSILENT` as a per-user (`HKCU`, lowest privileges) install;
  Start Menu shortcut always; optional Desktop task; uninstall removes program
  files/shortcuts but preserves user markers.
- Installed exe is byte-identical to the WI-01 artifact
  (`36A21986…77CC`); Python-free PATH launch; loopback-only 127.0.0.1; readiness
  before window; three modes totals; window close exits; failure dialog exit 1.
- Full suite 146 OK; no application source/API changes.
- Toolchain deviation: the task-specified ISCC directory lacks `ISCmplr.dll`;
  the build script validates candidates and fell back to the local
  Antigravity-bundled full Inno Setup 6.4.1 at
  `C:\Users\user\AppData\Local\Programs\Antigravity IDE\resources\app\node_modules\innosetup\bin\ISCC.exe`.
  Assess whether this is acceptable within scope and whether the artifact is a
  genuine clean x64 Inno Setup build; if the criterion is not met, flag it.

## Review rules

- Verify claims against actual files/logs. Reuse complete evidence; do not
  routinely rerun proven commands. Only a missing/ambiguous artifact permits one
  rerun of that command, recorded with reason.
- Check checklist I1–I12, including per-user no-admin install, Start Menu and
  optional Desktop shortcuts, no Python/console, readiness, all three modes,
  localhost-only/port conflict, window-close exit, understandable failure,
  user-file preservation on uninstall, developer uvicorn path, and no contract
  changes.
- If you install to re-check, use silent install/uninstall, clean up afterwards,
  never touch the user's port-8000 server, and make no repository edits.
- Findings outside the frozen checklist are backlog proposals.
- Severity: BLOCKER/MAJOR → FAIL; MINOR/NIT only → PASS with backlog.

## Required output

Return one bounded verdict:

1. `PASS` or `FAIL` (or `BLOCKED` with missing prerequisite).
2. Findings `WI02-R1-Fn` with severity, criterion, location, observed vs expected,
   evidence, closure requirement.
3. Which items verified from evidence vs. reran yourself.
4. End your turn after the verdict; no file edits, no dispatch.
