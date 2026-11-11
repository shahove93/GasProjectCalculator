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

## TASK GSV-03 — интерфейс трёх режимов (R1)

2026-11-11: первая попытка исполнителя (`ctx_5a8bcf2f5789`) изменила
`frontend/index.html` (+587/−82), но зависла без worker_done; координатор
остановил её и запустил продолжение того же логического TASK (`ctx_513a316e9b89`,
parented task). Продолжение провело реальную browser verification через Orca
browser: desktop ГСН 105000/5250/110250, ГСВ 100500/5025/105525, combined
75600/70350 и 139000/6950/145950; mobile 390×844, fits=true; ПК при САКЗ 0/1/0;
ошибка diameter 58; смена режима очищает результат. 6 скриншотов и
`docs/workflow/evidence/GSV-03-browser.md`; suite 131 OK. Независимый R1
OpenCode Pro (`ctx_d7c8f160505f`, effective DeepSeek V4 Pro) вернул PASS по
C1–C8; один NIT (в combined 422 не добавляет суффикс ГСВ к GSV-полям) — backlog.
Scoped commit, GSV-03 принят.

## GSV-04 — финальная консолидация (R0)

2026-11-11: README обновлён под три режима, правила ГСВ, новые endpoints,
структуру и 131 тест. Создан `docs/workflow/evidence/FINAL-EVIDENCE.md` с
baseline `2949223`, продуктовым revision `9dc84e0`, таблицей TASK/вердиктов,
переиспользованными доказательствами (131 suite OK, 26 API, 48 unit, browser
desktop/mobile) и отклонениями. Новых продуктовых изменений нет.

## Финальная приёмка R3 — FAIL, переоткрытие TASK

2026-11-11: Codex gpt-6-astra/high (`ctx_a35b269f1f44`, HEAD `1db285e`) вернул
FAIL этапа с 4 MAJOR: FINAL-GSV-01 гонка режима (поздний ответ ГСН показывается
под ГСВ), FINAL-GSV-02 начальный режим не применяется (видны оба блока),
FINAL-GSV-03 скрытые невалидные поля блокируют submit другого режима,
FINAL-GSV-04 отсутствуют утверждённые Pydantic-модели ответа и response_model.
Подтверждены также прежние routed PASS и границы scope. Один NIT backlog.
Решение: переоткрыть GSV-02 (API, R2) для моделей ответа и GSV-03 (UI, R1) для
состояний/валидации, затем повторные routed review и финальная приёмка.
Codex final calls: 1 FAIL.

## GSV-02 regression — модели ответа (R2)

2026-11-11: переоткрытый GSV-02 исправлен исполнителем `ctx_b02d931f09b2`:
добавлены `GsvBreakdownResponse`, `GsnSectionResponse`,
`CombinedCalculationResponse` и `response_model` на `/calculate/gsv` и
`/calculate/combined`; `POST /calculate` не тронут. 29 API / 134 suite OK.
Независимый R2 Codex `ctx_ddd46cfbef19` (gpt-6.1-sol/high, baseline `5f25144`)
вернул PASS по D1–D6 без findings. Codex calls GSV-02: 3 (1 FAIL + 2 PASS).
Scoped commit.

## GSV-03 regression — исправление UI (R1)

2026-11-11: переоткрытый GSV-03 исправлен исполнителем `ctx_7f43727686c5`:
реальный старт `setMode("gsn")`, токен `activeRequest`/`isStale` против
устаревших ответов, `disabled` для скрытых групп и повторная
`updateExcavatorAvailability`/`updatePanelAvailability`, суффикс «ГСВ» в
combined 422. Browser evidence: начальный режим, гонка, скрытый diameter=58 не
блокирует ГСН, прежние суммы, mobile fits=true; 134 suite OK.
Независимый R1 OpenCode Pro `ctx_faa3f1ff8d22` (baseline `ef9fb2a`) вернул PASS
без findings. Scoped commit.

## Финальная приёмка call 2 — PASS, этап COMPLETE

2026-11-11: Codex gpt-6-astra/high (`ctx_b632e310754a`, HEAD `22ec2bc`)
вернул PASS этапа: все 4 MAJOR и NIT закрыты, прежние требования и scope
подтверждены, 57 тестов ГСН и `POST /calculate` сохранены, suite 134 OK,
API 29 OK, browser desktop/mobile и регрессии подтверждены артефактами.
Единственный NIT — README указывал 131 тест вместо 134 — исправлен в том же
docs-only изменении. Оформлены `docs/workflow/FINAL-REPORT.md` и статус
COMPLETE. Все workers освобождены; push/merge/deploy не выполнялись.

