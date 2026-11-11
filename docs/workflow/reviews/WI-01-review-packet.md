# WI-01 R2 Codex review packet

## Task

Independent acceptance review of logical TASK **WI-01 — packaged desktop app and
native window**, risk class **R2**. You are the Codex reviewer. This is a bounded
review: inspect the actual diff and the supplied evidence, map them to the frozen
checklist, and return one verdict. Do not implement, do not edit any file, do not
commit, and do not expand the checklist.

- Frozen checklist: `docs/workflow/tasks/WI-01.md` (section "Frozen acceptance
  checklist").
- Baseline commit: `22133a13da0ccb70fc70b93c18529581ad7e43a1`.
- Branch/worktree: `feature/windows-installer`,
  `D:/Antigravity/GasProjectCalculator`.
- Cycle: C1 first full review. Codex calls used for WI-01 before this review: 0.

## Review scope (product diff)

Review these paths only:

- `app/main.py` (modified: `/` now uses `frontend_index_path()`)
- `app/resources.py` (new)
- `app/desktop_launcher.py` (new)
- `desktop_app.py` (new)
- `packaging/GasProjectCalculator.spec`, `packaging/build.ps1`,
  `packaging/README.md` (new)
- `requirements-desktop.txt` (new)
- `tests/test_desktop_launcher.py` (new)
- `.gitignore` additions
- Evidence under `docs/workflow/evidence/WI-01-*`

Out of scope and coordinator-owned pre-existing changes:
`AGENTS.md`, `ARCHITECTURE.md`, `README.md`, `ROADMAP.md`,
`docs/workflow/APPROVALS.md`, `docs/workflow/STATE.md`,
`docs/workflow/HISTORY.md`, `docs/workflow/WINDOWS-INSTALLER-BRIEF.md`,
`docs/workflow/tasks/`. These are approved planning/coordinator records; do not
review them as product changes.

Inspect with, for example:

```powershell
git diff 22133a1 -- app/main.py .gitignore
git status --short
git diff --no-index NUL app/desktop_launcher.py   # or read the new files
```

## Evidence pack

- `docs/workflow/evidence/WI-01-evidence.md`
- `docs/workflow/evidence/logs/WI-01-*.txt`
- `docs/workflow/evidence/WI-01-packaged-window.png`,
  `docs/workflow/evidence/WI-01-launch-error.png`

The evidence claims: build exit 0; artifact
`dist\GasProjectCalculator\GasProjectCalculator.exe` SHA256
`36A21986EB9A55F1D5309C7AA3E22EDD7EE9F12418B4EC4C27D051B9F77177CC`;
127.0.0.1-only listener on 8001 while user port 8000 stayed untouched; readiness
before window; three modes' totals; window-close release; failure dialog; full
suite 146 OK.

## Review rules

- Verify the claims against actual files and logs. Reuse complete evidence; do
  not routinely rerun proven commands. Only a missing/ambiguous artifact permits
  one rerun of that command, recorded with reason.
- Check behavior against the frozen checklist W1–W10, including: loopback-only
  bind, safe port conflict with the user's 8000, readiness gate, three modes,
  window-close exit with no leftover listener/process, understandable failure,
  developer uvicorn path, and no contract/calculation regression.
- Findings outside the frozen checklist are backlog proposals, not scope
  expansion.
- Severity: BLOCKER/MAJOR → FAIL; MINOR/NIT only → PASS with backlog.

## Required output

Return a single bounded verdict:

1. `PASS` or `FAIL` (or `BLOCKED` with the missing prerequisite).
2. Findings with stable IDs `WI01-R1-Fn`, severity, criterion, location,
   observed vs expected, reproduction/evidence, and closure requirement.
3. Which checklist items you verified from evidence vs. reran yourself.
4. End your turn after the verdict. Do not edit files and do not dispatch work.
