# Состояние проекта

**Визуальное продолжение 1.2.0 — COMPLETE (2026-11-12)**:
VP-01 PASS; VP-02 evidence pack полон. Lean finish: пять settled кадров
D1–D5 сняты после `getAnimations()`/`opacity=1`; полный integrated suite
исполнен один раз (219 tests OK, exit 0). Независимый **R2 PASS** (W1–W11;
NIT VP02-R2-N1 исправлен) и отдельная финальная stage-приёмка
**gpt-6.1-sol/high PASS**. Итог: `FINAL-REPORT-VISUAL-POLISH.md`; local
artifact 1.2.0 передан локально. Прежние BLOCKED/resume сохраняются в
истории: [VP-02-blocked-resume](evidence/VP-02-blocked-resume.md),
[VP-02-resume](evidence/VP-02-resume.md),
[VP-02-blocked](evidence/VP-02-blocked.md).

- Ветка `feature/gsv-mixed-diameters`, baseline
  `ac59d8c27ed47be07ac9b54acf8285bcab704be0`. Предыдущий этап 1.1.0 —
  COMPLETE (release id442672288) и не пересматривается; remote 1.1.0/1.0.0
  не меняются.
- Пользователь утвердил визуальную переделку: шапка и подвал по новым
  refs, заставка по `splash-installer-reference.jpg`, установщик в том же
  стиле, небольшие дизайнерские улучшения, новый local installer 1.2.0.
  Исполнитель — настоящий Orca **Codex `gpt-6-astra`, high** (явное
  ограниченное исключение); обе независимые приёмки (R2 и финальная
  stage) — отдельные **Codex `gpt-6.1-sol`, high** контексты по решению
  пользователя «поручим Sol».
- Logical TASK: **MD-02 A2 (VP-01)** и **MD-03 A2 (VP-02)**. Прежний
  A1/C1 PASS, NIT MD02-N1 и история сохранены. Бюджет: MD-02 1/4 → review
  2/4 (PASS); MD-03 1/4 → review call 2/4 (PASS, 0 FAIL). Финальная
  stage-приёмка учитывается отдельно.
- TASK/checklist: `docs/workflow/tasks/VP-01.md`, `VP-02.md`; preflight и
  восстановленные counters: `docs/workflow/evidence/VP-00-preflight.md`.
- Прежние installer bytes 1.0.0/1.1.0/legacy зафиксированы до build;
  сохраняются `:8000`/:8138, `.venv`, пользовательская установка/сессии,
  чужие изменения и новые design docs.
- Владелец активной работы — только текущий координатор; второго writer нет.
- **VP-01 (MD-02 A2/C1) PASS**: независимый R2 Codex `gpt-6.1-sol` high
  подтвердил V1–V12 по actual diff/evidence; MD02-N1 (обрезанный маховик)
  CLOSED; новых findings нет. Счётчики review 1/0/1, logical MD-02 2/0/2-of-4.
  Local scoped commit `1689773718c818a4ebca400afc2d8a4206b6458e`.
- **VP-02 (MD-03 A2) BLOCKED** реальным Codex provider usage limit
  (`gpt-6-astra` high, 5h limit, reset 16:28). Installer 1.2.0 собран:
  15 373 267 B SHA256 `4579FB3A…6113`; wizard/native screenshots и isolated
  evidence сохранены. Модель не заменялась, кредиты не покупались; worker
  fenced, пользовательские HKCU/ярлыки/106 files/PID 13248 и :8000/:8138
  восстановлены и сохранены.
- **VP-02 RESUME (2026-11-12)**: пользователь разрешил продолжить после
  восстановления лимитов. Ownership сверен: live writer только текущий
  координатор `ctx_ed7166e32fdc`; прежний worker release/stopped, второго
  writer нет. Planner evidence: `evidence/VP-02-resume.md`. Baseline
  продолжения HEAD `1689773718c818a4ebca400afc2d8a4206b6458e`; installer
  1.2.0 bytes `4579FB3A…6113` и user HKCU/ярлыки/106 files/PID 13248,
  :8000/:8138 сохранены. Доделываются только недостающие W1–W11 проверки и
  evidence pack, затем независимый R2 review.
