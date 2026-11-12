# MD-01 C2 review packet (Codex gpt-6.1-sol high, call 2/4)

## Task and cycle

- Project TASK: **MD-01** — три длины ГСВ, серверный расчёт, legacy-совместимый API.
- Risk **R2**; approach **A1**, cycle **C2**; this is the repeat full R2 review
  after C1 FAIL. Reviewer — independent Codex `gpt-6.1-sol` high.
- Baseline product diff: `32709a4c63904314be123f764930cfa0c59f1e9e`,
  branch `feature/gsv-mixed-diameters`. Submission — uncommitted working tree;
  reviewer не меняет файлов и не коммитит.
- Counters before this call: full reviews 1, failed 1, Codex calls 1/4.

## C1 finding to close

**MD01-R1 (MAJOR; D9/D14)** — explicit `null` keys were treated as absent:
mixed 4/0/4 + `length:null`, mixed + `diameter:null`, legacy + `pipe_lengths:null`
returned 200 instead of 422 on `/calculate/gsv` and nested `combined.gsv`.

C2 correction: raw-key `model_validator(mode="before")` in
`app/main.py`, standalone+combined regression tests, evidence C2 section.
Closure evidence must be verified against the actual C2 diff and logs.

## Frozen checklist

Full MD-01 checklist D1–D16 (`docs/workflow/tasks/MD-01.md`) plus C2 checklist
E1–E6 (`docs/workflow/tasks/MD-01-C2.md`):

| ID | Criterion |
| --- | --- |
| D1–D8, D10–D13, D15–D16 | as in MD-01; confirm no regression from C2 |
| D9/D14 | mixed/legacy conflict, partial pair, missing form, explicit null → 422; strict ints |
| E1 | mixed + `length:null` → 422 on both endpoints |
| E2 | mixed + `diameter:null` → 422 on both endpoints |
| E3 | legacy + `pipe_lengths:null` → 422 on both endpoints |
| E4 | valid mixed sums / legacy 9-key response / combined unchanged |
| E5 | full suite green, only allowlist changed |
| E6 | no commit/push; C1 FAIL preserved in evidence |

## Evidence supplied

- `docs/workflow/evidence/MD-01-evidence.md` — C1 sections plus appended C2
  section (correction, E1–E6, exact request/response, suite/scope).
- `docs/workflow/evidence/logs/MD-01-c2-*.txt` — C2 request/response, full
  suite (216 OK exit 0), scope.
- `docs/workflow/evidence/logs/MD-01-*.txt` — original C1 suite/evidence.
- `docs/workflow/reviews/MD-01-review.md` — C1 verdict/finding.
- Actual diff: `git diff 32709a4 -- app/gsv_calculator.py app/main.py
  tests/test_gsv_calculator.py tests/test_gsv_api.py`.

## Review instructions

1. Verify MD01-R1 is actually closed in the C2 diff (raw-key presence, explicit
   null rejection on both endpoints), and that valid mixed/legacy behavior and
   the 9-key legacy response did not regress.
2. Check the whole D1–D16 + E1–E6 checklist against actual diff/evidence;
   with complete evidence do not rerun commands (reuse rule). The reviewer may
   use one bounded read-only probe only if evidence is missing/ambiguous.
3. Report findings with ID/criterion/location/observed/expected/severity/
   closure evidence. MINOR/NIT do not fail. Do not change files, do not commit.
4. Return exactly one verdict: **PASS**, **FAIL** (BLOCKER/MAJOR) or
   **BLOCKED**; end your turn after the verdict.
