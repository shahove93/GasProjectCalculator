# Состояние проекта

Редизайн IN_PROGRESS, восстановление координатора разрешено пользователем.

Сначала прочитать [REDESIGN-RECOVERY](REDESIGN-RECOVERY.md): точные Run/Task/
Dispatch IDs, остановка старого coordinator подтверждена, ресурсные терминалы
освобождены, изменения/попытки сохраняются. Старый snapshot:
[evidence](evidence/REDESIGN-state-pre-recovery.md).

- Branch feature/ss-calculator-redesign, HEAD 32e77b1, worktree clean.
- Parent Run run_8e5d92ad57c7, coordinator TASK task_82bfbabba91b.
- Старый coordinator ctx_2af249de822a: stopped/exited/released.
- Child Run run_8de25272cf66 (координатор привязан через run-use), RD-01 task_527858dbf289.
- RD-01 attempts ctx_eeb0ad4b83cb и ctx_66fd60974141 stopped/exited/released.
- RD-01 implementer ctx_6bc08bbe6a19 succeeded/released; evidence RD-01-evidence.md,
  12 screenshots, suite reuse 152 OK; :8000 не тронут.
- RD-01 **ACCEPTED**, scoped commit `041b13d`; review record
  [RD-01-review](reviews/RD-01-review.md). Full reviews 1/2, failed 0, Codex 0.
  NIT backlog F1–F3 не блокируют.
- RD-02 window+splash (R2): baseline `041b13d`, A1/C1; implementer
  ctx_b89935976cc0 succeeded/released. Evidence RD-02-evidence.md + 4 снимка.
- RD-02 **PASS** Codex R2 ctx_66502b51d130 (`gpt-6.1-sol` high), released;
  finding IDs нет; review [RD-02-review](reviews/RD-02-review.md).
  Codex calls 1/4. RD-02 **ACCEPTED**, scoped commit `32e77b1`.
- RD-03 RU installer (R2): baseline `32e77b1`, A1/C1, Codex sol high,
  reserve ≤4/3M. Implementer ctx_e4488f57f75b, task_52e983ff51d0
  (OpenCode Flash, term_e70ef6bf) running.
- Next owner: RD-03 implementer; затем Codex R2 review.
- Frozen TASK RD-01..04/FINAL в docs/workflow/tasks; обычный routed review.
- :8000 PID12888 не трогать; :8123 проверочный server старого coordinator.
- Цель: СС.Расчет, компактный вариант 1, круглая эмблема, русская заставка и
  installer. Изменения согласованы в APPROVALS. No push/merge/Release.

ГСВ и прежний installer COMPLETE: [ГСВ](FINAL-REPORT.md),
[installer](FINAL-REPORT-WINDOWS-INSTALLER.md). История [HISTORY](HISTORY.md),
разрешения [APPROVALS](APPROVALS.md), инструкции [AGENTS](../../AGENTS.md).
