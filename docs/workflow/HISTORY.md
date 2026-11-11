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

## Пользователь разрешил восстановление координатора

Ответ «Разрешаю» на конкретную остановку зависшего coordinator и запуск новой
попытки той же задачи. ctx_2af249de822a worker-stop: stopped,
closed_agent_terminal/ptyKilled=true; worker-show process_stopped/exited.
Старый coordinator и обе остановленные RD-01 попытки ctx_66fd60974141,
ctx_eeb0ad4b83cb освобождены worker-release= released. Файлы и прежние counters
сохранены. Snapshot в evidence/REDESIGN-state-pre-recovery.md;
REDESIGN-RECOVERY.md задаёт remaining work и handoff. Старый suite evidence
152 tests OK, EXIT=0 не повторять без оснований. Новый coordinator возобновляет
тот же task_82bfbabba91b, без нового logical TASK/Run/approach.

## 2026-11-11 — RD-01: координатор привязан к child Run и продолжение dispatch

Новый OpenCode/DeepSeek Flash координатор прочитал APPROVALS, STATE, VISION,
ARCHITECTURE, ROADMAP, MODEL-ROUTING, recovery/handoff, skills и references,
`orca skills get orchestration` и coordinator-loop; привязался к существующему
child Run `run_8de25272cf66` через `run-use` (не новый Run/TASK). Ветка
`feature/ss-calculator-redesign` HEAD `bd91c77`; dirty RD-01 работа сохранена.
Запущен реальный Orca worker продолжения того же logical TASK: dispatch
`ctx_6bc08bbe6a19`, `task_527858dbf289`, agent opencode, requested model
`deepseek/deepseek-flash`, term_31df04d3. A1/C1, verdict NOT_REVIEWED; прежние
счётчики не сброшены. Задача worker: browser verification трёх viewport,
три эталонных режима, 422, reduced motion, network/asset provenance, полный
`RD-01-evidence.md`; без commit и без project PASS. :8000 PID12888 не тронут;
добавлять ничего вне allowlist нельзя. Next owner — дождаться worker_done и
отправить пакет независимому OpenCode Pro R1 review.

По запросу родительского координатора сверено владение: `worker-release`
для ctx_66fd60974141 и ctx_eeb0ad4b83cb вернул already_released
(terminal captured, processAction none) — активного старого writer нет.
Факт по ресурсам: :8123 сейчас не слушает (listener только :8000 PID12888,
не тронут), поэтому worker запускает собственный диагностический backend на
свободном порту ≠8000 с логами в workspace. Handoff подтверждён родителю
новым Dispatch ctx_6bc08bbe6a19; новый logical TASK/Run не создавался,
A1/C1 и counters сохранены.

## 2026-11-11 — RD-01: реализация/evidence завершены, запущен независимый R1 review

OpenCode/DeepSeek Flash реализатор `ctx_6bc08bbe6a19` завершил `worker_done
succeeded`, сохранив реализацию прежних попыток и закрыв browser-remainder на
диагностическом backend `127.0.0.1:8138` (собственный сервер не поднимал;
случайный :8137 остановлен; :8000 PID12888 не тронут). Результаты: три режима
125000/6250/131250, 100500/5025/105525, 139000/6950/145950; viewport
1050×740/860×620/390×844 без horizontal scroll; 422 видим; reduced motion;
внешних ресурсов нет; `app/` не изменён; suite reuse 152 OK EXIT=0; 12 реальных
скриншотов и `RD-01-evidence.md`. Emblem provenance: source SHA256
`86B79EFD…98AB`, product asset `C3DCBA6D…F4DC`, 146×146, без wordmark;
остаточный риск по корпоративным правам зафиксирован без выдуманной лицензии.
Worker освобождён (released). Для независимой приёмки R1 запущен отдельный
OpenCode Pro reviewer `ctx_edd1a2ae92e9` (`task_696412840fc3`, term_863f5dff).
A1/C1, полных review пока 0/2; counters не сброшены. Next owner — дождаться
вердикта reviewer и сохранить review record; PASS→scoped commit RD-01.

## 2026-11-11 — RD-01 R1 PASS (независимый OpenCode Pro)

