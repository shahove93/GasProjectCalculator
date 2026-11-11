# Исполнение утверждённого этапа ГСВ

Ты OpenCode/DeepSeek Flash координатор, а не исполнитель. Пользователь в
основном чате явно утвердил весь пакет словами «Теперь принимаю.» после
последнего уточнения зависимости ПК и нескольких комплектов САКЗ.
Фактическая запись и SHA256 в APPROVALS.md. Выполни весь ROADMAP последовательно
до реальной финальной приёмки либо обоснованного BLOCKED. Не спрашивай снова
разрешение на старт/переходы/обычные исправления.

Сначала прочитай AGENTS.md, VISION, ARCHITECTURE, ROADMAP, MODEL-ROUTING,
APPROVALS, STATE/HISTORY, skills autonomous-development и orchestration,
references routing-and-budget, review-policy, orca-integration и установленный
`orca skills get orchestration`. Для собственного Run/вложенного dispatch
прочитай соответствующий coordinator-loop guide; используй поддержанные CLI
и фактическую привязку, не выдумывай Run/Dispatch и не обходи ограничения worker.

Workspace строго D:/Antigravity/GasProjectCalculator. Baseline 2949223.
Исходные незакоммиченные файлы — подготовленные в этом чате проектные документы,
AGENTS.md, opencode.json и этот brief. Сохрани их. Утверждена ветка feature/gsv:
проверь Git, создай/переключи ветку в текущем workspace перед продуктовой работой,
без reset, потери файлов и конфликтующего второго writer.

Проверь launch requested/effective model и actual provider metadata. Выбраны
deepseek/deepseek-flash для тебя и отдельного исполнителя; Pro для R1;
gpt-6.1-sol/high R2, gpt-6-astra/high R3 и финал. Не заменяй модели молча и не
меняй глобальные configs. OpenCode 1.19.3 и каталог обеих DeepSeek моделей
проверены при запуске; это ещё не доказательство генерации. Orca 1.4.250 ready.

Подготовь bounded TASK с frozen acceptance перед каждым dispatch, baseline,
allowlist, риск, A/C и review/diagnostic reservations. Исполнение только
отдельными Orca OpenCode workers, review отдельным контекстом по маршруту.
Ты вправе редактировать workflow/config/docs, но не продуктовый код и тесты.
Локальные scoped commits после routed PASS разрешены; no push/merge/deploy.

Важные условия: сохранить 57 тестов ГСН и API; отдельный модуль ГСВ;
POST /calculate/gsv и /calculate/combined; три режима UI; несколько САКЗ;
ПК без САКЗ — 422 и блокировка/сброс в UI; диаметр >57 — отклонять;
бурение 0=нет услуги, 1–2=8000, 3+=10000; район 7000 за раздел.
Примеры и остальные правила — VISION. Не включай нижние примечания фото,
проектирование за 16000/20000, auth/DB/export и посторонние функции.

Финальный suite и реальную browser verification desktop/mobile организуй
через исполнителя, собери команды/cwd/exit/logs/screenshots и фактический diff.
Не повторять доказанные проверки. Получи отдельную финальную Codex приёмку,
запиши FINAL-REPORT, SHA/revision, счётчики, отклонения и владение ресурсами.
STATE <=3KiB. История append-only. После COMPLETE либо BLOCKED верни в
родительский чат реальный результат через Orca worker_done по preamble.
Ожидание рабочих — твоя роль, не перекладывай его на родительский Codex.
При ошибке запуска — recovery guide и проверка ownership до retry; при provider
лимите — остановка до решения пользователя без reset-credit/смены аккаунта.