## 2026-11-11 — запуск этапа Windows installer

Пользователь явно подтвердил «Да, сделай». ARCHITECTURE/ROADMAP hashes и границы
зафиксированы в APPROVALS. Подготовлен bounded brief; docs планирования изменены,
продуктовый код нет. Orca 1.4.250 ready. До запуска — main worktree
feature/gsv, HEAD 22133a1, только намеренные изменения AGENTS/ARCHITECTURE/
README/ROADMAP. Координатор должен создать feature/windows-installer, сохранить
пользовательский сервер и пройти routed checks до финальной приёмки.

## 2026-11-11 — preflight и TASK-пакет Windows installer

Ветка `feature/windows-installer` создана от `feature/gsv` HEAD `22133a1`;
worktree текущий, все намеренные planning-правки сохранены uncommitted, второго
writer нет. Подтверждена поддержка технологий: Python 3.12.4, WebView2
157.0.4341.42, PyInstaller 6.22.3 и pywebview 6.2.1 доступны для установки в
`.venv` (pin), Inno Setup 6 portable ISCC найден в
`C:\Users\user\AppData\Local\Temp\edr-windows-build\inno\ISCC.exe`; admin не
требуется, системная установка не нужна. Пользовательский uvicorn на :8000
остаётся нетронутым. Заморожены TASK records `docs/workflow/tasks/WI-01..03`:
WI-01 packaging/window (R2, ≤4 Codex calls/3M), WI-02 installer (R2, ≤4/3M),
WI-03 docs (R0), FINAL R3 (≤6/5M). Next owner — OpenCode coordinator: dispatch
WI-01 implementer `deepseek/deepseek-flash`, затем независимый R2 review.

## 2026-11-11 — WI-01 C1 PASS и scoped commit

WI-01 реализован OpenCode Flash (`ctx_447b9d0b2a16`, `task_48f15f0c1cb3`):
PyInstaller onedir + pywebview, loopback-only выбор порта, readiness-gate,
in-process shutdown, native error dialog, hook'и `--port-file`/`--auto-close-seconds`;
12 launcher-тестов; suite 146 OK; artifact SHA256 `36A2198…77CC`. Независимый R2
Codex `gpt-6.1-sol` high (`ctx_9db90733ecc1`, `task_4980bfc17b32`) вернул **PASS**
без findings: W1–W5/W7–W9 по evidence, W10 по diff; для W6 выполнен один
разрешённый bounded recheck на собранном exe (GSN/GSV/combined 200, суммы
совпали). Reviewer не менял файлы; исходные хэши совпали. Codex calls WI-01: 1.
Scoped commit `7fab960` содержит только product/evidence/task/review records;
planning docs остаются uncommitted. Next owner — WI-02 implementer.

## 2026-11-11 — WI-02 C1 PASS и scoped commit

WI-02 реализован OpenCode Flash (`ctx_ba47202b5ed0`, `task_350718a368b4`):
per-user Inno Setup installer (`PrivilegesRequired=lowest`, HKCU), Start Menu
shortcut, optional Desktop task, silent install/uninstall, user markers.
Artifact `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`, 15 256 037
bytes, SHA256 `2973278F…428F`. Toolchain deviation: указанный portable ISCC
неполон (нет `ISCmplr.dll`); build script проверил кандидатов и использовал
локальный полный Inno Setup 6.4.1 без системной установки. Независимый R2 Codex
`gpt-6.1-sol` high (`ctx_5ec0b1f12577`, `task_57bb5b55d7aa`) — **PASS**, I1–I12
по evidence, без BLOCKER/MAJOR; один MINOR backlog `WI02-R1-F1`
(`installer/verify-runtime.ps1` cleanup path). Codex calls WI-02: 1. Scoped
commit `144a75c`. Next owner — WI-03 docs implementer.

## 2026-11-11 — WI-03 R0 PASS и scoped commit

