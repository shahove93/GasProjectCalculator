# Coordinator: три диаметра ГСВ + графика по двум образцам

Ты OpenCode/DeepSeek Flash coordinator. Пользователь запросил новую версию
СС.Расчет и однозначно подтвердил формулу: «Сначала вычитать 5 м из самых
дешёвых труб: в примере доплата 3 × 4 000 = 12 000 ₽». Это исполнение запроса,
не обсуждение возможности; дополнительных разрешений на согласованные TASK
и обычные implementation choices не проси. Не пиши продуктовый код сам.

Обязательно прочитай AGENTS.md, VISION/ARCHITECTURE/ROADMAP, APPROVALS/STATE,
MODEL-ROUTING и GSV-MIXED-DIAMETERS-PLAN.md; skills autonomous-development,
orchestration и installed guide `orca skills get orchestration`; references
routing-and-budget/review-policy/orca-integration и coordinator-loop guide
перед своим child Run. Это новый scope, но старые логические TASK и их counters
не переименовывай/не сбрасывай. Бюджеты новых bounded TASK резервируй заранее.

Workspace D:/Antigravity/GasProjectCalculator, baseline9dea625. Сейчас ветка
feature/ss-calculator-redesign, единственные dirty файлы — плановые документы,
этот brief и два новых пользовательских image references. Сохрани всё.
Создай/выбери feature/gsv-mixed-diameters от этого baseline после проверки
Git/Orca ownership. До dispatch заморозь checklist и зафиксируй TASK/risk/IDs.
Реализация отдельными настоящими Orca OpenCode workers, не native subagents.

## Scope

1. Формула и backward-compatible API — R2, reviewer Codex Sol/high. Три
   отдельных длины (`pipe_lengths`: up_to_25/from_32_to_40/diameter_57),
   строгие integer≥0 без bool, сумма метража сервером, одна база5м с исключением
   самых дешёвых первыми; тот же код в отдельном ГСВ и combined.gsv. Legacy
   length/diameter request+response без breaking changes, конфликт форм422.
   Эталоны, суммы и поля ответа — основной PLAN. Никакой клиентский total
   не должен подменять расчёт сервера.
2. UI в двух режимах и detailed billing; точное artwork по
   docs/design/header-detail-reference.jpg и footer-detail-reference.jpg.
   Тарифы2500/3500/4000, названия «до Ø25», «Ø32–40», «Ø57». Пользователь
   хочет именно объёмную светящуюся трубу с золотым вентилем и нижние
   пламя/трубу/дом/тёплое окно, не прежний упрощённый рисунок. Изображения
   — reference, не замена интерактивной шапки скриншотом. Сохрани СС.Расчет,
   круглый фирменный знак, compact800×540/min760×520. Реальные native/client
   screenshots и визуальное сравнение с refs обязательны; не маскируй overflow
   через screenshot-only JS/style workaround. Визуальная приёмка — vision
   Codex R2, поскольку OpenCode Pro ранее не принимал изображения.
3. Rebuild локального Windows installer1.1.0; preserve текущий release1.0.0
   и старые local artifact bytes. VersionInfo/installer metadata согласовать.
   Проверить packaged+installed app: new fields/mixed benchmarks, ГСН
   regressions, совместимость, САКЗ/ПК/НДС, native splash, loopback/port conflict,
   close lifecycle, RU wizard, reinstall/uninstall с сохранением user files.
   Изолированный install dir с безопасным владением scratch и сохранением
   HKCU/shortcuts; не менять обычную пользовательскую установку/её сессию.
4. README/new screenshots/docs; full integrated suite через implementer,
   independent final Codex Astra/high acceptance, FINAL-REPORT-MIXED-GSV.md,
   STATE COMPLETE только после PASS. Installer file/hash передать root.

## Ресурсы и известный infrastructure failure

Не делай background Start-Process uvicorn в обычной OpenCode shell tool:
на предыдущем этапе каждый такой tool удерживался до остановки backend,
оставляя spinner часами. Backend запускай в отдельной управляемой Orca
service terminal/session (прочитай точный help перед командой), затем в
другой короткой команде readiness check; сохраняй handle/PID/port и ownership.
Нельзя ждать завершения service process в command, который должен вернуть
startup result. User :8000 и root-owned :8138 сохраняй; выбери свой порт.
Никаких глобальных OpenCode logs/Temp — все refs/assets в workspace.

После dispatch конец хода и Orca wake, без пустых check --wait циклов.
Worker completion не PASS. При tool failure/resource limitation присылай
точное описание сразу, не выдавай spinner за прогресс. Достаточные evidence
не гонять заново. При provider exhaustion — стоп зависимой цепочки и user
решение; никаких reset-credit/смены аккаунта/оплаты/обхода.

Model routing прежний: DeepSeek Flash coordinator/implementer, Pro R1 при
достаточных capabilities, Sol/high R2 и Astra/high R3/final. Локальные scoped
commits после routed PASS разрешены. Новая публикация, push/main/Release не
входят в этот execution packet; прошлый релиз не менять и не заменять.

При вопросах и необходимых обычных разрешениях внутри scope отвечай сам,
пользователь ранее разрешил не ждать его на таких шагах. Смена требований
или архитектуры/исчерпание реальных ресурсов — точная эскалация root.
После stage PASS/BLOCKED возврат через настоящий worker_done по preamble.
