# Рабочая схема по образцу EquipmentDocumentationRegistry

Подготовлено 2026-11-11 по запросу пользователя. Схема взята из локальных
`D:/Antigravity/EquipmentDocumentationRegistry/AGENTS.md`, `opencode.json`
и `docs/workflow/MODEL-ROUTING.md`. Разрешения и бюджеты другого проекта сюда
не переносятся. Запись модели в документ не переключает текущий чат.

| Роль | Целевая модель |
| --- | --- |
| Чат с пользователем, требования, проектирование | Codex, текущий чат |
| Orca/OpenCode координатор | `deepseek/deepseek-flash` |
| Отдельный Orca/OpenCode исполнитель | `deepseek/deepseek-flash` |
| Отдельный независимый R1-ревьюер OpenCode | `deepseek/deepseek-v4-pro` |
| Codex R2-ревью | `gpt-6.1-sol`, high |
| Codex R3-ревью и итоговая приёмка | `gpt-6-astra`, high |

R0 принимается по доказанному чек-листу без Codex. Координатор не пишет
продуктовый код, исполнитель не принимает собственную работу. Codex не ведёт
очередь и не ожидает работников. Каждый worker — настоящий Orca worker с
отдельной ролью, TASK, allowlist, baseline и замороженным чек-листом.

Перед запуском проверить текущую справку Orca, установку OpenCode, доступность
моделей и requested/effective model. В этом проекте генерация и dispatch ещё
не проверены; конфигурация другого проекта не является доказательством.
Глобальные настройки и учётные записи не менять; молча модель не заменять.

Процедуры риска, попыток, evidence и лимитов брать из актуальных
`C:/Users/user/.agents/skills/autonomous-development/references/routing-and-budget.md`
и `review-policy.md`. При отказе провайдера по лимиту остановить зависимую
цепочку до явного решения пользователя, без обхода лимитов.
