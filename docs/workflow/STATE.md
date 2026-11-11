# Состояние проекта

2026-11-11 — этапы ГСВ и Windows installer **COMPLETE** (Codex R3 PASS).

## ГСВ (принят)

- Ветка `feature/gsv`, baseline `2949223`, ревизия `8d2d215`; 134 теста OK,
  29 API OK; три режима и browser desktop/mobile evidence.
- GSV-01 R1 PASS; GSV-02 R2 (3 Codex); GSV-03 R1 PASS; GSV-04 R0 PASS;
  FINAL R3 PASS call 2. Отчёт [FINAL-REPORT](FINAL-REPORT.md), evidence
  [FINAL-EVIDENCE](evidence/FINAL-EVIDENCE.md).

## Windows installer (COMPLETE)

- Утверждён 2026-11-11; ветка `feature/windows-installer` от `feature/gsv`
  `22133a1`; R3 принял ревизию `3d291e9`.
- Артефакт (local, unsigned, не публиковался):
  `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`, 15 256 037 байт,
  SHA256 `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`.
- Проверено: clean x64 build; per-user install/HKCU; Start Menu + optional
  Desktop; без Python/консоли; readiness до окна; ГСН/ГСВ/combined
  131250/105525/145950; только 127.0.0.1 и обход занятого порта; закрытие
  освобождает порт; понятная ошибка; uninstall сохраняет файлы; developer
  uvicorn; README; suite 146 OK.
- TASK: WI-01 R2 PASS (1 call) `7fab960`; WI-02 R2 PASS (1) `144a75c`;
  WI-03 R0 PASS (0) `9eaed0a`; FINAL verify R0 PASS (0); FINAL R3 PASS (1)
  `3d291e9`.
- Evidence:
  [FINAL-WINDOWS-INSTALLER-EVIDENCE](evidence/FINAL-WINDOWS-INSTALLER-EVIDENCE.md);
  reviews `WI-0*`/`FINAL-STAGE`; отчёт
  [FINAL-REPORT-WINDOWS-INSTALLER](FINAL-REPORT-WINDOWS-INSTALLER.md).
- Backlog: `WI02-R1-F1` MINOR; одна машина; unsigned/SmartScreen; WebView2;
  GUI-uninstall не прокликан. Push/merge/deploy/release не разрешены.

Ссылки: [история](HISTORY.md), [разрешения](APPROVALS.md),
[роли](MODEL-ROUTING.md), [brief](WINDOWS-INSTALLER-BRIEF.md).

## СС.Расчет — редизайн IN_PROGRESS

- Утверждён 2026-11-11 (APPROVALS/SHA256). Ветка `feature/ss-calculator-redesign`
  от `e24d806`; workflow-коммит до dispatch. Run `run_8de25272cf66`.
- Эмблема: `assets/company-logo-source.png` (одобрен пользователем; формальные
  права репозиторием не подтверждены — остаточный риск). Installer stage цел.
- TASK sequential, A1/C1; checklists `docs/workflow/tasks/RD-*.md`:
  | TASK | Risk | Review | Reserve |
  | --- | --- | --- | --- |
  | RD-01 frontend+emblem | R1 | OpenCode Pro 1 full | Codex 0 |
  | RD-02 window+splash | R2 | Codex sol high 1 full | 4/3M |
  | RD-03 RU Inno+rebuild | R2 | Codex sol high 1 full | 4/3M |
  | RD-04 README | R0 | coord checklist | 0 |
  | FINAL-VERIFY | R0 | coord checklist | 0 |
  | FINAL stage | R3 | Codex astra high 1 | 6/5M |
- Dispatch IDs: pending. Next: coordinator commits docs, dispatches RD-01.
- Product NOT_REVIEWED. :8000 не трогать; без push/merge/release/deploy/signing;
  installer только локально.
