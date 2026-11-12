# RD-05 — независимая приёмка компактного UI и native geometry

- Логический TASK: RD-05, подход A1, цикл C1.
- Исполнитель: Orca OpenCode/DeepSeek Flash worker; исходный dispatch
  `ctx_e4831c98c444`, завершающий follow-up `ctx_b847d4877268`
  (`task_dc32b3365d51`). Продуктовый baseline `4b0be03`; фактический diff
  поверх `2fe240c`.
- Review route: сначала независимый OpenCode Pro `ctx_0e9b8901c316`
  (`task_50a9bc376b3f`, effective `deepseek/deepseek-v4-pro`) — **BLOCKED**
  не по продукту: у модели нет image input, поэтому U2/U11/U12 непроверяемы;
  U1, U3–U10 подтверждены PASS без rerun, продуктовых BLOCKER/MAJOR нет.
  Это capability-BLOCKED, не failed review. Для визуальной приёмки назначен
  независимый Codex R2 `ctx_8fb5c34ce714` (`task_52ee88d3a8f0`,
  `gpt-6.1-sol` high), read-only. Это первый полный review RD-05 A1/C1,
  не дополнительный цикл и не третий review RD-03/A1.
- Основной образец: `docs/design/original-window-splash-reference.png`;
  `approved-variant-1-reference.png` — вспомогательный для эмблемы/названия.

## Вердикт: PASS

BLOCKER/MAJOR отсутствуют; все U1–U12 приняты. F1/F2 — MINOR backlog.

| ID | Вердикт | Основание |
| --- | --- | --- |
| U1 | PASS | Outer 800×540 / min 760×520; client 784×501 / 744×481; DPI 96; clamp 400×300 → min |
| U2 | PASS | Тёмная шапка, эмблема/название, труба/вентиль и режимы; строка заказчика; пары полей и отдельный блок опций слева; тёплая карточка итога/кнопка справа; нижняя труба/дом |
| U3 | PASS (F1 MINOR) | Плотная раскладка; body/input 13 px, button 13,5 px; zoom/scale нет; подписи читаются на 1:1 снимках |
| U4 | PASS | Target/min × 3 режима до/после: scrollX/Y=0; docScroll=docClient; действие видно до/после; итог виден после расчёта; combined — внутренняя прокрутка |
| U5 | PASS | Функциональные ids/поля/payload сохранены; combined содержит обе группы; остаток доступен через внутренние области |
| U6 | PASS | Native DOM + screenshots: ГСН 131250, ГСВ 105525, combined 145950; НДС 5% |
| U7 | PASS | САКЗ 0 → ПК disabled/unchecked; САКЗ 1 → enabled/checked; switch режимов; реальный HTTP 422 и видимая ошибка |
| U8 | PASS | Mobile 390×844: scrollWidth=clientWidth=375; поля/опции/кнопка доступны |
| U9 | PASS | Только 4 product/test файла; protected paths без diff; targeted 33 OK/exit 0; geometry assertions обновлены без ослабления |
| U10 | PASS | Inline local assets; resource entries=[]; reduced-motion matches=true/animation none |
| U11 | PASS | Реальные before 1050×740 и after 800×540/760×520, DPI 96; размеры/manifest подтверждены |
| U12 | PASS | Desktop кадры — native viewport при scrollY=0; PrintWindow bitmap ограничен outer rect; full-page/склейки нет; скрытого обрезания нет |

## Findings (MINOR backlog, не блокируют PASS)

- **F1 (MINOR, U3)** — `frontend/index.html`: section-label 10,5 px и
  field-label 11,5 px ниже ориентира 13–14 px; body/input 13 px. Воспроизведение:
  fontSizes в `RD-05-native.json` и target/min 1:1. Закрытие backlog — увеличить
  подписи с повторными visual/overflow метриками либо закрепить типографическую
  иерархию.
- **F2 (MINOR, diagnostics/scope)** — `app/desktop_launcher.py`: опциональный
  файловый `--eval-bridge PATH` исполняет JS только при явном флаге; default
  `None`, без флага поток не стартует, нового listener нет, обычный запуск не
  меняется. Закрытие backlog — отделить как dev-only либо добавить узкую
  проверку opt-in/lifecycle.

## Evidence

`docs/workflow/evidence/RD-05-evidence.md`, логи
`docs/workflow/evidence/logs/RD-05-*`, screenshots
`docs/screenshots/rd-05-*` (20 файлов), frozen checklist
`docs/workflow/tasks/RD-05.md`. Reviewer переиспользовал evidence, полный suite
и сценарии не перезапускал; сравнил SHA256 четырёх изменённых файлов и 20
screenshots с `RD-05-artifacts.txt` — совпали.

## Счётчики

- RD-05: A1/C1, full reviews с вердиктом 1 (PASS), failed reviews 0,
  Codex calls 1 (R2 reserve ≤4/3M). R1 Pro BLOCKED — capability, не failed
  review и не full review с вердиктом.
- Прежние счётчики не изменены: RD-01 1/0/0, RD-02 1/0/1, RD-03 2/1/2,
  RD-04/FINAL R0 0, stage1 R3 1.

## Дальше

Scoped local commit RD-05, затем dispatch RD-06 (R2: пересборка
package/installer, legacy, установка и реальные native screenshots).
