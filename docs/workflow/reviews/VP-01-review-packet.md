# VP-01 R2 vision review packet (logical MD-02 / A2 / C1)

## Role and authority

You are the independent **R2 vision reviewer**: real Orca **Codex
`gpt-6.1-sol`, effort `high`**. You did not write this work. Do **not** modify
files, create commits, or run shell commands that write anywhere. Read-only
inspection is expected. Return a bounded verdict and end your turn; do not
wait for or coordinate workers.

Authority: `AGENTS.md`, `docs/workflow/VISUAL-POLISH-ASTRA-BRIEF.md`,
`docs/workflow/APPROVALS.md` (Astra section 2026-11-12),
`docs/workflow/tasks/VP-01.md`, `VISION.md`, `ARCHITECTURE.md`, `ROADMAP.md`,
and the review policy in
`C:/Users/user/.agents/skills/autonomous-development/references/review-policy.md`
(frozen checklist, severity, evidence reuse, counting).

## Review target

- Workspace: `D:/Antigravity/GasProjectCalculator`
- Branch: `feature/gsv-mixed-diameters`
- Baseline: `ac59d8c27ed47be07ac9b54acf8285bcab704be0`
- The implementation is **uncommitted in the working tree** (HEAD unchanged).
- Baseline is historical A1/C1. This is **A2/C1** under new user references;
  prior counters (MD-02 A1/C1: 1 full review, 0 FAIL, 1/4 Codex calls) are
  preserved. Do not treat this as a budget reset.

## Actual product diff to inspect

Only these product paths may differ:

- `frontend/index.html`
- `frontend/splash.html`
- `app/desktop_launcher.py` (only splash geometry/background constants)
- `tests/test_desktop_launcher.py` (one presentation string)
- `frontend/assets/header-pipe.svg`, `footer-pipe.svg`, `splash-scene.svg`,
  `installer-sidebar.svg|png`, `installer-header.svg|png`

A raw product diff is at
`docs/workflow/evidence/logs/VP-01-product.diff`; full status is at
`docs/workflow/evidence/logs/VP-01-status.txt`. Root/coordinator docs
(`AGENTS.md`, `VISION/ARCHITECTURE/ROADMAP`, `APPROVALS/HISTORY/MODEL-ROUTING/
STATE`, TASK/brief/preflight) are out of product scope and pre-existing; verify
they were not used to fake the product result, but do not review them as part
of V1–V12. `backend/API/calculator/requirements` must be zero-diff.

## References (open as images, use vision)

- `docs/design/header-detail-reference.jpg`
- `docs/design/footer-detail-reference.jpg`
- `docs/design/splash-installer-reference.jpg`
- Prior rejected comparisons for context:
  `docs/screenshots/md-02-compare-header.png`,
  `docs/screenshots/md-02-compare-footer.png`,
  `docs/screenshots/md-03-native-splash.png`

Brand must remain **`СС.Расчет`**, subtitle «Калькулятор ГСН и ГСВ» and the
round purple ООО «Северное сияние» emblem. References are visual samples, not
screenshots to paste into the UI.

## Frozen checklist (from VP-01.md)

