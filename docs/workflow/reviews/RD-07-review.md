# RD-07 — финальная интегрированная проверка (R0)

- Логический TASK: RD-07, R0 checklist verification.
- Verifier: Orca OpenCode/DeepSeek Flash `ctx_e7b35f80b38d`
  (`task_d2acfce2887d`, term_d6f1cdcb), read-only по продукту.
- Workspace: `D:\Antigravity\GasProjectCalculator`, ветка
  `feature/ss-calculator-redesign`.
- Baseline: `4b0be03`; suite revision `3a3a6b0`; final HEAD при записи
  `8ecb0e5` (docs-only сдвиг во время проверки; продуктовое состояние
  идентично).
- Evidence: `docs/workflow/evidence/RD-07-evidence.md`, логи
  `docs/workflow/evidence/logs/RD-07-*`.

## Вердикт R0: PASS

| ID | Результат | Основание |
| --- | --- | --- |
| F1 | PASS | Product diff `4b0be03..HEAD` — только `frontend/index.html`, `app/desktop_launcher.py`, 2 presentation test files; calculators/API/requirements/installer scripts без diff; посторонних/секретных файлов нет |
| F2 | PASS | Полный suite ровно один раз: `Ran 167 tests in 2.126s`, **OK**, exit 0; лог `RD-07-suite.txt` |
| F3 | PASS | Installer 15 286 980 B `71232EE4…7E08`; legacy pre-compact `04388410…949A`; previous-stage `2973278F…428F`; dist `5403540C…DD2C` — match |
| F4 | PASS | RD-05 20 screenshots, RD-06 34 screenshots; native JSON; mobile B7 `FFB848…43A5` 390×844, 375/375, scroll 0/0; RD06-F01 CLOSED, F02 MINOR backlog; FAIL сохранён |
| F5 | PASS | `app/main.py`, calculators, requirements без diff; значения 131250/105525/145950 подтверждены reuse-артефактами |
| F6 | PASS | README 800×540/min 760×520, новый installer size/hash и `rd-06-*` screenshots; STATE/HISTORY счётчики и route согласованы |
| Runtime | PASS | `:8000` PID12888, `:8138` PID23152, пользовательская установка/PID13248 не изменены; test backend/окон/портов не осталось |

## Счётчики

- RD-07: R0 PASS, Codex calls 0.
- Итог корректирующего этапа: RD-05 1 full/0 FAIL/1 Codex (R1 Pro capability
  BLOCKED, не failed); RD-06 2 full/1 FAIL/2 Codex, RD06-F01 CLOSED,
  RD06-F02 MINOR backlog; RD-07 R0 PASS.
- Прежние счётчики сохранены: RD-01 1/0/0, RD-02 1/0/1, RD-03 2/1/2,
  RD-04/FINAL R0 0, stage1 R3 1.

## Дальше

Codex R3 stage acceptance корректирующего этапа (`gpt-6-astra` high), затем
итоговый отчёт и COMPLETE. Проектный PASS фиксирует координатор.
