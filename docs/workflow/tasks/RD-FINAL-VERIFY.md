# RD-FINAL-VERIFY — Интегрированная проверка этапа редизайна (R0)

## Authority

Approved redesign stage; `AGENTS.md`, `ARCHITECTURE.md`, `ROADMAP.md` шаги
10–11, `docs/workflow/APPROVALS.md` (2026-11-11). Ты — OpenCode исполнитель
проверки; не меняешь файлы и не присваиваешь проектный PASS.

## Precondition

RD-01..RD-04 приняты и закоммичены. Baseline — продуктовый baseline
`e24d806`; final revision — текущий HEAD ветки `feature/ss-calculator-redesign`.

## Goal

Собрать интегрированный evidence pack против final HEAD: полный suite один
раз, фактический diff против baseline, artifact path/size/SHA256, наличие
скриншотов/документации, отсутствие неожиданных файлов, сохранность API/
расчётов/developer path.

## Allowed

- Только чтение/запуск проверок; запись `docs/workflow/evidence/RD-FINAL-*`
  и `docs/workflow/evidence/logs/RD-FINAL-*`.
- Не менять продуктовый код, не коммитить, не push/merge/deploy.
- Не трогать пользовательский сервер на 8000; не переустанавливать без
  необходимости, если RD-03 evidence полон (reuse rule).

## Frozen checklist

| ID | Check | Evidence |
| --- | --- | --- |
| RF-1 | `git diff --stat e24d806..HEAD` соответствует scope редизайна | Diff/status |
| RF-2 | Полный unittest suite exit 0, число тестов | Exact command/CWD/exit/log |
| RF-3 | Artifact существует, size/SHA256 совпадают с README/RD-03 | Hash check |
| RF-4 | Скриншоты app/installer существуют и не пустые | File checks |
| RF-5 | Title/shortcut `СС.Расчет`, subtitle, окно/размеры | Reuse proof + spot check |
| RF-6 | Три режима 131250/105525/145950 подтверждены | Reuse RD-01/RD-03 evidence |
| RF-7 | Splash lifecycle/no network/reduced motion доказаны | Reuse RD-02 evidence |
| RF-8 | Installer RU, reinstall/uninstall сохраняют user files | Reuse RD-03 evidence |
| RF-9 | Расчёты/API/тарифы не изменены | Diff + suite |
| RF-10 | Нет незаявленных файлов/секретов/бинарников в git | Status/file list |

## Reporting

Верни: HEAD SHA, diff scope, suite result, hash, reuse mapping, NOT_RUN и
любые расхождения. Не заявляй PASS.
