# Состояние проекта

**Визуальное продолжение 1.2.0 — IN_PROGRESS** (2026-11-12).

- Ветка `feature/gsv-mixed-diameters`, baseline
  `ac59d8c27ed47be07ac9b54acf8285bcab704be0`. Предыдущий этап 1.1.0 —
  COMPLETE (release id442672288) и не пересматривается; remote 1.1.0/1.0.0
  не меняются.
- Пользователь утвердил визуальную переделку: шапка и подвал по новым
  refs, заставка по `splash-installer-reference.jpg`, установщик в том же
  стиле, небольшие дизайнерские улучшения, новый local installer 1.2.0.
  Исполнитель — настоящий Orca **Codex `gpt-6-astra`, high** (явное
  ограниченное исключение); R2 review — **Codex `gpt-6.1-sol`, high**;
  финальная приёмка — отдельный **`gpt-6-astra`, high** контекст.
- Logical TASK: **MD-02 A2 (VP-01)** и **MD-03 A2 (VP-02)**. Прежний
  A1/C1 PASS, NIT MD02-N1 и история сохранены. Бюджет: MD-02 1/4 → новый
  review 2/4; MD-03 1/4 → новый review 2/4. Финальная stage-приёмка
  учитывается отдельно.
- TASK/checklist: `docs/workflow/tasks/VP-01.md`, `VP-02.md`; preflight и
  восстановленные counters: `docs/workflow/evidence/VP-00-preflight.md`.
- Прежние installer bytes 1.0.0/1.1.0/legacy зафиксированы до build;
  сохраняются `:8000`/:8138, `.venv`, пользовательская установка/сессии,
  чужие изменения и новые design docs.
- Владелец активной работы — только текущий координатор; второго writer нет.
- **VP-01 (MD-02 A2/C1) PASS**: независимый R2 Codex `gpt-6.1-sol` high
  подтвердил V1–V12 по actual diff/evidence; MD02-N1 (обрезанный маховик)
  CLOSED; новых findings нет. Счётчики review 1/0/1, logical MD-02 2/0/2-of-4.
  Local scoped commit выполняется координатором.
- Next: VP-02 (installer 1.2.0, MD-03 A2) → R2 review → интегрированный full
  suite → отдельная финальная Astra stage-приёмка → FINAL-REPORT/README/STATE
  → local commit.
- Ограничения: нет push/merge/deploy/release/signing; public release 1.1.0
  не заменять.

[смешанные диаметры](FINAL-REPORT-MIXED-GSV.md),
[публикация 1.1.0](PUBLICATION-v1.1.0.md),
[история](HISTORY.md), [разрешения](APPROVALS.md),
[визуальный brief](VISUAL-POLISH-ASTRA-BRIEF.md).
