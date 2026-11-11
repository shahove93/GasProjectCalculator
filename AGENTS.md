# GasProjectCalculator: разработка через Orca

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
