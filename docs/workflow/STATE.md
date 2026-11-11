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

- GSV-01 R1: PASS OpenCode Pro `ctx_6f8faa93b48a`; 48 новых / 105 total OK.
- GSV-02 R2: C1 FAIL только по evidence/baseline, C2 PASS; после финального
  FAIL переоткрыт и исправлен (response models), R2 PASS `ctx_ddd46cfbef19`;
  29 API / 134 suite OK. Codex calls: 3 (1 FAIL + 2 PASS).
- GSV-03 R1: UI три режима; первая попытка остановлена без worker_done,
  продолжение завершило browser evidence; R1 PASS `ctx_d7c8f160505f`.
  Финальная приёмка нашла 4 MAJOR (2 в UI); UI переоткрыт и исправлен
  (initial mode, stale response, hidden validation, NIT); R1 PASS
  `ctx_faa3f1ff8d22`, findings нет. 134 suite OK.
- GSV-04 R0: README и FINAL-EVIDENCE обновлены; продуктовый код не менялся.
- Активных helper workers нет; все освобождены.
- FINAL R3: первый вызов `ctx_a35b269f1f44` — FAIL (4 MAJOR + 1 NIT), все
  исправлены и повторно приняты routed review. Ожидается повторная финальная
  приёмка gpt-6-astra high, затем FINAL-REPORT.
- Вердикт этапа: NOT_REVIEWED до финальной приёмки. Push/merge/deploy запрещены.

Ссылки: [история](HISTORY.md), [разрешения](APPROVALS.md),
[роли](MODEL-ROUTING.md), [brief](COORDINATOR-BRIEF.md).
