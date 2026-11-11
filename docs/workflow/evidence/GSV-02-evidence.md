# Evidence — TASK GSV-02 (R2, A1/C1, corrected for C2)

- Baseline: HEAD на старте C2-ревью (все координаторские документы и evidence
  закоммичены); ветка `feature/gsv`; workspace
  `D:/Antigravity/GasProjectCalculator`. Проверяемый продуктовый diff —
  `git diff HEAD` плюс untracked `tests/test_gsv_api.py`.
- C1-ревью Codex выявило MAJOR `GSV02-R2-01`: в evidence был указан неверный
  baseline `501a32b`, а на момент проверки в дереве были ещё не закоммиченные
  координаторские evidence-файлы. Это административное расхождение, не дефект
  продукта. Для C2 baseline исправлен, координаторские evidence-файлы
  закоммичены до повторного ревью; исполняемый diff остаётся прежним.
- Implementer: Orca dispatch `ctx_dde7ed3bb86f`, task `task_6ffa0aed9f78`,
  agent opencode, requested model `deepseek/deepseek-flash`.
- Diff продукта (`git diff HEAD`): `app/main.py` +90/−1 (новые модели,
  `/calculate/gsv`, `/calculate/combined`; `/calculate` не изменён); новый
  `tests/test_gsv_api.py` (26 тестов). Координаторские evidence-документы входят
  в baseline-коммит и не являются изменениями исполнителя. Ожидаемый
  `git status --short` на момент C2-ревью: только `M app/main.py` и
  `?? tests/test_gsv_api.py`.

## Выполненные проверки (логи исполнителя, сохранённые копии)

1. `.\.venv\Scripts\python.exe -m unittest tests.test_gsv_api -v`
   CWD `D:/Antigravity/GasProjectCalculator`; exit 0; `Ran 26 tests ... OK`.
   Log: `docs/workflow/evidence/logs/GSV-02-api.txt`.
2. `.\.venv\Scripts\python.exe -m unittest discover -s tests`
   CWD `D:/Antigravity/GasProjectCalculator`; exit 0; `Ran 131 tests ... OK`.
   Log: `docs/workflow/evidence/logs/GSV-02-suite.txt`.
3. `git status --short` / `git diff --stat`:
   `docs/workflow/evidence/logs/GSV-02-status.txt`,
   `docs/workflow/evidence/logs/GSV-02-diff-stat.txt`.

## Отчёт исполнителя (inline)

Добавлены строгие Pydantic-модели и endpoints `/calculate/gsv`,
`/calculate/combined` с валидацией (diameter 1..57, неотрицательные int, strict
bool, ПК только с САКЗ, 422 без частичного 200 для combined), используются
`get_gsv_breakdown`, `get_breakdown`, `calculate_vat` без дублирования формул;
`/calculate` и `calculator.py` не менялись.

## Frozen checklist GSV-02

B1 контракт POST /calculate сохранён; B2 /calculate/gsv возвращает точные поля
breakdown; B3 diameter 1..57, 0/58 → 422; B4 length/бурение/САКЗ/ПК/район
соответствуют VISION; B5 ПК без САКЗ → 422; B6 структура combined содержит gsn,
gsv, customer_type, is_district, subtotal, vat, total; B7 общие тип и район,
независимые параметры разделов; B8 ошибка любого раздела → 422 без частичного
200; B9 общие subtotal/vat/total равны суммам разделов; B10 пять GSV-примеров и
общий пример 139000/6950/145950 точны; B11 полный suite 131 OK, изменений вне
allowlist нет.

## C2 review result

Codex R2 C2 (dispatch `ctx_ed2dda90c5c1`, gpt-6.1-sol/high, baseline HEAD
`67952b1`): PASS по B1–B11, findings отсутствуют, `GSV02-R2-01` закрыт.
Подтверждены diff только `app/main.py` (+90/−1) и `tests/test_gsv_api.py`,
suite 131 OK, формулы не дублируются, `/calculate` не изменён.