Независимый OpenCode Pro reviewer `ctx_edd1a2ae92e9` (`task_696412840fc3`,
effective `deepseek/deepseek-v4-pro`, term_863f5dff) вернул **PASS** по
R1-1..R1-11 без BLOCKER/MAJOR; файлов не менял, повторных прогонов не делал
(evidence полный, reuse rule). Подтверждены: заголовок/подпись, круглая
эмблема 146×146 без wordmark с исходным фиолетовым, тёмно-синяя шапка/pipe/
teal, три viewport без horizontal scroll, три эталонных режима
125000/6250/131250, 100500/5025/105525, 139000/6950/145950, очистка режимов
и видимый 422, отсутствие внешних ресурсов, `app/` zero diff, suite 152 OK,
reduced motion. Findings только NIT: F1 stale git listing двух layout-PNG,
F2 mojibake в 422 JSON, F3 дублирующиеся примечания в browser log — backlog,
не блокируют. Остаточный риск по правам на эмблему зафиксирован. R1 full
reviews 1/2, failed 0, Codex calls 0. Review record:
`docs/workflow/reviews/RD-01-review.md`. Reviewer освобождён. Next owner —
scoped commit RD-01 и dispatch RD-02 (R2, Codex sol high).

RD-01 закоммичен scoped-коммитом `041b13d` (32 файла: presentation
`frontend/index.html`, эмблема, статические тесты, source asset, 12 реальных
скриншотов, evidence/logs, recovery/STATE/HISTORY, review record); push/merge
не выполнялись. Для RD-02 (native window 1050×740/min 860×620, branding
`СС.Расчет`, локальная русская splash-анимация без сети и искусственной
задержки, reduced motion, русские ошибки, loopback lifecycle) заморожен
checklist `docs/workflow/tasks/RD-02.md`, baseline `041b13d`, A1/C1, R2,
резерв Codex ≤4 вызовов/3M. Запущен implementer `ctx_b89935976cc0`
(`task_e59117ab6038`, OpenCode Flash, term_4c6fe15a). Next owner — дождаться
worker_done и отправить пакет на независимый Codex R2 review.

## 2026-11-11 — RD-02 реализация завершена, запущен Codex R2 review

OpenCode/DeepSeek Flash implementer `ctx_b89935976cc0` (`task_e59117ab6038`)
завершил RD-02 на baseline `041b13d`: `APP_TITLE` ровно `СС.Расчет`, окно
1050×740/min 860×620, локальная frameless русская splash-заставка 520×320 с
SVG-потоком газа к дому, lifecycle «splash shown → backend start → ready →
main created → splash closed → main shown», reduced motion, отсутствие сети,
русская ошибка с остановкой backend, loopback/port-skip/close-stop. Evidence
`RD-02-evidence.md`, 4 реальных native-скриншота, полный suite 163 OK EXIT=0;
`app/main.py`, calculators и функциональный `frontend/index.html` не изменены;
:8000/:8138 не тронуты. Implementer освобождён. Запущен независимый R2
Codex reviewer `ctx_66502b51d130` (`task_f3daf8be58f6`, `gpt-6.1-sol` high,
term_55b493f1) с frozen R2-1..R2-11. Codex calls RD-02: 0 пока; counters
не сброшены. Next owner — дождаться вердикта; PASS→scoped commit RD-02.

## 2026-11-11 — RD-02 R2 PASS (Codex)

Независимый Codex R2 reviewer `ctx_66502b51d130` (`task_f3daf8be58f6`,
`gpt-6.1-sol` high, term_55b493f1) вернул **PASS** по R2-1..R2-11 без
BLOCKER/MAJOR/MINOR/NIT и без finding IDs. Проверен фактический diff от
`041b13d` при HEAD `2703e83`, исходные логи, 4 реальных native-снимка, SHA256
launcher/splash/снимков; файлов ревьюер не менял, rerun=0 (evidence reuse).
Подтверждены title `СС.Расчет`, 1050×740/min 860×620, реальная локальная
русская splash-заставка до readiness, порядок ready→hidden main→splash closed→
main shown, readiness 0,75 s и main через 107 мс без искусственной задержки,
reduced motion, file-only/no-network, русская ошибка с остановкой backend,
busy 8000→127.0.0.1:8001 и освобождение порта, suite 163 OK, отсутствие
изменений API/calculators/functional `frontend/index.html`/installer/user data.
Остаточные ограничения: native 96 DPI, reduced motion через эмуляцию, ранний
диагностический failure, WebView2 ~0,57 s, packaged splash — в RD-03; права на
эмблему — ранее зафиксированный риск. Codex calls RD-02: 1; R2 full reviews 1,
failed 0. Reviewer освобождён. Next owner — scoped commit RD-02 и dispatch RD-03.

