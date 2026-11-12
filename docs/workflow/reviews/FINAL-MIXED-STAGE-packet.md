# FINAL-MIXED-STAGE acceptance packet (Codex gpt-6-astra high)

## Stage

- Approved stage: **2026-11-12 — три диаметра ГСВ + artwork по двум образцам +
  local installer 1.1.0**.
- Final integrated revision: `0431c0bf7babeb3c420c1b990a32fdde05d892ec`
  (`docs(workflow): integrated verification evidence (MD-05 R0 PASS)`),
  branch `feature/gsv-mixed-diameters`.
- Stage baseline: `9dea625f4a3cddd93c4f1b9df5c01d607d7023db`.
- Product commits: `1d77194` (MD-01 API), `fb080aa` (MD-02 UI/artwork),
  `d08148c` (MD-03 installer metadata), `557fe2d` (MD-04 README);
  `0431c0b` adds MD-05 evidence/accounting only.
- Reviewer: independent Codex `gpt-6-astra` high. **Read-only:** do not modify
  files, do not commit, do not rerun already-proven checks when evidence is
  complete and unambiguous (review-policy reuse rule). Budget: 1 call from
  R3 reserve ≤6 calls / 5M input tokens; this is the stage acceptance, not a
  per-TASK retry route.

## Authority and scope

`AGENTS.md`, `VISION.md` (mixed-diameter addition), `ARCHITECTURE.md`
(mixed-diameter + installer/compactness additions), `ROADMAP.md` (stage
2026-11-12), `docs/workflow/APPROVALS.md` (stage approval),
`docs/workflow/GSV-MIXED-DIAMETERS-PLAN.md`, frozen task checklists
`docs/workflow/tasks/MD-01..05.md`, `FINAL-MIXED-STAGE.md`.

## Frozen stage criteria (A1–A9)

| ID | Criterion |
| --- | --- |
| A1 | All PLAN benchmarks confirmed: 75600/79275/71400/63000/70875; combined 151000/7550/158550 |
| A2 | Single 5 m base cheapest-first; server computes totals; client total cannot override |
| A3 | Legacy length/diameter API + response and GSN intact; mixed/partial/explicit-null → 422; strict integers |
| A4 | UI three lengths + total meterage + server breakdown in GSV and combined; artwork matches both refs; `СС.Расчет` + emblem kept |
| A5 | Native 800×540/min 760×520 and mobile 390 without hidden overflow; action+total visible |
| A6 | Installer 1.1.0 built/verified; release v1.0.0 and legacy bytes unchanged; installed-app mixed/GSN/САКЗ/ПК/НДС/lifecycle/RU/reinstall/uninstall |
| A7 | README/evidence/review records consistent; full suite green (one integrated run) |
| A8 | Old RD/GSV/WI counters preserved, no budget reset; new MD-01..05 within reserves |
| A9 | No unauthorized push/merge/deploy/release/signing; scope respected |

## Evidence map

- `docs/workflow/evidence/MD-01-evidence.md` (+ C2 section), logs `MD-01-*`:
  formula/API/legacy/422, D1–D16, E1–E6; review `reviews/MD-01-review.md`
  (C1 FAIL → C2 PASS, MD01-R1 closed).
- `docs/workflow/evidence/MD-02-evidence.md`, logs `MD-02-*`, 33 screenshots
  `docs/screenshots/md-02-*`, comparisons `md-02-compare-{header,footer}.png`;
  review `reviews/MD-02-review.md` (Codex vision PASS; NIT MD02-N1 backlog).
- `docs/workflow/evidence/MD-03-evidence.md`, logs `MD-03-*`, 33 screenshots
  `docs/screenshots/md-03-*`; review `reviews/MD-03-review.md` (Codex PASS,
  no findings).
- `docs/workflow/evidence/MD-04-evidence.md`, logs `MD-04-*`, README;
  review `reviews/MD-04-review.md` (coordinator R0 PASS).
- `docs/workflow/evidence/MD-05-evidence.md`, logs `MD-05-*`;
  review `reviews/MD-05-review.md` (R0 PASS F1–F8; suite 219 OK exit 0 at
  `557fe2d`, one run).
- References: `docs/design/header-detail-reference.jpg` (1021×194),
  `footer-detail-reference.jpg` (1021×177).
- Local artifact (git-ignored): `installer/Output/GasProjectCalculator-Setup-1.1.0.exe`,
  15 293 993 B, SHA256
  `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710`.
  Unchanged: 1.0.0 `71232EE4…A7E08`; legacy `04388410…949A`,
  `2973278F…2428F`.
- Diff to inspect: `git diff 9dea625..0431c0b` (planning/docs + product),
  product subset `git diff 9dea625..0431c0b -- app frontend tests installer README.md`.

## Accounting to verify

Old logical counters preserved: GSV-01..04, WI-01..03, RD-01 1/0/0,
RD-02 1/0/1, RD-03 2/1/2, RD-05 1/0/1, RD-06 2/1/2, RD-07 R0, prior stage R3 1.
New MD counters: MD-01 2 full/1 FAIL/2 Codex; MD-02 1/0/1; MD-03 1/0/1;
MD-04 R0/0 Codex; MD-05 R0/0 Codex. No rename/reset of prior history.

## Known residual findings/risks (not blockers)

- MD02-N1 **NIT** backlog: gold valve handwheel top slightly clipped by SVG
  viewBox; required artwork elements remain distinguishable.
- Installer is unsigned (SmartScreen may warn); release v1.0.0 untouched.
- Verification environment is one Windows x64 / WebView2 / DPI 96; remote
  Release asset was not re-downloaded in MD-05.
- Combined detail scrolls inside its card on minimum size; total/action stay
  visible.

## Verdict format

Return exactly one verdict: **PASS**, **FAIL** (BLOCKER/MAJOR with finding
IDs/locations/evidence), or **BLOCKED** (unverifiable prerequisite). Map
delivered behavior to VISION/ARCHITECTURE/ROADMAP/APPROVALS and confirm or
reject A1–A9. End your turn after the verdict; the coordinator writes the
FINAL-REPORT and marks STATE COMPLETE only after PASS.
