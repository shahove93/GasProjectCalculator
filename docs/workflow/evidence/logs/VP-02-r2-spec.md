# VP-02 R2 independent review — self-contained spec

You are a real Orca **Codex** worker, model **`gpt-6.1-sol`**, effort **`high`**.
You are the independent R2 reviewer for logical TASK **MD-03**, approach **A2**,
cycle **C1**, of the СС.Расчет visual-polish stage. You are not the implementer
and you must not accept or modify the product.

## Hard rules

- **Read-only.** Do not edit, create, delete, or move any file. Do not run the
  installer, build, install/uninstall, tests, or network requests. Read-only
  shell is allowed only for `git diff`, `git status`, `Get-FileHash`,
  `Get-Item`, and reading files.
- Use **actual diff and primary sources**, not summaries alone.
- Use real vision on the required images listed below; do not infer visuals
  from filenames or prose.
- Do not duplicate already-proven build/install/lifecycle/test runs unless you
  find a concrete evidence gap or contradiction. If you re-run a read-only
  command, record exact command/CWD/exit and why.
- Finish with exactly one `worker_done` containing the verdict. Do not edit
  review files; the coordinator writes them.

## Workspace and baseline

- CWD/workspace: `D:/Antigravity/GasProjectCalculator`, branch
  `feature/gsv-mixed-diameters`, baseline/HEAD
  `1689773718c818a4ebca400afc2d8a4206b6458e` (VP-01 / MD-02 A2 already PASS).
- Approved scope: `docs/workflow/VISUAL-POLISH-ASTRA-BRIEF.md`,
  `docs/workflow/VISUAL-POLISH-LEAN-FINISH.md`,
  `docs/workflow/APPROVALS.md` (Astra/1.2.0 + Lean finish sections),
  `docs/workflow/tasks/VP-02.md`.
- Frozen checklist: **W1–W11** in `docs/workflow/tasks/VP-02.md`. Do not add,
  remove, or weaken criteria.

## Bounded packet (read these first)

1. `docs/workflow/reviews/VP-02-review-packet.md` — the full bounded review
   instructions; follow it.
2. `docs/workflow/evidence/VP-02-evidence.md` — evidence pack (including the
   Lean finish section: five settled shots + 219-test suite).
3. `docs/workflow/evidence/logs/VP-02-resumed-product.diff` — actual product diff.
4. `docs/workflow/evidence/logs/VP-02-resumed-manifest.json`,
   `VP-02-old-artifacts-before.json`, `VP-02-resumed-preflight.json`.
5. `docs/workflow/evidence/logs/VP-02-resumed-settled-shots.json` and
   `VP-02-final-full-suite.txt` / `.exit.txt`.

## Required observations

- **Actual diff/allowlist:** only `installer/GasProjectCalculator.iss`
  (version/branding), `installer/build-installer.ps1` (version-specific
  output guard), and new `installer/assets/**`. `app/`, `frontend/`,
  `packaging/`, `requirements*`, `tests/` must be zero-diff vs HEAD.
- **Artifact:** `installer/Output/GasProjectCalculator-Setup-1.2.0.exe`,
  15 373 267 B, FileVersion `1.2.0.0`, ProductVersion `1.2.0`, SHA256
  `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113`;
  prior 1.0.0/1.1.0/legacy bytes unchanged.
- **Vision — installer:** `docs/screenshots/visual-02-wizard-welcome.png`,
  `-dir`, `-tasks`, `-ready`, `-installing`, `-finish` (598×464). Check
  branded sidebar/header, RU labels/buttons, contrast, no control overlap,
  Inno Setup 6.4.1, RU-only, prior AppId, Desktop task off by default, and
  motive consistency with `docs/design/splash-installer-reference.jpg`.
- **Vision — installed app:** `visual-02-native-splash.png`,
  `visual-02-resumed-native-target-gsn/gsv/combined.png`,
  `visual-02-resumed-native-minimum-gsn/gsv/combined.png`,
  `visual-02-resumed-native-startup-error.png`,
  `visual-02-resumed-splash-os/flag/animated.png`.
- **Vision — five settled frames:**
  `visual-02-resumed-desktop-gsv-D1..D5-settled.png` (800×540,
  `scrollY=0`, `opacity=1`, totals 75600/79275/71400/63000/70875).
- **W5/W9:** isolated install 1.1.0 → upgrade 1.2.0 → reinstall → uninstall,
  numeric exits 0; HKCU/shortcuts exact restore; 106 user files unchanged;
  sentinel user files preserved.
- **W7 values:** combined 151000/7550/158550; legacy/422; ГСН regression;
  САКЗ/ПК/район/НДС 5%; mode switching.
- **W8:** loopback-only, occupied test port, close terminates backend/launcher
  without children, Russian error path/exit 1, reduced motion.
- **W10:** targeted 36 OK; full suite 219 OK/exit 0; static 137 assertions;
  manifest 48 PNG/5 artifacts/106 user files; `git diff --check` exit 0.

## Verdict format (in worker_done)

Return:

- **PASS / FAIL** for the whole R2 review.
- Per-W1–W11 verdict with the actual evidence path/value you observed.
- Severity for any finding: BLOCKER / MAJOR / MINOR / NIT, with stable IDs.
- List of images actually viewed with vision.
- Residual risks and explicit NOT_RUN items.
- `requested/effective` model/agent/effort as you understand them.

PASS only if all criteria are met. MINOR/NIT do not require a new cycle.
BLOCKER/MAJOR means FAIL with exact localization and evidence; do not fix it
yourself.
