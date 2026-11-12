# MD-01 evidence — три длины ГСВ, серверный расчёт, legacy-API

Дата: 2026-11-12. Исполнитель: OpenCode Flash. Reviewer: Codex `gpt-6.1-sol`
high (R2). **Product verdict: NOT_REVIEWED** (исполнитель не выставляет PASS).

## Baseline и scope

- Ветка: `feature/gsv-mixed-diameters` (сохранена, не переключалась).
- Baseline HEAD (координаторский task pack): `32709a4c63904314be123f764930cfa0c59f1e9e`.
- CWD всех команд: `D:\Antigravity\GasProjectCalculator`.
- Python: `.venv\Scripts\python.exe` 3.12.4; pydantic 2.13.5, FastAPI 0.141.1.
- Commit/push/merge/deploy/release/signing: не выполнялись.

Изменённые файлы (только allowlist):

```
app/gsv_calculator.py        | 106 +++++++++++++++
app/main.py                  | 100 ++++++++++----
tests/test_gsv_api.py        | 308 ++++++++++++++++++++++++++++++
tests/test_gsv_calculator.py | 169 ++++++++++++++++++++
4 files changed, 659 insertions(+), 24 deletions(-)
```

`app/calculator.py` — zero-diff (`git diff --stat -- app/calculator.py` пуст).
`tests/test_main.py` не изменялся. Логи: `logs/MD-01-*.`

## Команды, CWD, exit

| Проверка | Команда | CWD | Exit |
| --- | --- | --- | --- |
| Unit + API | `.\.venv\Scripts\python.exe -m unittest tests.test_gsv_calculator tests.test_gsv_api -v` | `D:\Antigravity\GasProjectCalculator` | 0 (119 tests OK) |
| Full suite | `.\.venv\Scripts\python.exe -m unittest discover -s tests` | `D:\Antigravity\GasProjectCalculator` | 0 (209 tests OK) |
| Baseline suite (до изменений) | same | same | 0 (167 tests OK) |
| Request/response dump | `.\.venv\Scripts\python.exe <temp>\md01_evidence.py logs/...` | same | 0 |

Exact output — `logs/MD-01-unit-api.txt`, `logs/MD-01-full-suite.txt`,
`logs/MD-01-suite-exit.txt`, `logs/MD-01-request-response.txt`.
Baseline/diff/scope — `logs/MD-01-baseline.txt`, `MD-01-diff-stat.txt`,
`MD-01-changed-files.txt`, `MD-01-calculator-diff.txt`, `MD-01-status.txt`.

## Формула (реализация)

`remaining = 5`; для категорий в порядке `up_to_25 → from_32_to_40 →
diameter_57`: `included = min(length, remaining)`, `remaining -= included`,
`billable = length - included`, `surcharge = billable * rate`;
ставки 2500/3500/4000; `total_length = Σ length`;
`length_surcharge = Σ surcharge`. База 60000/80000, бурение, САКЗ 14000,
ПК 4000, район 7000, НДС 5% — как прежде.

## Frozen acceptance checklist

