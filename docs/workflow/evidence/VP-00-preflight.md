# VP-00 — preflight визуального продолжения (2026-11-12)

Исполнитель записи: OpenCode/DeepSeek Flash, координатор. Статус:
**IN_PROGRESS** (не product PASS).

## Authority

- `docs/workflow/VISUAL-POLISH-ASTRA-BRIEF.md`
- `docs/workflow/APPROVALS.md` — «Astra: панели, заставка и стиль установщика
  — 2026-11-12»
- `docs/workflow/VISUAL-POLISH-COORDINATOR-DISPATCH.md`
- `AGENTS.md`, `VISION.md`, `ARCHITECTURE.md`, `ROADMAP.md`,
  `docs/workflow/MODEL-ROUTING.md`
- `docs/workflow/tasks/MD-02.md`, `MD-03.md` и их review records
- `docs/workflow/reviews/MD-02-review.md`, `MD-03-review.md`,
  `FINAL-MIXED-STAGE-review.md`

## Workspace / baseline

- CWD: `D:/Antigravity/GasProjectCalculator`
- Branch: `feature/gsv-mixed-diameters`
- Baseline HEAD: `ac59d8c27ed47be07ac9b54acf8285bcab704be0`
- Uncommitted project docs (root): `VISION.md`, `ARCHITECTURE.md`,
  `ROADMAP.md`, `docs/workflow/APPROVALS.md` (modified);
  `docs/workflow/VISUAL-POLISH-ASTRA-BRIEF.md`,
  `docs/workflow/VISUAL-POLISH-COORDINATOR-DISPATCH.md`,
  `docs/design/splash-installer-reference.jpg` (untracked). Must be preserved.

## Ownership

`orca orchestration worker-list --json` checked: active workflow writer is only
the current coordinator dispatch `ctx_3cdcedf304e0` / `task_d75e7fdcd753`
(term `term_875a9df6-2025-41ec-9922-4d6f29d15e1b`). All prior
GasProjectCalculator workers are settled/released or failed without a live
writer. No second writer; no checkout/clean/reset performed.

## Reconstructed counters (not reset)

| Logical TASK | Prior approach/cycles | Prior reviews | Prior Codex calls | Next |
| --- | --- | --- | --- | --- |
| MD-02 visual | A1/C1 PASS (formal) | 1 full, 0 FAIL | 1/4 (`gpt-6.1-sol` high) | A2/C1 under new user refs; reserve 1 full R2 vision review; call 2/4 |
| MD-03 installer | A1/C1 PASS | 1 full, 0 FAIL | 1/4 (`gpt-6.1-sol` high) | A2/C1 for 1.2.0/branding; reserve 1 full R2 review; call 2/4 |
| FINAL-MIXED-STAGE | A1/C1 PASS | 1 stage acceptance | 1 (`gpt-6-astra` high) | New separate stage acceptance for this visual stage; implementer context excluded |

Rationale: user explicitly rejected the A1 visual similarity and supplied new
references/scope; this is a materially different approach (A2), not a reset of
the logical TASK, its history or its spend. Previous NIT MD02-N1 (clipped
handwheel) is to be closed by the new geometry; it never triggered a correction
cycle before.

Reservations before dispatch:

- MD-02/A2/C1: 1 full R2 vision review, model `gpt-6.1-sol` high.
- MD-03/A2/C1: 1 full R2 review, model `gpt-6.1-sol` high.
- Final stage: 1 Codex `gpt-6-astra` high acceptance in a separate reviewer
  context (not the implementer).
- Full integrated test suite: once by OpenCode/coordinator on the final
  revision (per brief), not simulated.

## Old installer bytes preserved before any build

Recorded `Get-FileHash -Algorithm SHA256` (2026-11-12, before VP-02 build):

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| `installer/Output/GasProjectCalculator-Setup-1.0.0.exe` | 15 286 980 | `71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08` |
| `installer/Output/GasProjectCalculator-Setup-1.1.0.exe` | 15 293 993 | `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710` |
| `installer/Output/legacy/GasProjectCalculator-Setup-1.0.0-pre-compact.exe` | 15 273 647 | `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A` |
| `installer/Output/legacy/GasProjectCalculator-Setup-1.0.0-previous-stage.exe` | 15 256 037 | `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F` |

## References inspected (vision)

- `docs/design/header-detail-reference.jpg` — dark navy header; muted teal
  pipe, metal couplings, wide horizontal gold oval handwheel on a stem/valve,
  single pipe with an elbow; no dashed fill, no extra branch, restrained glow.
- `docs/design/footer-detail-reference.jpg` — light strip; thin contour pipe
  with couplings, blue flame at left, complete house with warm 4-pane window
  at right, tree/bushes, soft ground line.
- `docs/design/splash-installer-reference.jpg` — dark navy gradient; title in
  upper third with narrow teal accent, «Подготавливаем расчёт…», large
  continuous pipe with valve at left, elbow down, glowing flow to contour house
  at right, warm 4-pane window, soft hills; no gray photo frame.
- Prior `docs/screenshots/md-02-compare-header.png`,
  `md-02-compare-footer.png`, `md-03-native-splash.png` — show the rejected
  A1 differences: dashed/neon pipe, extra branch, clipped/small handwheel,
  dark massive footer pipe, clipped house, emblem-centered splash without the
  reference composition.

## Next

Dispatch VP-01 to a real Orca Codex `gpt-6-astra` / high worker in the current
workspace, then end the turn and wait for Orca wake (no polling).
