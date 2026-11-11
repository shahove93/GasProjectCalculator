# Evidence — TASK GSV-02 REGRESSION (R2, reopened)

- Baseline: `69f00f2`; ветка `feature/gsv`; workspace
  `D:/Antigravity/GasProjectCalculator`.
- Implementer: dispatch `ctx_b02d931f09b2`, task `task_efce847e1cd6`,
  opencode / `deepseek/deepseek-flash`.
- Причина переоткрытия: финальная приёмка R3 `FINAL-GSV-04` — отсутствовали
  утверждённые ARCHITECTURE отдельные Pydantic-модели ответа и `response_model`.
- Diff: `app/main.py` +39/−2; `tests/test_gsv_api.py` +84. Других изменений нет
  (`git status --short`: только эти два файла).

## Изменения

- Добавлены `GsvBreakdownResponse`, `GsnSectionResponse`,
  `CombinedCalculationResponse` (все поля int, customer_type Literal,
  is_district bool).
- `response_model=` применён к `POST /calculate/gsv` и
  `POST /calculate/combined`. `POST /calculate` не изменён.
- Добавлены тесты ключей/int-типов и наличия OpenAPI response schemas.

## Проверки

1. `.\.venv\Scripts\python.exe -m unittest tests.test_gsv_api -v`
   CWD `D:/Antigravity/GasProjectCalculator`; exit 0; `Ran 29 tests ... OK`.
   Log: `logs/GSV-02R-api.txt`.
2. `.\.venv\Scripts\python.exe -m unittest discover -s tests`
   CWD `D:/Antigravity/GasProjectCalculator`; exit 0; `Ran 134 tests ... OK`.
   Log: `logs/GSV-02R-suite.txt`.
3. `git status --short`: `M app/main.py`, `M tests/test_gsv_api.py`.
   Log: `logs/GSV-02R-status.txt`.
4. `git diff --stat`: `logs/GSV-02R-diff-stat.txt`; полный патч:
   `logs/GSV-02R-diff.patch`.
5. OpenAPI: `logs/GSV-02R-openapi.txt`; типы ответов:
   `logs/GSV-02R-response-types.txt`.

## Frozen checklist regression

D1 три Pydantic-модели ответа существуют; D2 `response_model` применён к
`/calculate/gsv` и `/calculate/combined`; D3 ключи и значения ответов прежние,
типы int; D4 `POST /calculate` не изменён; D5 тесты проверяют int-типы и
OpenAPI response schemas; D6 полный suite 134 OK и diff только в allowlist.
