# Состояние проекта

2026-11-11 — EXECUTING: утверждённый этап ГСВ, ветка `feature/gsv`, baseline `2949223`.

- Утверждение: APPROVALS.md, SHA256 пакета зафиксированы; «Теперь принимаю.».
- Preflight: Orca 1.4.250, OpenCode 1.19.3, модели `deepseek/deepseek-flash`
  и `deepseek/deepseek-v4-pro` в каталоге. Run `run_8e5d92ad57c7`.
- Baseline suite: 57 unittest, exit 0, OK (CWD `D:/Antigravity/GasProjectCalculator`).
- Рабочее дерево: проектные документы/AGENTS.md/opencode.json сохранены; ветка
  создана без reset.

## Логические TASK и маршруты (бюджеты до dispatch)

| TASK | Содержание | Риск | Приёмка | Циклы | Codex calls |
| --- | --- | --- | --- | --- | ---: |
| GSV-01 | модуль расчёта ГСВ + unit-тесты | R1 | OpenCode Pro | C1 | 0 |
| GSV-02 | API /gsv и /combined + тесты | R2 | Codex gpt-6.1-sol high | C1 | ≤4 |
| GSV-03 | UI три режима + browser evidence | R1 | OpenCode Pro | C1 | 0 |
| GSV-04 | финальный suite, browser, README, evidence | R0 | чек-лист коорд. | C1 | 0 |
| FINAL | приёмка этапа | R3 | Codex gpt-6-astra high | — | ≤6 |

Каждый TASK: отдельный Orca OpenCode worker, allowlist и frozen acceptance;
исполнитель не коммитит. Координатор коммитит scoped после routed PASS.

## Текущий статус

- Активных helper workers нет. Продуктовый код не начинался.
- Следующий шаг: commit workflow-документов, затем dispatch GSV-01.
- Вердикт этапа: NOT_REVIEWED. Push/merge/deploy запрещены.

Ссылки: [история](HISTORY.md), [разрешения](APPROVALS.md),
[роли](MODEL-ROUTING.md), [brief](COORDINATOR-BRIEF.md).