RD-02 закоммичен scoped-коммитом `32e77b1` (launcher/resources/spec/tests,
`frontend/splash.html`, 4 native-снимка, evidence/logs, review, STATE/HISTORY).
Для RD-03 (полностью русский Inno Setup, ярлык `СС.Расчет`, publisher
`ООО «Северное сияние»`, per-user без UAC, x64, optional Desktop, reinstall/
uninstall с сохранением user files, пересборка packaged app+installer,
SHA256, реальные скриншоты) заморожен checklist `docs/workflow/tasks/RD-03.md`,
baseline `32e77b1`, A1/C1, R2, резерв Codex ≤4/3M. Запущен implementer
`ctx_e4488f57f75b` (`task_52e983ff51d0`, OpenCode Flash, term_e70ef6bf);
поручено сохранить прежний installer artifact, использовать проверенный
локальный Inno Setup 6.4.1 и не трогать :8000/:8138. Next owner — дождаться
worker_done и отправить пакет на Codex R2 review.

## 2026-11-11 — RD-03 реализация завершена, запущен Codex R2 review

OpenCode/DeepSeek Flash implementer `ctx_e4488f57f75b` (`task_52e983ff51d0`)
завершил RD-03 на baseline `32e77b1`: русский Inno Setup (`AppName`/ярлыки
`СС.Расчет`, publisher `ООО «Северное сияние»`, `Languages\Russian.isl`,
`ShowLanguageDialog=no`, `PrivilegesRequired=lowest`, x64compatible, Start Menu
всегда + optional Desktop unchecked, русский uninstaller), обновлённые
verify-скрипты, пересобран packaged app и installer. Артефакт
`installer/Output/GasProjectCalculator-Setup-1.0.0.exe`, 15 273 647 bytes,
SHA256 `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`;
прежний installer сохранён в `installer/Output/legacy/`. Проверены: clean
silent install без desktop, reinstall с desktop, HKCU/no-admin, Python-free
GUI, splash/readiness, три режима 131250/105525/145950, loopback/port-conflict
8123→8124/close-free, GUI uninstall с сохранением markers, suite 163 OK exit 0;
9 реальных скриншотов; :8000/:8138 не тронуты. NOT_RUN: скриншот setup-error
dialog (процесс остановлен без residue) — оценка за reviewer. Implementer
освобождён. Запущен независимый R2 Codex reviewer `ctx_0f37bf720947`
(`task_70cf5390b9b4`, `gpt-6.1-sol` high, term_96fdf92a), Codex calls RD-03: 0.
Next owner — дождаться вердикта; PASS→scoped commit RD-03.

## 2026-11-11 — RD-03 C1 FAIL (Codex R2), назначена C2

Независимый Codex R2 reviewer `ctx_0f37bf720947` (`task_70cf5390b9b4`,
`gpt-6.1-sol` high) вернул **FAIL** по одному finding: RD03-F01 MAJOR (R3-2) —
нет реального скриншота ошибки самого Setup; попытка
`/DIR=C:\Windows\System32\RD03-Forbidden` не наблюдала error-dialog. Остальные
R3-1/R3-3..R3-13 PASS; артефакт независимо пересчитан (15 273 647 bytes,
SHA256 `043884…949A`), Authenticode NotSigned, legacy artifact сохранён,
неожиданных продуктовых изменений нет. Ревьюер файлов не менял, rerun=0;
освобождён. Codex calls RD-03: 1/4; R2 full reviews 1/2; failed reviews 1.
Review record: `docs/workflow/reviews/RD-03-review.md`. Назначена C2: одна
bounded коррекция только setup-error evidence (реальный русский error dialog
именно этого артефакта + cleanup proof), затем одно повторное полное R2-ревью
того же TASK; остальные доказательства сохраняются, новый подход не требуется.
Next owner — dispatch C2 implementer.

Запущен C2 implementer `ctx_2b97c2f59827` (`task_c7fab3f54056`, OpenCode Flash,
term_9cd3fefe): только реальный русский Setup-error screenshot именно артефакта
с SHA256 `043884…949A`, команда/CWD/revision/exit, cleanup proof, обновление
R3-2/NOT_RUN в evidence; без пересборки, коммитов и изменений других
доказательств. :8000/:8138 не трогать. Next owner — дождаться worker_done,
затем повторное полное Codex R2-ревью (call 2/4).

## 2026-11-11 — RD-03 C2: setup-error evidence закрыт, запущено повторное R2

C2 implementer `ctx_2b97c2f59827` (`task_c7fab3f54056`) закрыл RD03-F01:
запустил ровно тот артефакт (SHA256 `043884…949A`) в GUI с
`/DIR=C:\Windows\System32\RD03-Forbidden`, нажал Далее×3 → Установить, получил
настоящий русский Inno Setup error-dialog «Невозможно создать папку …
Ошибка 5: Отказано в доступе.» и второй «Установка не была завершена…»;
exit 4. Реальный native-снимок `docs/screenshots/rd-03-setup-error.png`, логи
`RD-03-setup-error*.txt`, cleanup proof (нет install dir/блокера/HKCU/ярлыков),
hash артефакта не изменился, :8000/:8138 целы, продукт не менялся. R3-2
дополнен в evidence. Implementer освобождён. Запущено одно повторное полное
R2-ревью Codex `ctx_a92d1fc9a28c` (`task_c20c237aec63`, `gpt-6.1-sol` high,
term_6d8c9eb6): проверить закрытие RD03-F01 и весь frozen checklist; Codex
call RD-03 2/4. Next owner — дождаться вердикта; PASS→scoped commit RD-03.

