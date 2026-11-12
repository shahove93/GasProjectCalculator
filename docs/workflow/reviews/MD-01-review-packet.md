# MD-01 R2 review packet (Codex gpt-6.1-sol high)

## Task

- Project TASK: **MD-01** — три длины ГСВ, серверный расчёт, legacy-совместимый API.
- Risk: **R2**; route: independent Codex `gpt-6.1-sol` high; approach/cycle A1/C1.
- Baseline: `32709a4c63904314be123f764930cfa0c59f1e9e` (ветка
  `feature/gsv-mixed-diameters`). Submission — uncommitted working-tree diff
  против baseline; reviewer файлов не меняет и не коммитит.
- Perimeter: `app/gsv_calculator.py`, `app/main.py`,
  `tests/test_gsv_calculator.py`, `tests/test_gsv_api.py`,
  `docs/workflow/evidence/MD-01-*`, `logs/MD-01-*`. Всё остальное — вне scope;
  coordinator-owned `docs/workflow/**` не считать продуктовым diff.

## Frozen checklist (verbatim from `docs/workflow/tasks/MD-01.md`)

| ID | Criterion |
| --- | --- |
| D1 | 4/0/4 → total_length 8, surcharge 12000, subtotal 72000, total 75600 |
| D2 | 2/4/3 → 9, 15500, 75500, 79275 |
| D3 | 0/5/2 → 7, 8000, 68000, 71400 |
| D4 | 3/1/1 → 5, 0, 60000, 63000 |
| D5 | 8/0/0 → 8, 7500, 67500, 70875 |
| D6 | `pipe_breakdown` — 3 позиции в порядке, included/billable/rate/surcharge; сумма == length_surcharge |
| D7 | total/length_surcharge/total_length клиента не принимаются/не подменяют сервер |
| D8 | legacy `/calculate/gsv` — ровно прежние 9 ключей, прежние суммы |
| D9 | смешение mixed+legacy, неполная пара, отсутствие формы → 422 |
| D10 | bool/float/string/negative/null/пропуск/лишний ключ → 422 |
| D11 | combined mixed 4/0/4 + ГСН10/район → 151000/7550/158550 |
| D12 | legacy combined работает без breaking changes |
| D13 | `POST /calculate` (ГСН) не изменён |
| D14 | strict integer ≥0 без bool; legacy diameter 1..57 |
| D15 | полный suite зелёный; только allowlist |
| D16 | нет commit/push/merge/deploy; scope соблюдён |

## Evidence supplied

- `docs/workflow/evidence/MD-01-evidence.md` — baseline, diff, commands/CWD/exit,
  D1–D16, negative cases, NOT_RUN.
- `docs/workflow/evidence/logs/MD-01-*.txt` — unit/API, full suite, request/
  response dump, baseline/diff/scope/status.
- Product diff: `git diff 32709a4 -- app/gsv_calculator.py app/main.py
  tests/test_gsv_calculator.py tests/test_gsv_api.py`.

## Review instructions

1. Inspect the actual final diff, evidence and any unexpected files against the
   frozen checklist; do not rerun already-documented commands when evidence is
   complete and unambiguous (review-policy reuse rule).
2. Confirm formula order `up_to_25 → from_32_to_40 → diameter_57`, one 5 m base,
   server-computed totals, strict input and legacy response shape.
3. Report each finding with ID, criterion, location, observed result,
   reproduction, expectation, severity (BLOCKER/MAJOR/MINOR/NIT) and closure
   evidence. MINOR/NIT do not fail.
4. Return exactly one verdict: **PASS**, **FAIL** (BLOCKER/MAJOR) or
   **BLOCKED**. Do not modify files, do not commit, do not mark project PASS
   yourself; end your turn after the verdict.
