# История

## 2026-11-11 — обследование и проектирование

- Прочитаны autonomous-development, orchestration, routing-and-budget,
  review-policy, templates и opencode-model-selection.
- `orca skills get orchestration`: exit 0; прочитана установленная справка.
- `git status --short --branch`: `main...origin/main`, dirty отсутствовал.
  Baseline `2949223`; последние изменения — скриншоты и интерфейс ГСН.
- Прочитаны README, расчёт и API, тесты, релевантные части интерфейса.
- CWD `D:/Antigravity/GasProjectCalculator`;
  `.\.venv\Scripts\python.exe -m unittest discover -s tests`:
  exit 0, Ran 57 tests in 0.105s, OK. Есть предупреждение Starlette о
  deprecated httpx TestClient; оно не привело к падению тестов.
- Проверены локальные инструкции, конфигурация и model routing проекта
  EquipmentDocumentationRegistry. Из него перенесено предложение ролей,
  без переноса разрешений, статусов, счётчиков и продуктовой конфигурации.
- Запрошены правила/тарифы ГСВ и необходимость общего итога ГСН + ГСВ.
- Созданы проекты VISION, ARCHITECTURE, ROADMAP и workflow records.
  Продуктовый код не менялся; Orca Run/workers не запускались.

## Уточнение правил ГСВ по фотографии

Пользователь подтвердил отдельные и суммарный расчёты, источник и ограничения
его использования; затем уточнил диаметры, минимальную оплату бурения,
независимость САКЗ/ПК и район по каждому разделу. VISION дополнен формулами,
контрольными примерами и предложением целочисленного ввода; ARCHITECTURE —
общей сметой и тремя режимами; ROADMAP обновлён для утверждения.
Реализация не запущена; новых тестов и ревью не выполнялось.

## Уточнение зависимости ПК и количества САКЗ

Пользователь исправил прежнее правило: ПК допустим только с САКЗ; комплектов
САКЗ может быть несколько. VISION и ARCHITECTURE обновлены: количество ×
14 000 ₽, зависимость ПК в UI и серверной валидации, соответствующие проверки.
Добавлен пример с двумя комплектами и одним ПК: итог 96 600 ₽.
Один опциональный ПК остаётся явно обозначенным предложением на утверждение.
Код не менялся, новые проверки не запускались.

## Утверждение и подготовка запуска

Пользователь: «Теперь принимаю.» Зафиксированы hashes полного утверждённого
пакета в APPROVALS. Подготовлены локальные AGENTS.md, opencode.json и bounded
COORDINATOR-BRIEF для OpenCode/DeepSeek Flash. Продуктовый код не менялся.
Preflight: OpenCode 1.19.3, `opencode models deepseek` содержит Flash и Pro;
Orca 1.4.250 ready, текущий worktree подтверждён: D:/Antigravity/GasProjectCalculator,
baseline 2949223. `orca orchestration status` оказался неподдерживаемым
read-only discovery command; никаких мутаций эта ошибка не выполняла.

## Начало исполнения утверждённого этапа

2026-11-11: координатор OpenCode/DeepSeek Flash после preflight создал ветку
`feature/gsv` (без reset) в текущем workspace, сохранив незакоммиченные проектные
документы. Baseline `2949223`; suite 57 тестов exit 0 OK. Зафиксированы
логические TASK GSV-01 (R1), GSV-02 (R2), GSV-03 (R1), GSV-04 (R0) и финальная
приёмка R3 с маршрутами и резервами в STATE. Реализация ещё не начиналась.

## TASK GSV-01 — модуль ГСВ (R1)

2026-11-11: OpenCode/DeepSeek Flash исполнитель (dispatch `ctx_d1f4b5534011`)
создал `app/gsv_calculator.py` и `tests/test_gsv_calculator.py` (48 тестов).
Проверки: unit 48 OK, полный suite 105 OK, exit 0; изменений вне allowlist нет.
Координатор однократно сохранил логи (в отчёте не было лог-артефакта) в
`docs/workflow/evidence/logs/`. Независимый R1 OpenCode Pro (dispatch
`ctx_6f8faa93b48a`, effective DeepSeek V4.1 Pro) вернул PASS без findings по
A1–A12. Scoped commit выполнен; GSV-01 принят.

## TASK GSV-02 — API (R2): C1 FAIL и C2-коррекция evidence

2026-11-11: исполнитель OpenCode/DeepSeek Flash (dispatch `ctx_dde7ed3bb86f`)
добавил `app/main.py` (+90/−1) с `/calculate/gsv` и `/calculate/combined` и
`tests/test_gsv_api.py` (26 тестов); API 26 OK, полный suite 131 OK, exit 0.
Независимый R2 Codex (`ctx_a52e8c040396`, effective model gpt-6.1-sol/high)
подтвердил B1–B10, но вернул FAIL по B11 (MAJOR `GSV02-R2-01`): неверный baseline
`501a32b` в evidence и незакоммиченные координаторские evidence-файлы в рабочем
дереве. Продуктовых дефектов не найдено. Координатор исправил baseline на
`63dcde7`, закоммитил evidence-документы и назначил C2 — повторное полное R2-ревью
того же кода. Счётчик Codex: 1 вызов, 1 FAIL.

## TASK GSV-02 — API (R2): C2 PASS

2026-11-11: повторное полное R2-ревью Codex (dispatch `ctx_ed2dda90c5c1`,
effective gpt-6.1-sol/high, baseline HEAD `67952b1`) вернуло PASS по B1–B11:
findings нет, `GSV02-R2-01` закрыт; продуктовый diff только `app/main.py`
(+90/−1) и `tests/test_gsv_api.py`, suite 131 OK. Codex calls по TASK: 2
(1 FAIL + 1 PASS), в пределах R2-резерва. Scoped commit, GSV-02 принят.
