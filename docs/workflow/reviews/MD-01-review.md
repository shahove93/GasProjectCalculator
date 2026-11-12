# MD-01 review record

## C1 — R2 Codex review

- Reviewer: Codex `gpt-6.1-sol` high, dispatch `ctx_1ce9629cc368`,
  task `task_dd90a60b5e14`, term `term_8cc909a5-f836-46db-9966-c19a4400d142`.
- Baseline `32709a4c63904314be123f764930cfa0c59f1e9e`; A1/C1; read-only.
- Verdict: **FAIL** (1 MAJOR).
- Finding **MD01-R1 (MAJOR; D9/D14)** — `app/main.py:36–38, 52–60`:
  nullable `length`/`diameter`/`pipe_lengths` + `is not None` treat an explicit
  `null` key as absent. Reproduction: valid mixed 4/0/4 + `length:null` or
  `diameter:null`; valid legacy 5/25 + `pipe_lengths:null` — standalone and
  nested `combined.gsv` return 200 instead of the required 422. Reviewer checked
  six missing cases with one bounded stdin script at the stated HEAD/diff;
  all six 200 (mixed total 75600, legacy total 63000 standalone).
- Confirmed without rerun: formula/order of the single 5 m base correct;
  server sums and legacy 9-key response preserved; D1–D8/D10–D16 confirmed
  (D14 subject to MD01-R1); suite 209 OK exit 0 accepted from logs.
- Files changed by reviewer: none. Commit by reviewer: none.
- Counters MD-01: full reviews 1, failed 1, Codex calls 1/4.

## C2 authorization

Bounded correction of the same approach: reject explicit `null`/mixed forms by
raw-key presence, add 422 regression tests on both endpoints, rerun the full
suite and update evidence. Then one repeat full R2 review (call 2/4). Product
formula/response contract must not change.

## C2 — repeat full R2 Codex review

- Implementer: OpenCode Flash `ctx_ca7386182b3a` (`task_ee2c65f2e67a`):
  raw-key `model_validator(mode="before")` in `app/main.py`; standalone and
  combined 422 regressions; evidence C2; full suite 216 OK exit 0.
- Reviewer: Codex `gpt-6.1-sol` high, dispatch `ctx_b5a2191479fe`,
  task `task_773af3e0df8b`, read-only.
- Verdict: **PASS**. **MD01-R1 CLOSED** (D9/D14, E1–E3): explicit-null/mixed
  cases return 422 on both endpoints, with closure evidence
  `tests/test_gsv_api.py:707–727,786–799` and
  `logs/MD-01-c2-request-response.txt`.
- Confirmed: D1–D8/D10–D13/D15–D16 and E4–E6; formula and legacy 9-key response
  preserved; combined total 158550; suite 216 OK accepted from C2 evidence
  without rerun; C1 FAIL preserved. Reviewer changed no files, no commit.
- Counters MD-01: full reviews 2, failed 1, Codex calls 2/4.
- **MD-01 ACCEPTED**; scoped commit owned by coordinator; next TASK MD-02.