| ID | Criterion | Evidence |
| --- | --- | --- |
| V1 | Header side-by-side geometry/composition: dark navy, calm translucent teal pipe, metal couplings, wide horizontal gold oval handwheel with stem/valve fully visible, pipe bend as ref; no extra branch, no dashed/dotted fill, no excessive neon | `visual-01-compare-header.png` + native screenshot |
| V2 | Footer side-by-side: light strip, thin contour pipe with couplings, blue flame left, fully visible house with warm window right, tree/bushes, soft ground line; no massive dark pipe/neon, no clipped house/roof | `visual-01-compare-footer.png` + native |
| V3 | Splash side-by-side: dark gradient, title upper third with narrow teal accent, «Подготавливаем расчёт…», continuous pipe with valve left, elbow down, glowing flow to contour house right, warm 4-pane window, hills; no gray photo frame | `visual-01-compare-splash.png` + native splash |
| V4 | No clipping/extraneous details; handwheel fully visible; house/roof fully visible; removed extra branch/dashes/overglow | Native screenshots + SVG/DOM |
| V5 | `СС.Расчет`, subtitle and round emblem preserved; local-only assets, no external URLs | Screenshot + static scan |
| V6 | Real native target 800×540 and min 760×520; browser desktop and mobile 390×844; all three modes action/total available; desktop `scrollY=0`; no screenshot-only CSS/JS/zoom workaround | Screenshots + metrics |
| V7 | Small design improvements only; no broad redesign, field-order/math/mode-name/window-size change | Screenshots + diff |
| V8 | GSN/GSV/combined, mixed lengths/totals, САКЗ/ПК/район/НДС preserved; backend/API/calculator zero-diff | Real values + diff |
| V9 | Splash readiness/close/error/reduced-motion/loopback unchanged; no artificial delay in normal launch | Lifecycle logs/screens |
| V10 | Installer artwork sources prepared (sidebar welcome/finish + small header), local/reproducible, consistent with splash | Asset paths + previews |
| V11 | Targeted presentation/desktop tests green; static no-network scan; diff strictly in allowlist; no functional/security test weakened | Commands/exit/logs + scope |
| V12 | Evidence pack has real images/side-by-sides, not just prose; NOT_RUN marked honestly | `VP-01-evidence.md`, logs, screenshots |

Also verify closure of prior **MD02-N1 (NIT, clipped handwheel)**: the new
geometry must show the whole handwheel within the viewBox/container.

## Evidence pack

Primary: `docs/workflow/evidence/VP-01-evidence.md`.

Key artifacts:

- `docs/workflow/evidence/logs/VP-01-targeted-tests.txt` + `.exit.txt` (36 OK,
  exit 0)
- `docs/workflow/evidence/logs/VP-01-browser.json`,
  `VP-01-browser-run.txt`, `VP-01-mobile-viewport.json`
- `docs/workflow/evidence/logs/VP-01-native.json`,
  `VP-01-native-run.txt`, `VP-01-native-splash.json`,
  `VP-01-normal-launch.log`, `VP-01-error-launch.log`
- `docs/workflow/evidence/logs/VP-01-static.json` (DOM/JS/AST contract,
  backend zero-diff, no external assets)
- `docs/workflow/evidence/logs/VP-01-processes-after-close.json`,
  `VP-01-ports-after-close.json`
- `docs/workflow/evidence/logs/VP-01-artifact-manifest.json`
- Images under `docs/screenshots/visual-01-*`, including the three comparisons,
  native target/min, desktop/mobile, D1–D5, 422/switch, splash/error.

## Evidence and command reuse rule

Inspect the actual diff and underlying artifacts. With complete, unambiguous
evidence, **do not rerun** the same commands. A missing or ambiguous artifact
permits **one** rerun of the corresponding read-only command; record gap,
reason, command, CWD, revision, exit code and result. Otherwise return
FAIL/BLOCKED. Do not broaden the checklist; out-of-checklist observations are
backlog proposals. Do not invent results.

## Verdict format (return in worker_done)

Return concisely:

1. **Verdict: PASS / FAIL / BLOCKED**, with severity per finding.
2. Per criterion V1–V12: confirmed / finding ID (closed/backlog/not verified).
3. Findings with ID, location, observed result, expectation, severity, and
   closure evidence. Only BLOCKER/MAJOR cause FAIL; MINOR/NIT are backlog if all
   criteria pass.
4. MD02-N1 closure status.
5. Actual product diff checked; unexpected files outside allowlist; evidence
   reused vs the single permitted rerun.
6. Files you changed (must be none) and commit (must be none).
7. Counters for this review: full reviews 1, failed 0/1, Codex calls used.

Do not write to the repository; return your verdict and end your turn.
