# Восстановление после зависания координатора

Пользователь явно разрешил: «Разрешаю» на остановку зависшего координатора
и возобновление той же задачи новым OpenCode coordinator. Это infrastructure
recovery, не новый scope/approach и не обход provider usage limit. Отказа
провайдера по лимиту не установлено. Все старые TASK/review counters сохраняются.

Original parent Run run_8e5d92ad57c7, logical coordinator TASK
task_82bfbabba91b, stopped Dispatch ctx_2af249de822a. Stop receipt:
state=stopped, processAction=closed_agent_terminal, ptyKilled=true;
последующий worker-show: process_stopped/exited. Старый coordinator не работает.

Child execution Run: run_8de25272cf66. RD-01 task_527858dbf289,
attempts ctx_eeb0ad4b83cb и ctx_66fd60974141 остановлены, exited.
Нет активного product writer. Перед продолжением сверить worker-list и
поддержанную передачу/привязку child Run через installed guide и CLI help.
Не создавать новый Run/TASK для обхода владения или обнуления counters.

Ветка feature/ss-calculator-redesign, HEAD bd91c77; dirty frontend/index.html,
tests/test_main.py; untracked assets/, frontend/assets/, tests/test_frontend_redesign.py,
RD-01-* logs. Это работа текущего TASK, не повод спрашивать пользователя или
обнулять её. Сначала изучить текущий diff и продолжить оставшиеся критерии.
RD-01 ещё NOT_REVIEWED; A1/C1, полных acceptance review ещё не было.
Точный расход инфраструктурных попыток восстановить из authoritative evidence.

Уже доказано: docs/workflow/evidence/logs/RD-01-suite.txt — 152 tests, OK,
EXIT=0; не повторять без изменения кода/неоднозначности evidence.
Осталось RD-01: реальные browser screenshots, 3 viewport, benchmark расчёты,
422 и reduced-motion, evidence pack, отдельный OpenCode Pro R1 review.
Далее RD-02 window+splash, RD-03 RU installer, RD-04 docs, финал по frozen TASK.

Пользовательский server :8000 (PID 12888) не трогать. Временный проверочный
server :8123 запущен старым coordinator PID 22988 / child 24388; сначала
проверить актуальную identity/listener и переиспользовать при возможности.
Не повторять background startup в унаследованных pipe. Использовать hidden
detached launch с workspace logs, ограничивать время каждой команды. Если
неизвестно, завис ли provider/tool, не выдавать spinner/liveness за прогресс.

Не читать global OpenCode logs или Temp. Лого workspace source уже есть.
Не выполнять product implementation/браузерную проверку самим координатором:
передать scoped remainder отдельному OpenCode worker. Не ждать в пустых циклах;
после dispatch завершать ход и принимать Orca wake. Не повторять долгое
изучение общего help; читать help только конкретной нужной команды.

До dispatch зафиксировать текущие IDs/ownership/counters. После подлинного
результата — routed review и только затем переход. Если child Run невозможно
безопасно восстановить — вернуть точную ошибку, не зависать молча. Подтверждение
восстановления — новый Dispatch исполнителя, затем артефакты, не общий статус.

Сохранять модель DeepSeek Flash для coordinator/implementer и Pro для R1;
не менять глобальные настройки/permissions/учётные записи. Кодовые review R2
Sol/high, R3/final Astra/high; прежние ограничения push/merge/release сохраняются.
