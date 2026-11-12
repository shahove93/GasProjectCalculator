# Состояние проекта

2026-11-12 — этап «три диаметра ГСВ + artwork по двум образцам + installer
1.1.0»: **COMPLETE**. Ветка `feature/gsv-mixed-diameters`; stage baseline
`9dea625`; продуктовый revision `557fe2d`; verification/accounting `0431c0b`;
финальный docs-commit — HEAD при передаче. Независимая Codex R3
`gpt-6-astra` high приняла этап **PASS**. Отчёт:
[FINAL-REPORT-MIXED-GSV](FINAL-REPORT-MIXED-GSV.md).

| TASK | Risk | Итог | Review / counters |
| --- | --- | --- | --- |
| MD-01 | R2 | mixed-формула, API, legacy | Codex PASS (C2); 2 full/1 FAIL/2 calls |
| MD-02 | R2 | UI трёх длин, детализация, artwork | Codex vision PASS; 1/0/1; NIT MD02-N1 |
| MD-03 | R2 | installer 1.1.0 + installed checks | Codex PASS; 1/0/1 |
| MD-04 | R0 | README/screenshots/docs | coordinator R0 PASS; 0 |
| MD-05 | R0 | интегрированный suite 219 OK | coordinator R0 PASS; 0 |
| FINAL-MIXED | R3 | stage acceptance | Codex Astra **PASS**; 1 call |

Authority: [PLAN](GSV-MIXED-DIAMETERS-PLAN.md), VISION/ARCHITECTURE/ROADMAP,
[APPROVALS](APPROVALS.md), MODEL-ROUTING. Frozen checklists:
`docs/workflow/tasks/MD-01..05.md`, `FINAL-MIXED-STAGE.md`.

Installer (локально, git-ignored): `installer/Output/
GasProjectCalculator-Setup-1.1.0.exe`, 15 293 993 B, SHA256
`3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710`.
Release v1.0.0 (15 286 980 B, SHA256 `71232EE4…7E08`) и оба legacy bytes не
изменены. Push/merge/deploy/release/signing не выполнялись; :8000 PID12888 и
:8138 PID23152 не тронуты.

Старые счётчики сохранены: GSV-01..04, WI-01..03, RD-01 1/0/0, RD-02 1/0/1,
RD-03 2/1/2, RD-05 1/0/1, RD-06 2/1/2, RD-07 R0, прежний stage R3 1.
Остаточные: MD02-N1 NIT (backlog); FINALMD-N1 MINOR (editorial STATE/packet
counts) исправлен при финализации; неподписанный installer/SmartScreen; одна
Windows/WebView2/DPI96 среда; combined inner scroll при min размере.
Следующий шаг — решение пользователя о публикации 1.1.0; текущий execution
packet её не включает.

## Ранее принято и опубликовано

main/feature/ss-calculator-redesign `9dea625`; compact 800×540/min 760×520,
3 режима, русский installer/splash, 167 OK. Release v1.0.0 target `e4e4dee`,
SS-Raschet-Setup.exe 15 286 980 B, SHA256 `71232EE4…7E08`.
[Публикация](PUBLICATION-v1.0.0.md),
[компактная версия](FINAL-REPORT-COMPACT-CORRECTION.md),
[разрешения](APPROVALS.md), [история](HISTORY.md),
[инструкции](../../AGENTS.md), [маршруты](MODEL-ROUTING.md).
