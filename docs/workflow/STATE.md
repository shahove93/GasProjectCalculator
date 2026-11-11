# Состояние проекта

Редизайн «СС.Расчет» IN_PROGRESS (утверждён, вариант 1). Recovery:
[REDESIGN-RECOVERY](REDESIGN-RECOVERY.md), старый snapshot
[evidence](evidence/REDESIGN-state-pre-recovery.md).

- Branch `feature/ss-calculator-redesign`, HEAD `6d91036`, RD-03 C2 dirty.
- Parent Run `run_8e5d92ad57c7`, coordinator TASK `task_82bfbabba91b`.
- Child Run `run_8de25272cf66` (coordinator bound via `run-use`).
- RD-01 **ACCEPTED**, commit `041b13d`, OpenCode Pro R1 PASS; review
  [RD-01-review](reviews/RD-01-review.md); NIT F1–F3 backlog.
- RD-02 **ACCEPTED**, commit `32e77b1`, Codex R2 PASS (calls 1/4); review
  [RD-02-review](reviews/RD-02-review.md).
- RD-03 installer (R2): C1 FAIL (RD03-F01 MAJOR, R3-2 missing setup-error
  screenshot); C2 correction closed it with real RU dialog. C2 repeated full
  review `ctx_a92d1fc9a28c` returned **PASS**, RD03-F01 CLOSED; review
  [RD-03-review](reviews/RD-03-review.md). Full reviews 2/2, failed 1,
  Codex calls 2/4.
- Artifact (local, git-ignored):
  `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`, 15 273 647 bytes,
  SHA256 `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`;
  legacy artifact сохранён в `installer/Output/legacy/`.
- RD-03 **ACCEPTED**, scoped commit `ffe17fb`. Artifact remains local at
  `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`, 15 273 647 bytes,
  SHA256 `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`;
  legacy artifact в `installer/Output/legacy/`.
- RD-04 README (R0): **ACCEPTED**, scoped commit `c72979a`; review
  [RD-04-review](reviews/RD-04-review.md); R0 links MISSING=0, hash совпал.
- RD-FINAL-VERIFY (R0): baseline `e24d806`, final HEAD `c72979a`; verifier
  ctx_1cb546ad517e, task_e08ed7f8ac7b (OpenCode Flash, term_2f6a9d9f) running.
- Next owner: FINAL-VERIFY worker_done → R0 approval → Codex R3 stage
  acceptance (astra high) → FINAL-REPORT.
- Frozen TASK `docs/workflow/tasks/RD-*.md`, FINAL-VERIFY, FINAL.
- `:8000` PID12888 и `:8138` не трогать; no push/merge/deploy/release;
  installer только локально.

ГСВ и прежний installer COMPLETE: [ГСВ](FINAL-REPORT.md),
[installer](FINAL-REPORT-WINDOWS-INSTALLER.md). [HISTORY](HISTORY.md),
[APPROVALS](APPROVALS.md), [AGENTS](../../AGENTS.md).