WI-03 выполнен OpenCode Flash (`ctx_a98297a25356`, `task_1aeb67e09150`):
README получил раздел «Установка на Windows» с точным путём/размером/SHA256
артефакта, per-user каталогом, необязательным ярлыком Desktop, предупреждением
о неподписанном артефакте, localhost/close-to-stop, удалением, журналом и
ссылками на evidence; developer-раздел сохранён отдельно. R0 принят
координатором по D1–D5: artifact hash перепроверен, README соответствует
WI-01/WI-02 evidence; false claims нет. Codex calls WI-03: 0. Scoped commit
`9eaed0a`. Next owner — FINAL verification, затем Codex R3 stage acceptance.

## 2026-11-11 — FINAL verification (R0) PASS

OpenCode Flash (`ctx_ddea24ab3dd2`, `task_98720142e516`) провёл интегрированную
проверку без product change: `git diff 144a75c..9eaed0a` — только README и
evidence/review; artifact 15 256 037 байт, SHA256 `2973278F…428F` совпал;
полный suite `146 tests OK`, exit 0; user uvicorn `0.0.0.0:8000` PID 12888 не
тронут; README указывает точный artifact и сохраняет developer path. Составлен
[FINAL-WINDOWS-INSTALLER-EVIDENCE](../evidence/FINAL-WINDOWS-INSTALLER-EVIDENCE.md)
с картой frozen checklist и NOT_RUN. R0 принят координатором; Codex calls 0.
Next owner — Codex R3 stage acceptance `gpt-6-astra` high.

## 2026-11-11 — Codex R3 stage acceptance PASS, этап COMPLETE

Codex `gpt-6-astra` high (`ctx_591f058a7ec3`, `task_898d8341faad`) независимо
проверил интегрированный diff `22133a1..3d291e9` (launcher/packaging/installer/
tests, TASK/review/evidence, screenshots) и вернул **PASS** без BLOCKER/MAJOR:
scope соблюдён, VISION/расчёты/API/frontend не изменены, ARCHITECTURE/ROADMAP
SHA256 совпали с APPROVALS; clean x64 build, per-user HKCU install, Start Menu +
optional Desktop, Python-free GUI, readiness, три режима 131250/105525/145950,
127.0.0.1-only и обход занятого порта, закрытие освобождает порт, понятный
симулированный отказ, два uninstall с сохранением маркеров, developer uvicorn,
suite 146 OK, README и artifact SHA256 `2973278F…428F` подтверждены по исходным
логам. Reviewer файлов не менял, проверки повторно не запускал. Codex calls
этапа: 3 (WI-01 1, WI-02 1, stage 1); потолки не превышены. `WI02-R1-F1`
остаётся MINOR backlog. Оформлены
`docs/workflow/FINAL-REPORT-WINDOWS-INSTALLER.md`,
`docs/workflow/reviews/FINAL-STAGE-review.md` и STATE COMPLETE. Push/merge/deploy/
release не выполнялись; installer передан локально.

## 2026-11-11 — редизайн СС.Расчет одобрен

Пользователь одобрил первый visual concept. ARCHITECTURE/ROADMAP дополнены и
захэшированы в APPROVALS. Scope: компактное окно, оригинальный круглый логотип,
русский installer, splash с газовым потоком. Product code не менялся; dispatch
передан новому Orca coordinator по REDESIGN-BRIEF.md.

## 2026-11-11 — Редизайн СС.Расчет: план заморожен, ветка создана

Пользователь одобрил визуальный вариант 1; ARCHITECTURE/ROADMAP/APPROVALS
обновлены и зафиксированы. Координатор OpenCode/DeepSeek Flash создал ветку
`feature/ss-calculator-redesign` от `feature/windows-installer` `e24d806`,
сохранив незакоммиченные утверждённые документы и `assets/company-logo-source.png`.
Создан Run `run_8de25272cf66`. До dispatch заморожены TASK RD-01..RD-04,
FINAL-VERIFY и FINAL в `docs/workflow/tasks/`; маршруты: RD-01 R1 (OpenCode
Pro), RD-02/RD-03 R2 (Codex `gpt-6.1-sol` high), RD-04/FINAL-VERIFY R0
(coординатор), FINAL R3 (Codex `gpt-6-astra` high). Бюджеты Codex
зарезервированы в STATE. Product code не менялся; пользовательский сервер :8000
не затрагивался. Next owner — координатор: scoped commit документов и dispatch
RD-01 через реального Orca worker.