- **VP-02 resume dispatched**: runtime не позволил reopen прежний task в
  `run_8e5d92ad57c7` (`task_not_found`/`worker_cannot_coordinate_own_run`),
  поэтому та же logical работа идёт в дочернем Run `run_51b48d1d96cc`,
  task `task_150bb380db2c`, worker `ctx_988a8c02d5c3`
  (term `term_879889ea-ac9e-48ad-bc89-978a67a20e10`). Requested/effective
  подтверждены: `agent=codex`, `model=gpt-6-astra`, `effort=high`.
  Self-contained spec: `evidence/VP-02-resume-spec.md`; receipts в logs.
- **VP-02 снова BLOCKED** (2026-11-12 ~16:54): Codex `gpt-6-astra` high
  вернул usage limit («try again at 9:31 PM», предложение `gpt-6-luna`
  отклонено). Worker fenced (`state=stopped`, terminal closed), модель/аккаунт
  не менялись, кредиты не покупались. Основной evidence pack
  [VP-02-evidence](evidence/VP-02-evidence.md) собран; gap — только пять
  browser-кадров `visual-02-resumed-desktop-gsv-D1..D5.png`, снятых во время
  `fadeUp`; settled-пересъёмка NOT_RUN. Подробности:
  [VP-02-blocked-resume](evidence/VP-02-blocked-resume.md).
- Проверено после остановки: user PID 13248, :8000/:8138, HKCU 1.0.0,
  ярлыки, 106 files/37 372 847 B и artifact bytes сохранены; isolated
  процессов нет; commit/push/merge/deploy/release нет.
- **Lean finish выполнен (2026-11-12):** пять settled кадров
  `visual-02-resumed-desktop-gsv-D1..D5-settled.png` сняты после
  `document.getAnimations()` при `opacity=1`, итоги
  75600/79275/71400/63000/70875; полный integrated suite исполнен один раз
  по HEAD `1689773718`: 219 tests OK, exit 0.
- **VP-02 (MD-03 A2/C1) R2 PASS (2026-11-12):** независимый Codex
  `gpt-6.1-sol` high, task `task_65c331479b7e`, dispatch `ctx_df0f7573e041`,
  actual diff/23 vision images. Все W1–W11 PASS, 0 BLOCKER/MAJOR/MINOR;
  один NIT VP02-R2-N1 о формулировке «48 PNG» (фактически 39 PNG + 9 JPEG
  с расширением .png) исправлен в evidence без пересъёмки. Verdict:
  [VP-02-review](../reviews/VP-02-review.md). Счётчик review call 2/4
  израсходован; logical MD-03 2/0/2-of-4.
- **Финальная stage-приёмка (2026-11-12) PASS:** отдельный Codex
  `gpt-6.1-sol` high, task `task_38ba500ce885`, dispatch `ctx_059202c6763a`,
  read-only; критерии 1–6 PASS, новых findings 0. Verdict:
  [VP-02-final-stage-review](../reviews/VP-02-final-stage-review.md).
- **Этап COMPLETE:** `FINAL-REPORT-VISUAL-POLISH.md`; README содержит
  локальную сборку 1.2.0 (не опубликована); local artifact
  15 373 267 B SHA256 `4579FB3A…6113`; local scoped commit выполнен.
  Push/merge/deploy/release/signing не выполнялись.
- Astra не запускается, пока нет новой реальной продуктовой визуальной
  правки.
- Ограничения: нет push/merge/deploy/release/signing; public release 1.1.0
  не заменять.

[смешанные диаметры](FINAL-REPORT-MIXED-GSV.md),
[публикация 1.1.0](PUBLICATION-v1.1.0.md),
[история](HISTORY.md), [разрешения](APPROVALS.md),
[визуальный brief](VISUAL-POLISH-ASTRA-BRIEF.md).
