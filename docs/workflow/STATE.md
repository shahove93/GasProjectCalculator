# Состояние проекта

2026-11-11 — этап ГСВ **COMPLETE**; этап Windows installer **IN_PROGRESS**.

## ГСВ (принят)

- Ветка `feature/gsv`, baseline `2949223`, продуктовая ревизия `8d2d215`.
- 134 теста OK, 29 API OK; три режима и browser desktop/mobile evidence.
- GSV-01 R1 PASS; GSV-02 R2 PASS (3 Codex calls); GSV-03 R1 PASS;
  GSV-04 R0 PASS; FINAL R3 PASS call 2.
- Отчёт: [FINAL-REPORT](FINAL-REPORT.md); evidence:
  [FINAL-EVIDENCE](evidence/FINAL-EVIDENCE.md).

## Windows installer (IN_PROGRESS)

- Утверждён 2026-11-11; ARCH/ROADMAP SHA256 совпали (2596…, 7879…). Scope:
  local installer artifact; без signing/push/merge/release.
- Ветка `feature/windows-installer` от `feature/gsv` HEAD `22133a1`; worktree
  текущий; approved planning docs сохранены uncommitted; второй writer нет.
- Preflight: Orca 1.4.250; Python 3.12.4; WebView2 157.0.4341.42;
  PyInstaller 6.22.3 + pywebview 6.2.1 installable (pin); Inno Setup 6 portable
  ISCC `C:\Users\user\AppData\Local\Temp\edr-windows-build\inno\ISCC.exe`;
  admin не требуется. User uvicorn на :8000 не трогать.
- TASK records: [WI-01](tasks/WI-01.md), [WI-02](tasks/WI-02.md),
  [WI-03](tasks/WI-03.md).

| TASK | Риск | Маршрут / бюджет | Статус |
| --- | --- | --- | --- |
| WI-01 packaging/window | R2 | Codex gpt-6.1-sol high, ≤4 calls/3M | PASS C1 (1 call); commit `7fab960` |
| WI-02 installer | R2 | Codex gpt-6.1-sol high, ≤4 calls/3M | PASS C1 (1 call); commit `144a75c`; artifact SHA256 `2973278…428F` |
| WI-03 docs | R0 | coordinator checklist | PASS (0 calls); commit `9eaed0a` |
| FINAL verify | R0 | coordinator checklist | PASS (0 calls); suite 146 OK |
| FINAL stage | R3 | Codex gpt-6-astra high, ≤6 calls/5M | R3 acceptance dispatch |

- WI-01 evidence: [WI-01-evidence](evidence/WI-01-evidence.md),
  verdict [WI-01-review](reviews/WI-01-review.md). Reviewer — Codex
  `gpt-6.1-sol` high, PASS без findings; 1 Codex call.
- WI-02 evidence: [WI-02-evidence](evidence/WI-02-evidence.md),
  verdict [WI-02-review](reviews/WI-02-review.md). Codex PASS, 1 call; MINOR
  backlog `WI02-R1-F1` (verify-runtime cleanup path) для FINAL-REPORT.
- WI-03 evidence: [WI-03-evidence](evidence/WI-03-evidence.md),
  verdict [WI-03-review](reviews/WI-03-review.md). R0 PASS, 0 Codex calls.
- FINAL evidence:
  [FINAL-WINDOWS-INSTALLER-EVIDENCE](evidence/FINAL-WINDOWS-INSTALLER-EVIDENCE.md):
  docs-only diff since `144a75c`, artifact hash совпал, suite 146 OK, user
  uvicorn :8000 не тронут.
- Next owner: Codex R3 stage acceptance `gpt-6-astra` high; затем FINAL-REPORT.
- Installer artifact: local only; exact path/hash после сборки.

## Остаточное

- Starlette/httpx warning в тестах; browser evidence Orca engine.
- Push/merge/deploy/release не разрешены.
- Активных helper workers нет.

Ссылки: [история](HISTORY.md), [разрешения](APPROVALS.md),
[роли](MODEL-ROUTING.md), [brief](WINDOWS-INSTALLER-BRIEF.md).