| ID | Результат | Evidence |
| --- | --- | --- |
| D1 | 4/0/4 → total_length 8, surcharge 12000, subtotal 72000, vat 3600, total 75600 | `MD-01-request-response.txt` D1; `test_d1_four_zero_four` (unit+API) |
| D2 | 2/4/3 → 9, 15500, 75500, vat 3775, total 79275 | log D2; `test_d2_two_four_three` |
| D3 | 0/5/2 → 7, 8000, 68000, vat 3400, total 71400 | log D3; `test_d3_zero_five_two` |
| D4 | 3/1/1 → 5, 0, 60000, vat 3000, total 63000 | log D4; `test_d4_three_one_one_boundary` |
| D5 | 8/0/0 → 8, 7500, 67500, vat 3375, total 70875 | log D5; `test_d5_eight_zero_zero` |
| D6 | pipe_breakdown: 3 позиции в порядке, included/billable/rate/surcharge по формуле; surcharge сумма == length_surcharge | log D6; `test_d6_breakdown_order_and_values`, `test_d6_pipe_breakdown_structure`, `test_pipe_lengths_breakdown_keeps_zero_positions` |
| D7 | client `total`/`total_length`/`length_surcharge` → 422 (extra_forbidden), не влияют на сумму | log D7; `test_d7_client_total_is_not_accepted` |
| D8 | legacy без pipe_lengths: ровно 9 прежних ключей, 8м Ø25 = 70875, 5м Ø57 = 63000 | log D8; `test_legacy_eight_meters_25_is_70875`, `test_legacy_five_meters_57_is_63000`, `test_legacy_breakdown_keys_unchanged`, существующие API exact-JSON тесты |
| D9 | mixed+legacy, неполная legacy-пара, отсутствие формы → 422 | log D9 (3 кейса); `test_d9_*` (4 теста) |
| D10 | bool/float/string/negative/null/пропуск ключа/лишний ключ → 422 | log D10 (7 кейсов); `test_d10_*` (7 тестов) |
| D11 | combined mixed 4/0/4 + ГСН10/район: gsv subtotal 79000, combined subtotal 151000, vat 7550, total 158550 | log D11; `test_d11_combined_mixed_four_zero_four` |
| D12 | legacy combined `gsv.length`/`diameter` работает, без новых ключей; 139000/6950/145950 | log D12; `test_d12_legacy_combined_still_works` |
| D13 | `POST /calculate` не изменён (app/calculator.py zero-diff), прежние суммы 105000/5250/110250 | `MD-01-calculator-diff.txt` (0 строк); log D13; `tests/test_main.py` |
| D14 | strict integer ≥0 без bool; legacy diameter 1..57 | unit + API `test_d14_*`; существующие diameter 0/58/25.5 тесты |
| D15 | full suite 209 OK, exit 0; только allowlist-файлы | `MD-01-full-suite.txt`, `MD-01-suite-exit.txt`, `MD-01-diff-stat.txt` |
| D16 | нет commit/push; изменения только в allowlist | `MD-01-baseline.txt` (HEAD без изменений), `MD-01-status.txt`, `MD-01-changed-files.txt` |

## Negative cases (exact 422)

- D7: `total: 1`, `total_length: 1`, `length_surcharge: 1` → `extra_forbidden`.
- D9: `pipe_lengths` + `length`; только `length`; ни одной формы; `pipe_lengths` + `diameter`.
- D10: `up_to_25` = `true`/`1.5`/`"4"`/`-1`/`null`; отсутствует `diameter_57`;
  лишний ключ `extra`; `pipe_lengths` не объект (список).
- D14: legacy `length` = `true`/`5.0` → 422; `diameter` 0/58 → 422.
- Combined: mixed+legacy внутри `gsv` → 422; лишний top-level `total` → 422.

## Behavior notes / риски

- Legacy-ответ сохраняет ровно прежнюю форму (9 ключей). Mixed-ответ добавляет
  `total_length` и `pipe_breakdown`; `response_model_exclude_none=True` не даёт
  legacy-ответу получить `null`-ключи. OpenAPI-схема этих полей помечает их
  nullable/optional — это осознанный компромисс единой response-модели.
- Один и тот же helper `get_gsv_mixed_breakdown` используется в
  `/calculate/gsv` и nested `gsv` в `/calculate/combined`.
- `/calculate` (ГСН) не трогался; его прежний float-вывод `110250.0/5250.0`
  остаётся baseline-поведением `app/calculator.py` и не входит в scope.

## NOT_RUN

- Реальный uvicorn/HTTP-сервер не поднимался: API проверен через
  `fastapi.testclient.TestClient` (route/модели/валидация идентичны).
- Browser/UI проверки — вне scope MD-01 (это MD-02).
- Installer/build — вне scope MD-01 (MD-03).
- Commit/push/merge/deploy/release — запрещены TASK; не выполнялись.

## Итог для координатора

Все пункты D1–D16 покрыты evidence и зелёными тестами (209 OK, exit 0).
Продуктовый PASS не выставляется: требуется независимый Codex R2 review и
решение координатора о scoped commit.

## C2 — correction of MD01-R1 (explicit null / mixed-form rejection)

Дата: 2026-11-12. Исполнитель: OpenCode Flash (C2, тот же TASK MD-01).
Основание: C1 R2 FAIL по finding **MD01-R1 (MAJOR, D9/D14)** —
`docs/workflow/reviews/MD-01-review.md`. **Product verdict: NOT_REVIEWED**
(исполнитель не выставляет PASS). C1-история выше сохранена без изменений.

### Baseline и scope C2

- Ветка: `feature/gsv-mixed-diameters` (не переключалась).
- Baseline HEAD: `32709a4c63904314be123f764930cfa0c59f1e9e` (тот же, что C1).
- CWD всех команд: `D:\Antigravity\GasProjectCalculator`.
- C2 изменил: `app/main.py` (только raw-key валидация формы ввода),
  `tests/test_gsv_api.py` (regression 422), эту evidence и
  `docs/workflow/evidence/logs/MD-01-c2-*`.
