# Состояние проекта

2026-11-11 — этап ГСВ **COMPLETE**; этап Windows installer **COMPLETE**
(независимый Codex R3 stage acceptance PASS).

## ГСВ (принят)

- Ветка `feature/gsv`, baseline `2949223`, продуктовая ревизия `8d2d215`;
  134 теста OK, 29 API OK; три режима и browser desktop/mobile evidence.
- GSV-01 R1 PASS; GSV-02 R2 PASS (3 Codex calls); GSV-03 R1 PASS;
  GSV-04 R0 PASS; FINAL R3 PASS call 2.
- Отчёт: [FINAL-REPORT](FINAL-REPORT.md); evidence:
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
  GUI-маршрут uninstall не прокликан.
- Push/merge/deploy/release не выполнялись и не разрешены. Активных helper
  workers нет.

Ссылки: [история](HISTORY.md), [разрешения](APPROVALS.md),
[роли](MODEL-ROUTING.md), [brief](WINDOWS-INSTALLER-BRIEF.md).
