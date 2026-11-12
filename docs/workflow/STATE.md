# Состояние проекта

**Корректирующий этап компактности — IN PROGRESS** (2026-11-12). Пользователь
запросил убрать несходство с макетом и уменьшить калькулятор примерно вдвое;
разрешение и SHA256 — [APPROVALS](APPROVALS.md), brief —
[COMPACT-CORRECTION-BRIEF](COMPACT-CORRECTION-BRIEF.md). Предыдущий редизайн
COMPLETE: [FINAL-REPORT](FINAL-REPORT-SS-RASCHET-REDESIGN.md).

- Ветка `feature/ss-calculator-redesign`; настоящий HEAD/baseline
  `4b0be03`; проектные правки и docs корректирующего этапа сохранены.
- Учёт не сброшен: RD-01 1 full/0 FAIL/0 Codex; RD-02 1/0/1; RD-03 2/1/2;
  RD-04 и FINAL R0 — 0; stage1 R3 — 1. RD-03/A1 третьего full review не
  получает.
- RD-01-F4 (MAJOR): прежняя R1-4 «кнопка/итог видны в viewport» опровергнута
  реальными снимками (full-page/workaround); старый критерий 1050×740 заменён
  новым scope. RD-01 остаток 1 full сохранён, новых review RD-01 не добавлено.
- TASK: **RD-05** R1 компактный UI/geometry (OpenCode Flash → независимый
  OpenCode Pro; A1/C1; follow-up `ctx_b847d4877268`); **RD-06** R2 package/installer и реальная программа
  (OpenCode Flash → Codex `gpt-6.1-sol` high; A1/C1); **RD-07** R0 final
  verify (suite один раз); затем Codex R3 `gpt-6-astra` high.
  Frozen checklists: [RD-05](tasks/RD-05.md), [RD-06](tasks/RD-06.md),
  [RD-07](tasks/RD-07.md).
- Scope: `frontend/index.html`, `app/desktop_launcher.py`, presentation
  tests; пересборка package/installer, legacy-копия прежнего артефакта,
  evidence/screenshots, workflow docs. Вычисления/API/данные не менять.
- Ориентир: окно ~800×540, min ~760×520, плотные пары полей, результат справа
  с итогом, трубная иллюстрация; читаемый текст без CSS zoom/scale; все три
  режима и поля сохранены; action/итог при scrollY=0 без page scroll.
- Ограничения: не трогать `:8000` PID12888, окно/сессию 4392714 и посторонние
  процессы; отдельный test instance/порт; local unsigned installer; scoped
  commits после PASS; no push/merge/deploy/release/signing.
- Остаточные риски прежнего этапа (эмблема, SmartScreen, одна WebView2-среда,
  reduced motion, screenshot workaround) сохраняются; новые findings — в
  HISTORY/review.
- Следующий владелец — координатор: docs-commit, dispatch RD-05, затем routed
  review без пропуска циклов.