- `app/gsv_calculator.py`, формула, ставки, суммы, имена полей ответа и
  legacy-семантика в C2 не менялись (C1 diff `app/gsv_calculator.py` сохранён
  как есть).

### Correction

`GsvParameters` теперь проверяет **фактическое присутствие ключей исходной
формы** в `model_validator(mode="before")` по сырому dict, а не `is not None`
после парсинга:

- `pipe_lengths` присутствует (даже `null`) вместе с `length`/`diameter` →
  `ValueError` (mixed);
- `pipe_lengths: null` без legacy-пары → `ValueError` (`pipe_lengths не может
  быть null`);
- legacy-форма требует присутствия обоих ключей `length` и `diameter` и
  не-`null` значений; отсутствие ключа или `null` → `ValueError`;
- прежняя проверка `ПК только с САКЗ` осталась `mode="after"`.

Тот же `GsvParameters` используется в standalone `/calculate/gsv` и nested
`gsv` в `/calculate/combined`, поэтому поведение одинаково на обоих endpoints.

### Frozen C2 acceptance checklist

| ID | Результат | Evidence |
| --- | --- | --- |
| E1 | mixed + `length:null` → 422 на `/calculate/gsv` и `combined.gsv` | `MD-01-c2-request-response.txt` E1; `test_c2_mixed_with_length_null_is_422`, `test_c2_combined_mixed_with_length_null_is_422` |
| E2 | mixed + `diameter:null` → 422 на обоих endpoints | log E2; `test_c2_mixed_with_diameter_null_is_422`, `test_c2_combined_mixed_with_diameter_null_is_422` |
| E3 | legacy + `pipe_lengths:null` → 422 на обоих endpoints | log E3; `test_c2_legacy_with_pipe_lengths_null_is_422`, `test_c2_combined_legacy_with_pipe_lengths_null_is_422`; плюс `pipe_lengths:null` вместо legacy — `test_c2_pipe_lengths_null_instead_of_legacy_is_422` (log E3b) |
| E4 | Валидные mixed/legacy не изменились: mixed 4/0/4 → 75600, legacy 5/25 → 63000 (9 ключей), combined mixed → 158550 | log E4; существующие `test_d1`–`test_d5`, `test_d8`, `test_d11`, `test_d12` |
| E5 | Полный suite зелёный; изменены только allowlist-файлы | `MD-01-c2-full-suite.txt` (216 tests OK), `MD-01-c2-suite-exit.txt` (exit 0), `MD-01-c2-scope.txt` |
| E6 | Нет commit/push; C1 FAIL сохранён в evidence | `MD-01-c2-scope.txt` (HEAD `32709a4`, modified только allowlist + evidence); C1 R2 FAIL выше и в `MD-01-review.md` сохранён |

### Exact E1–E3 (оба endpoints)

Полные request/response — `logs/MD-01-c2-request-response.txt`. Ключевые
наблюдения:

- E1: mixed 4/0/4 + `"length": null` → standalone `422`,
  `detail[0].loc == ["body"]`, msg `pipe_lengths нельзя смешивать с
  length/diameter`; combined `422`, `loc == ["body","gsv"]`.
- E2: mixed 4/0/4 + `"diameter": null` → standalone `422`; combined `422`
  (same loc/msg).
- E3: legacy 5/25 + `"pipe_lengths": null` → standalone `422`; combined
  nested `gsv` `422`.
- E3b: только `"pipe_lengths": null` (без legacy-пары) → standalone `422`,
  msg `pipe_lengths не может быть null`.

### Suite / scope C2

| Проверка | Команда | CWD | Exit |
| --- | --- | --- | --- |
| Full suite (C2 diff) | `.\.venv\Scripts\python.exe -m unittest discover -s tests` | `D:\Antigravity\GasProjectCalculator` | 0 (216 tests OK) |
| Request/response dump | `.\.venv\Scripts\python.exe <temp>\md01_c2_evidence.py` | same | 0 |

`git status --short` (C2): modified `app/gsv_calculator.py`, `app/main.py`,
`tests/test_gsv_api.py`, `tests/test_gsv_calculator.py` — это C1-изменения
allowlist; C2 добавил только `app/main.py` validator + `tests/test_gsv_api.py`
+ evidence. Commit/push/merge/deploy не выполнялись; HEAD остаётся
`32709a4c63904314be123f764930cfa0c59f1e9e`.

### NOT_RUN C2 / итог

- Повторное независимое R2-ревью — за Codex (call 2/4), не исполнителем.
- Real uvicorn/HTTP, browser/UI, installer — вне scope C2.
- PASS не выставляется: требуется независимое ревью исправленного diff.

