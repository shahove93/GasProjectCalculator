# Состояние проекта

**СС.Расчет — редизайн COMPLETE** (2026-11-12). Все TASK приняты,
FINAL-VERIFY R0 PASS, независимая Codex R3 stage acceptance **PASS**.
Отчёт: [FINAL-REPORT-SS-RASCHET-REDESIGN](FINAL-REPORT-SS-RASCHET-REDESIGN.md).

- Ветка `feature/ss-calculator-redesign` от `e24d806`; продуктовая ревизия
  доставки `a14f032`; после неё только docs-only commit (report/review/state).
- Child Run `run_8de25272cf66`; parent Run `run_8e5d92ad57c7`,
  coordinator TASK `task_82bfbabba91b`.
- TASK: RD-01 R1 PASS (`041b13d`, [review](reviews/RD-01-review.md));
  RD-02 R2 PASS (`32e77b1`, [review](reviews/RD-02-review.md));
  RD-03 R2 C1 FAIL→C2 PASS, RD03-F01 CLOSED (`ffe17fb`,
  [review](reviews/RD-03-review.md)); RD-04 R0 PASS (`c72979a`);
  RD-FINAL-VERIFY R0 PASS ([evidence](evidence/RD-FINAL-evidence.md));
  Stage R3 PASS (`gpt-6-astra` high, `ctx_3b5e848dc8a6`).
- Счётчики: RD-01 1 full/0 FAIL/0 Codex; RD-02 1/0/1; RD-03 2/1/2;
  RD-04 + FINAL R0 0 Codex; stage R3 +1. Скрытых failed reviews нет.
- Артефакт (local, unsigned, git-ignored):
  `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`, 15 273 647 bytes,
  SHA256 `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`;
  legacy installer сохранён в `installer/Output/legacy/`.
- Проверено: title/ярлыки `СС.Расчет`, круглая эмблема без wordmark, окно
  1050×740/min 860×620, RU splash/ready lifecycle, RU installer/uninstaller,
  три режима 131250/105525/145950, loopback/port/close, user files сохранены,
  suite 163 OK exit 0; API/расчёты не изменены.
- Остаточный риск: формальные права на эмблему не подтверждены; installer
  неподписан (SmartScreen); одна Windows/WebView2-среда, reduced motion через
  эмуляцию. NIT backlog RD-01 F1–F3; RD-FINAL N01/N02 исправлены в STATE.
- `:8000` PID12888 не тронут; no push/merge/deploy/release/signing; installer
  передан локально. Все Orca workers released.

Предыдущие этапы COMPLETE: ГСВ — [FINAL-REPORT](FINAL-REPORT.md);
Windows installer —
[FINAL-REPORT-WINDOWS-INSTALLER](FINAL-REPORT-WINDOWS-INSTALLER.md).
Разрешения [APPROVALS](APPROVALS.md), инструкции [AGENTS](../../AGENTS.md).
