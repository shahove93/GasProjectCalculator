# GasProjectCalculator: разработка через Orca

## Приоритетное исключение: визуальная доработка 1.2.0

По прямому решению пользователя 2026-11-12 визуальный scope из
`docs/workflow/VISUAL-POLISH-ASTRA-BRIEF.md` (верх/низ приложения, заставка,
дизайнерские улучшения и оформление установщика) реализует **только настоящий
Orca Codex worker с моделью `gpt-6-astra`, reasoning effort `high`**.
Это правило имеет приоритет над общими указаниями ниже о том, что код пишет
OpenCode/DeepSeek Flash, и над прежними TASK/модельными конфигурациями.

OpenCode/DeepSeek Flash в этом этапе только координирует документы, очередь,
диспатч, сбор доказательств и запуск проверок; он не пишет и не исправляет
продуктовый код, SVG/CSS, splash или installer branding. Все такие исправления
также возвращаются Astra. Не передавать их Flash/Pro или другой модели.
Перед продуктовой работой координатор обязан проверить и записать реальные
requested/effective `agent=codex`, `model=gpt-6-astra`, `effort=high` из Orca
launch receipt/worker-show. Одного упоминания Astra в prompt недостаточно.
Если выбранная модель не запускается/не подтверждается — BLOCKED с точной
ошибкой, без молчаливой замены. Не менять глобальные конфиги и аккаунты.

Независимый vision review выполняет отдельный Codex Sol/high, финальную
приёмку — отдельный Codex **gpt-6.1-sol/high** reviewer по дополнительному
решению пользователя «Давай да, поручим Sol»; исполнитель себя не принимает.
Прежние TASK/counters/history, ветка feature/gsv-mixed-diameters и границы
разрешений сохраняются. Результат — local installer1.2.0; опубликованные
1.0.0/1.1.0 и пользовательская установка сохраняются. Вне этого ограниченного
визуального этапа действует обычная маршрутизация проекта.

Экономия именно при завершении этого этапа: Astra применяется только при
необходимых продуктовых визуальных исправлениях. Снятие screenshots, запуск
тестов/готовых скриптов, сбор logs и документация выполняются OpenCode;
это не продуктовый визуальный код. Не запускать Astra ради evidence/команд.
Финальный ограниченный порядок и запрет повторных проверок:
`docs/workflow/VISUAL-POLISH-LEAN-FINISH.md` (приоритет над старыми resume briefs).
Общую маршрутизацию других задач и глобальные конфиги не менять.

Перед работой прочитать `C:/Users/user/.agents/skills/autonomous-development/SKILL.md`;
перед Orca — `C:/Users/user/.agents/skills/orchestration/SKILL.md` и установленный
guide. Перед TASK/dispatch/review — routing-and-budget.md; перед приёмкой и
исправлениями — review-policy.md из references autonomous-development.

Источник требований — VISION.md, архитектуры — ARCHITECTURE.md, очереди —
ROADMAP.md. Фактическое утверждение и SHA256 — docs/workflow/APPROVALS.md.
Текущее состояние — docs/workflow/STATE.md, история append-only.

OpenCode/DeepSeek Flash координирует; отдельный Orca OpenCode/Flash worker
пишет код. Независимый OpenCode/Pro принимает R1, Codex принимает R2/R3 и
итог этапа. Роли и модели — docs/workflow/MODEL-ROUTING.md. Координатор не
пишет продуктовый код; исполнитель не принимает свою работу. Использовать
реальных Orca workers, не заменять встроенными subagents.

Утверждено последовательное выполнение всего этапа ГСВ. Работать в ветке
feature/gsv, в текущем workspace D:/Antigravity/GasProjectCalculator.
Координатор проверяет отсутствие конфликта ветки и переключает её перед
продуктовой работой с сохранением текущих проектных документов. Scoped local
commits после routed PASS разрешены; push/merge/deploy запрещены без отдельного
разрешения. Не менять глобальные конфиги/аккаунты и не обходить provider limits.
Сохранять посторонние изменения, .venv и пользовательские сессии.

Среда: Windows PowerShell, Python `.venv/Scripts/python.exe`.
Suite: `.\.venv\Scripts\python.exe -m unittest discover -s tests`.
Сервер: `.\.venv\Scripts\python.exe -m uvicorn app.main:app`.
UI также требует реальной browser verification desktop/mobile и evidence.
Не повторять уже доказанные проверки без основания из review-policy.

ГСН и POST /calculate сохранить совместимыми. ПК допустим только с САКЗ;
САКЗ — количество комплектов по 14000, ПК — один опциональный за 4000.
Три режима: ГСН, ГСВ, общая смета; район по 7000 каждому разделу до НДС.
Не брать нижние примечания фотографии и строку «Проект» в новый scope.

Утверждён отдельный этап Windows installer: см. ROADMAP.md и
ARCHITECTURE.md. Пользователь подтверждает упаковку Python, отдельное окно,
ярлыки Start Menu/Desktop и локальное выполнение без установки Python у
пользователя. Push/merge/release asset/deployment требуют отдельного разрешения;
installer build artifact передать локально.

Актуальный этап по запросу 2026-11-12: три длины ГСВ и графика по двум новым
референсам. Scope/формула/порядок в docs/workflow/GSV-MIXED-DIAMETERS-PLAN.md,
инструкции coordinator — GSV-MIXED-COORDINATOR-BRIEF.md. Базовые5м вычитать
из самых дешёвых труб первыми. Ветка feature/gsv-mixed-diameters от9dea625;
новый local installer1.1.0, опубликованный release1.0.0 не заменять.
