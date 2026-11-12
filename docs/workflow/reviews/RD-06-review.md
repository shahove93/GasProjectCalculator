# RD-06 — независимая приёмка package/installer/real program

- Логический TASK: RD-06, подход A1, цикл **C1**.
- Исполнитель: Orca OpenCode/DeepSeek Flash worker `ctx_94c225a27a49`
  (`task_cfc31f1035c5`).
- Reviewer: независимый Codex R2 `ctx_9656110c3af4`
  (`task_60a2a42b9b63`, `gpt-6.1-sol` high), read-only.
- Baseline RD-05 `1af13d6`; dispatch HEAD `7ce34f2`; review HEAD `edd36f4`
  (координаторские docs-only STATE/HISTORY).
- Основной образец: `docs/design/original-window-splash-reference.png`.

## Вердикт C1: FAIL

B1–B6 и B8–B11 — PASS; **B7 FAIL** (RD06-F01, MAJOR). Продуктовый diff от
`1af13d6` пуст; артефакты и hashes совпадают; installer/build/install/restore
подтверждены; evidence reuse RD-02/RD-03/RD-05 обоснован; rerun=0, файловых
изменений reviewer не делал.

| ID | Вердикт | Основание |
| --- | --- | --- |
| B1 | PASS | package+installer exit 0; dist exe 6 836 651 B `5403540C…DD2C`; installer 15 286 980 B `71232EE4…7E08` |
| B2 | PASS | legacy pre-compact 15 273 647 B `04388410…949A`; previous-stage 15 256 037 B `2973278F…428F` не тронут |
| B3 | PASS | изолированная установка в temp, backup/restore HKCU/ярлыка, пользовательская установка/PID13248 не изменены |
| B4 | PASS | установленный exe hash = dist; запуск без Python, PE subsystem GUI |
| B5 | PASS | installed target/min 800×540/760×520, client 784×501/744×481, DPI96, 3 режима scrollY=0, action+итог видимы |
| B6 | PASS | 131250/105525/145950, САКЗ/ПК, switch/422 подтверждены |
| B7 | **FAIL** | `docs/screenshots/rd-06-installed-mobile-390x844.png` — stitched/duplicated header около y=426, обрезанные полосы справа около x=362, кнопка не показана; противоречит metrics hScroll=false в `RD-06-mobile-390.txt`/evidence |
| B8 | PASS | splash/ready, loopback, port conflict, close; reuse обоснован |
| B9 | PASS | uninstall test instance + restore; user files/установка по умолчанию не затронуты |
| B10 | PASS | продуктовый diff пуст; protected paths без изменений; full suite оставлен RD-07 |
| B11 | PASS | новый artifact локальный; signing/push/merge/deploy отсутствуют; test-процессов/портов не осталось |

## Finding

**RD06-F01 (MAJOR, B7, OPEN)** — mobile evidence gap, не утверждение дефекта
CSS. Файл `docs/screenshots/rd-06-installed-mobile-390x844.png` (SHA256
`BA0D59196C6457407F2E5F5574BF8722E7E93339370F586ED92889FA59D9455C`)
содержит повтор шапки и горизонтально обрезанные соседние полосы; это
full-page/склейка, а не цельный настоящий viewport 390×844. Ожидается один
реальный viewport-снимок 390×844 (при `scrollY=0`) без дублирования и
horizontal clipping, плюс согласованные metrics (scrollWidth==clientWidth,
hScroll=false) и команда/CWD/revision/exit/cleanup. Закрытие — bounded C2
capture того же rebuilt installed artifact, без изменения продукта.

## C2 (повторный полный review): PASS

Повторный полный Codex R2 `ctx_1a3e73e23fcb` (`task_73c34faf0b72`,
`gpt-6.1-sol` high), read-only, финальный HEAD `630c2dc`, вернул **PASS** по
B1–B11. **RD06-F01 CLOSED**: основной `rd-06-installed-mobile-390x844.png`
(82 172 B, SHA256 `FFB84856…43A5`) — настоящий viewport 390×844, одна шапка,
кнопка видна, без horizontal clipping; metrics 375/375, 889/844, scroll 0/0,
hScroll=false, max right edge 375. Старый `BA0D…455C` явно SUPERSEDED;
C1 FAIL/finding/hash/описание сохранены. Артефакты: installer
15 286 980 B `71232EE4…7E08`; legacy pre-compact `04388410…949A`;
previous-stage `2973278F…428F`; dist/installed exe `5403540C…DD2C`;
source/packaged index `60B15F15…4037`. Test instance/порты убраны,
пользовательская установка/PID13248 и `:8000`/`:8138` не тронуты.
Evidence reuse, runtime/build/install/suite rerun=0.

**RD06-F02 (MINOR, B7 supplementary, OPEN backlog)** — вспомогательный
`rd-06-installed-mobile-390x844-result.png` не доказывает заявленный
scrollY=45: верхние 45 строк пустые, область x0..374/y129..843 пиксель-в-пиксель
совпадает с первым кадром; основной B7 proof полностью подтверждён первым PNG.
Закрытие backlog — аннотировать кадр как вспомогательный либо переснять
согласованный scroll-кадр; новой correction/full review не требуется.

## Счётчики

- RD-06: A1/C2, full reviews с вердиктом **2** (C1 FAIL, C2 PASS),
  failed reviews **1**, Codex calls **2** (R2 reserve ≤4/3M).
- RD06-F01 CLOSED; RD06-F02 MINOR backlog.
- Прежние счётчики не изменены: RD-01 1/0/0, RD-02 1/0/1, RD-03 2/1/2,
  RD-04/FINAL R0 0, RD-05 1/0/1, stage1 R3 1.

## Дальше

Scoped local commit RD-06, затем RD-07 (R0: один полный suite на финальном
интегрированном состоянии, artifact/evidence reuse), затем Codex R3 stage
acceptance и итоговый отчёт.
