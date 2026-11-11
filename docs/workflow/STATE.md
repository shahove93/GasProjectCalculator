# Состояние проекта

2026-11-11 — **COMPLETE**: утверждённый этап ГСВ реализован и принят.

- Ветка `feature/gsv`, baseline `2949223`; последняя продуктовая ревизия
  `8d2d215`; финальный docs/evidence commit добавляет отчёт и README NIT.
- Утверждение: APPROVALS.md, SHA256 пакета совпали при финальной приёмке.
- Preflight: Orca 1.4.250, OpenCode 1.19.3; DeepSeek Flash/Pro, GPT-6.1-sol,
  GPT-6-astra использованы по маршрутам.

## Результат

- Сохранены 57 тестов ГСН и контракт `POST /calculate`.
- Добавлены `app/gsv_calculator.py`, `POST /calculate/gsv`,
  `POST /calculate/combined`, Pydantic-модели запроса и ответа.
- UI: три режима ГСН/ГСВ/ГСН+ГСВ, несколько САКЗ, ПК только с САКЗ
  (422 + блокировка/сброс), диаметр >57 отклоняется, бурение 0/8000/10000,
  район 7000 за раздел, НДС 5%.
- Полный suite: 134 теста, exit 0, OK. API: 29 OK. Browser desktop/mobile
  и regression-сценарии с 10 скриншотами.

## TASK и приёмка

| TASK | Риск | Вердикт | Codex calls |
| --- | --- | --- | ---: |
| GSV-01 модуль | R1 | PASS OpenCode Pro | 0 |
| GSV-02 API | R2 | PASS после C1 FAIL и regression | 3 |
| GSV-03 UI | R1 | PASS после regression | 0 |
| GSV-04 docs/evidence | R0 | PASS | 0 |
| FINAL этап | R3 | PASS call 2 (call 1 FAIL) | 2 |

Все finding'и финального FAIL исправлены и повторно приняты. NIT README
(131→134) исправлен. Отчёт: [FINAL-REPORT](FINAL-REPORT.md).
Доказательства: [FINAL-EVIDENCE](evidence/FINAL-EVIDENCE.md).

## Остаточное

- Starlette/httpx warning в тестах; browser evidence только Orca engine.
- Push/merge/deploy не выполнялись и не разрешены.
- Активных helper workers нет; все ресурсы освобождены.

Ссылки: [история](HISTORY.md), [разрешения](APPROVALS.md),
[роли](MODEL-ROUTING.md), [brief](COORDINATOR-BRIEF.md).