## 2026-11-11 — RD-03 C2 PASS, RD03-F01 CLOSED

Повторное полное R2-ревью Codex `ctx_a92d1fc9a28c` (`task_c20c237aec63`,
`gpt-6.1-sol` high, term_6d8c9eb6) вернуло **PASS**; RD03-F01 **CLOSED**.
Ревьюер файлов не менял, rerun=0; проверил 10 native-снимков, raw logs,
бинарники и hash. C2 setup-error: exact installer с
`/DIR=C:\Windows\System32\RD03-Forbidden`, реальные Далее/Установить, русские
диалоги «Невозможно создать папку … Ошибка 5: Отказано в доступе» и
«Установка не была завершена…», exit 4; `rd-03-setup-error.png` 322×179,
SHA256 `02E78874…267C`; cleanup без install dir/HKCU/ярлыков/блокера,
:8000/:8138 целы, artifact hash не изменился. Все R3-1..R3-13 повторно PASS.
Артефакт: 15 273 647 bytes, SHA256 `043884…949A`; legacy `2973278F…428F`;
NotSigned. Счётчики RD-03: full reviews 2/2, failed 1, Codex calls 2/4.
Review record обновлён (`docs/workflow/reviews/RD-03-review.md`); reviewer
освобождён. RD-03 **ACCEPTED**; next owner — scoped commit RD-03, затем RD-04
(R0 README), FINAL-VERIFY (R0) и Codex R3 stage acceptance.

RD-03 закоммичен scoped-коммитом `ffe17fb` (4 installer-файла, evidence/logs,
10 снимков, C1/C2 review record, STATE/HISTORY); артефакт остаётся локальным
git-ignored. Для RD-04 (README под `СС.Расчет`, exact artifact path/size/
SHA256, RU install/uninstall, сохранение user files, окно/заставка/reduced
motion, три режима без изменений, ссылки на реальные скриншоты, без
claims о signing/publication/telemetry) запущен OpenCode Flash
`ctx_d59e441d9384` (`task_cb670182c32f`, term_d9ede751); приёмка — R0
coordinator checklist. Next owner — дождаться worker_done, принять R0 и
закоммитить, затем FINAL-VERIFY (R0) и Codex R3 stage acceptance.

## 2026-11-11 — RD-04 R0 PASS

OpenCode Flash `ctx_d59e441d9384` (`task_cb670182c32f`) обновил README под
`СС.Расчет`: бренд/подпись, exact local artifact path/size 15 273 647/SHA256
`043884…949A`, RU per-user installer + Start Menu/optional Desktop, русский
uninstall с сохранением `%LOCALAPPDATA%\GasProjectCalculator`, окно 1050×740
(min 860×620), заставка/reduced motion, три режима и developer-путь без
изменений, реальные ссылки на RD-01/RD-02/RD-03 screenshots/evidence/reviews,
локальная неподписанная сборка без claims о публикации/телеметрии/cloud.
Изменён только `README.md` (+85/−30) и `RD-04-evidence.md`. Координатор
принял R0 по R4-1..R4-7: artifact hash/size сверены, все относительные ссылки
существуют (MISSING=0), false claims нет. Review record
`docs/workflow/reviews/RD-04-review.md`; Codex calls 0. Worker освобождён.
Next owner — scoped commit README, затем FINAL-VERIFY (R0), Codex R3 stage
acceptance и FINAL-REPORT.

RD-04 закоммичен scoped-коммитом `c72979a` (README, RD-04 evidence/review,
STATE/HISTORY). Запущен отдельный verifier FINAL-VERIFY (R0)
`ctx_1cb546ad517e` (`task_e08ed7f8ac7b`, OpenCode Flash, term_2f6a9d9f):
проверить интегрированный diff `e24d806..c72979a`, один полный suite, artifact
path/size/SHA256 `043884…949A`, наличие скриншотов/документации, reuse
RD-01..RD-03 evidence, отсутствие неожиданных файлов и неизменность расчётов/
API; записать `RD-FINAL-evidence.md`/logs. Next owner — принять R0, затем
Codex R3 stage acceptance.
