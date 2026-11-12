# FINAL-MIXED-STAGE review record

## Final stage acceptance — PASS

- Reviewer: independent Codex `gpt-6-astra` high, dispatch
  `ctx_fdefaa501548`, task `task_e65cd54e7145`, read-only.
- Final integrated revision: `0431c0bf7babeb3c420c1b990a32fdde05d892ec`;
  product revision `557fe2d`; stage baseline `9dea625`.
- Verdict: **PASS**, A1–A9 confirmed.

### Confirmed

- **A1:** benchmarks 75600/79275/71400/63000/70875; combined
  151000/7550/158550.
- **A2:** single 5 m base cheapest-first; server-computed totals; no client
  override.
- **A3:** legacy length/diameter API/response and GSN intact; strict
  mixed/partial/explicit-null validation → 422.
- **A4:** three-length UI + total meterage + server breakdown in GSV/combined;
  both reference motifs; `СС.Расчет` and round emblem preserved.
- **A5:** native action/total visible at target/min; mobile 390 accessible by
  normal vertical scroll, no hidden horizontal overflow.
- **A6:** local installer chain, installed runtime/lifecycle/RU wizard/
  reinstall/uninstall; legacy hashes unchanged.
- **A7:** README/evidence consistency; integrated suite `219 OK` at `557fe2d`
  with only docs after it.
- **A8:** old counters preserved; MD counts 2/1/2, 1/0/1, 1/0/1, R0, R0.
- **A9:** scoped changes; no evidence of unauthorized publication/signing/
  push/merge/deploy.

### Findings and residual limits

- **FINALMD-N1 (MINOR, editorial):** stale STATE lines about unchanged product
  code/next commit and review-packet screenshot counts 36/35 vs the MD-05
  inventory of 66. Non-blocking; fixed by the coordinator during finalization
  (STATE now COMPLETE; packet counts corrected to 33 MD-02 + 33 MD-03 = 66).
- **MD02-N1 (NIT, backlog):** gold valve handwheel top slightly clipped by SVG
  viewBox; required artwork elements remain distinguishable.
- Unsigned local installer (SmartScreen may warn); release v1.0.0 untouched.
- One Windows x64 / WebView2 / DPI 96 environment; remote Release asset not
  re-downloaded in MD-05.
- Combined detail scrolls inside its card at minimum size; total/action stay
  visible.

### Accounting

This stage: MD-01 2 Codex calls, MD-02 1, MD-03 1, MD-04 0, MD-05 0,
FINAL-MIXED 1; R3 reserve 1/6 used. No new implementation/review cycle was
required after the final PASS. Reviewer changed no files and made no commit.
