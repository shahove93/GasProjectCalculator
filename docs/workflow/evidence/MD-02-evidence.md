# MD-02 evidence — три длины ГСВ в UI, серверная детализация, artwork

Дата: 2026-11-12. Исполнитель: OpenCode Flash (Orca dispatch MD-02).
Reviewer: Codex `gpt-6.1-sol` high (R2, vision). **Product verdict: NOT_REVIEWED**
(исполнитель не выставляет PASS).

## Baseline, workspace, scope

- Workspace/CWD: `D:\Antigravity\GasProjectCalculator`.
- Ветка: `feature/gsv-mixed-diameters` (не переключалась).
- Baseline HEAD: `1d77194d777963214e83bb2ad63bcf0b431b5485` — MD-01 R2 PASS
  (`feat(gsv): mixed three-diameter lengths with legacy-compatible API`).
- Изменённые tracked-файлы (только allowlist):
  `frontend/index.html`, `tests/test_frontend_redesign.py`.
- `frontend/assets/**`, `frontend/splash.html`, `app/**`, installer/packaging,
  requirements, VISION/ARCHITECTURE/ROADMAP/workflow docs не изменялись.
- Новые файлы: `docs/screenshots/md-02-*`, `docs/workflow/evidence/logs/MD-02-*`,
  этот evidence. Коммит/push/merge/deploy/release не выполнялись.

Diff и scope: `logs/MD-02-baseline.txt`, `logs/MD-02-diff-stat.txt`,
`logs/MD-02-changed-files.txt`, `logs/MD-02-scope.txt`.

```text
frontend/index.html             | 570 ++++++++++++++++++++++++++++++++++------
tests/test_frontend_redesign.py |  59 ++++-
2 files changed, 550 insertions(+), 79 deletions(-)
```

## Что изменено

### Ввод и payload

- В `#group-gsv` (режим ГСВ и общая смета) вместо `gsv-length`/`gsv-diameter`
  три поля: `gsv-length-up-to-25` (`до Ø25`), `gsv-length-32-40` (`Ø32–40`),
  `gsv-length-57` (`Ø57`); `type=number`, `min=0`, `step=1`, ноль = нет
  позиции.
- Payload ГСВ и `combined.gsv` содержит только
  `pipe_lengths: {up_to_25, from_32_to_40, diameter_57}`; legacy
  `length`/`diameter` в UI не отправляются.
- Клиент не вычисляет `total`, `total_length` или `length_surcharge`:
  общий метраж и строки `pipe_breakdown` берутся из ответа сервера
  (`total_length`, `pipe_breakdown[]`), включая нулевые позиции.
- Детализация в обеих формах: общий метраж + таблица
  `category/length/included_length/billable_length/rate/surcharge`.
  Ставки отображаются как 2 500 / 3 500 / 4 000; в заголовках указано, что
  ставка и сумма в рублях (в ячейках компактной таблицы `₽` опущен, чтобы
  значения полностью помещались на 760×520).

### Artwork

- Верх: inline SVG `viewBox 0 0 360 96` — объёмная бирюзовая труба с
  металлическими муфтами, золотистым вентилем, мягким teal-свечением на
  тёмно-синем фоне; широкий баннер справа от бренда.
- Низ: inline SVG `viewBox 0 0 760 60` — труба с муфтами, голубое пламя слева,
  дом с тёплым окном справа, лёгкий пейзаж; высота полосы 54 px (mobile 58 px).
- `СС.Расчет`, подзаголовок и круглая эмблема сохранены. Внешних сетевых
  ресурсов нет. Компактность не достигается zoom/scale; overflow не
  маскируется page-level hidden.

## Окружение проверки и владение процессами

| Что | Значение |
| --- | --- |
| Backend (browser) | Orca terminal `term_0c4f6594-f91d-4990-9458-4ab50eb78675` (terminal pid 25108), listener pid 8668, `127.0.0.1:8022`, HTTP 200 |
| Desktop launcher | Orca terminal `term_b1d4c5be-6eb6-4b09-85b6-67186efb0114` (terminal pid 21876), launcher pid 20820, backend `127.0.0.1:8023`, port-file ready |
| Browser | Orca tab page `2854ab60-a2bb-4cef-8fdc-977aa1296a2d` |
| Native window | pywebview main window PID 20820, DPI 96 |

Порты `:8000` и root-owned `:8138` не использовались. Свои процессы
остановлены после проверок (см. «Остановка»). Доказательство:
`logs/MD-02-port-ownership.txt`.

## Команды и exit

| Проверка | Команда | CWD | Exit |
| --- | --- | --- | --- |
| Targeted frontend tests | `.\.venv\Scripts\python.exe -m unittest tests.test_frontend_redesign -v` | workspace | 0 (13 OK) |
| Full suite | `.\.venv\Scripts\python.exe -m unittest discover -s tests` | workspace | 0 (219 OK) |
| Frontend script syntax | `node --check <extracted script>` | workspace | 0 |
| Static URL scan | `Select-String frontend/index.html,frontend/splash.html -Pattern 'https?://'` | workspace | no matches |
| Browser verification | `orca tab create/fill/click/eval/screenshot` + `orca exec set viewport` | workspace | 0 |
| Native verification | `.\.venv\Scripts\python.exe app.desktop_launcher ... --eval-bridge ...` + `drive_native.py 20820 8023` | workspace | 0 |

Полный вывод suite: `logs/MD-02-suite.txt` (219 tests OK), exit 0:
`logs/MD-02-suite-exit.txt`.

## Browser verification (Orca browser, Chromium)

Viewport 800×540, `scrollY=0` после каждого расчёта. Источник точных
значений — `logs/MD-02-browser.json` и `logs/MD-02-browser-summary.txt`.
Скриншоты: `docs/screenshots/md-02-browser-desktop-*`.

### U1/U2 — поля и payload

- В режиме ГСВ и combined доступны три поля с подписями `до Ø25`,
  `Ø32–40`, `Ø57`; `document.getElementById('gsv-length')` и
  `gsv-diameter` отсутствуют (DOM assertions).
- Реально перехваченный запрос из UI:

```json
{"url":"/calculate/gsv","body":"{\"customer_type\":\"частное лицо\",\"is_district\":false,\"pipe_lengths\":{\"up_to_25\":4,\"from_32_to_40\":0,\"diameter_57\":4},\"drilling_holes\":0,\"sakz_sets\":0,\"has_panel\":false}"}
```

`pipeKeys = up_to_25, from_32_to_40, diameter_57`; `hasLegacy = false`.
Для combined перехвачен `combined.gsv.pipe_lengths` с теми же тремя ключами
и без legacy-полей.

### U3/U4 — серверная детализация и эталоны D1–D5

| Case | Длины (до25/32–40/57) | Метраж | Доплата | Подытог | НДС | Итог |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| D1 | 4 / 0 / 4 | 8 м | 12 000 | 72 000 | 3 600 | **75 600** |
| D2 | 2 / 4 / 3 | 9 м | 15 500 | 75 500 | 3 775 | **79 275** |
| D3 | 0 / 5 / 2 | 7 м | 8 000 | 68 000 | 3 400 | **71 400** |
| D4 | 3 / 1 / 1 | 5 м | 0 | 60 000 | 3 000 | **63 000** |
| D5 | 8 / 0 / 0 | 8 м | 7 500 | 67 500 | 3 375 | **70 875** |

Пример детализации D1 из DOM (все значения — из `pipe_breakdown` ответа):
`до Ø25: 4 м / 4 м / 0 м / 2 500 / 0`,
`Ø32–40: 0 м / 0 м / 0 м / 3 500 / 0`,
`Ø57: 4 м / 1 м / 3 м / 4 000 / 12 000`.
Нулевые позиции отображаются. Скриншоты D1–D5:
`md-02-browser-desktop-gsv-d1..d5.png`;
нативный D1: `md-02-native-target-gsv.png`.

### U5 — САКЗ/ПК, район, НДС

- САКЗ 0 → ПК `disabled=true, checked=false`; САКЗ 1 → `disabled=false`;
  возврат к 0 → ПК снова `checked=false, disabled=true`
  (`logs/MD-02-native-summary.txt`, `misc.sakzPanel`).
- В ГСВ D1 + 1 САКЗ + ПК + район: 60 000 + 12 000 + 14 000 + 4 000 +
  7 000 = 97 000; НДС 4 850; итог **101 850 ₽** (браузерный DOM).
- Combined: ГСН 10 м + район (75 600 ₽) и ГСВ 4/0/4 + район (82 950 ₽),
  общий подытог **151 000 ₽**, НДС **7 550 ₽**, итог **158 550 ₽** —
  совпадает с утверждённым PLAN. Скриншоты:
  `md-02-browser-desktop-combined.png`,
  `md-02-native-target-combined.png`, `md-02-native-target-combined-detail.png`.

### U6 — 422 и очистка при смене режима

- Реальный серверный 422 (ПК при 0 САКЗ): ошибка видима,
  текст `body: ПК доступен только при наличии хотя бы одного комплекта САКЗ`,
  результат скрыт. Скриншот `md-02-browser-desktop-422.png`, нативный
  `md-02-native-422.png`.
- Смена режима: заголовок «Расчёт стоимости — ГСН», placeholder видим,
  ошибка скрыта, все три result-контейнера `display:none`.
  Скриншот `md-02-browser-desktop-after-switch-clear.png`.

## Native verification (реальное окно desktop launcher)

Win32 `PrintWindow` c `PW_RENDERFULLCONTENT`, DPI 96.

| Состояние | outer | client | DPI |
| --- | --- | --- | --- |
| target | 800×540 | 784×501 | 96 |
| min | 760×520 | 744×481 | 96 |

| Размер | Режим | Итог | scroll | hScroll/vScroll | submit в viewport | итог в viewport | таблица влезает |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| target | ГСН | 68 250 ₽ | 0,0 | нет/нет | да | да | — |
| target | ГСВ | 75 600 ₽ | 0,0 | нет/нет | да | да | да |
| target | combined | 158 550 ₽ | 0,0 | нет/нет | да | да | да |
| min | ГСН | 68 250 ₽ | 0,0 | нет/нет | да | да | — |
| min | ГСВ | 75 600 ₽ | 0,0 | нет/нет | да | да | да |
| min | combined | 158 550 ₽ | 0,0 | нет/нет | да | да | да |

`body overflow-x: auto`, `overflow-y: hidden`; страница не имеет
h/v scroll, компактность реальная (без zoom/scale). Combined использует
внутреннюю прокрутку детализации; итог и кнопка вне её и видимы. Для
U3 combined-детализация дополнительно снята после внутреннего скролла:
`md-02-native-target-combined-detail.png`,
`md-02-native-min-combined-detail.png`.

Полные метрики: `logs/MD-02-native.json`, `logs/MD-02-native-summary.txt`.
Скриншоты target/min всех трёх режимов:
`md-02-native-target-{gsn,gsv,combined}.png`,
`md-02-native-min-{gsn,gsv,combined}.png` (+ `-before`).

## Mobile 390×844

`logs/MD-02-mobile.json`, `logs/MD-02-mobile-gsn.json`; скриншоты
`md-02-browser-mobile-390x844-gsn.png`,
`md-02-browser-mobile-390x844-gsv.png`,
`md-02-browser-mobile-390x844-combined.png`.

- ГСН: `inner=390×844`, `hScroll=false`, `vScroll=false`, итог 75 600 ₽
  (10 м + район), кнопка и итог в viewport (`MD-02-mobile-gsn.json`).
- ГСВ: `inner=390×844`, `hScroll=false`, `vScroll=false`, итог 75 600 ₽,
  кнопка и итог в viewport; таблица помещается.
- Combined: `doc=[375,1186]`, `client=[375,844]`, `hScroll=false`,
  `vScroll=true`; итог 158 550 ₽ видим, ключевое действие доступно
  вертикальным скроллом (одна колонка); горизонтального overflow нет,
  таблица помещается.

## Artwork mapping к референсам

- `docs/design/header-detail-reference.jpg` → верхний inline SVG:
  объёмная бирюзовая труба, металлические муфты, золотистый вентиль,
  мягкие блики/свечение, тёмно-синий фон, широкий баннер.
- `docs/design/footer-detail-reference.jpg` → нижний inline SVG:
  труба с муфтами, голубое пламя слева, дом с тёплым окном справа,
  лёгкий пейзаж, широкая нижняя полоса.
- `СС.Расчет` и круглая эмблема сохранены; старый title/числа/20% из
  референса не переносились.
- Side-by-side: `docs/screenshots/md-02-compare-header.png`,
  `docs/screenshots/md-02-compare-footer.png`.

## U9 — бренд и отсутствие внешних ресурсов

- DOM: `<title>СС.Расчет</title>`, `h1 > СС.Расчет`, эмблема — embedded
  `data:image/png;base64` (совпадает с `frontend/assets/company-emblem.png`).
- Static scan: в `frontend/index.html` и `frontend/splash.html` нет
  `http://`/`https://` ссылок; нет `@import`, `fonts.googleapis`.
- Browser `performance.getEntriesByType("resource")`: только same-origin
  POST-запросы `/calculate*`; `thirdParty=[]`, `styleSheetImports=0`
  (`logs/MD-02-mobile.json`).

## U12 — suite и scope

- Full suite: **219 tests OK**, exit 0 (`logs/MD-02-suite.txt`,
  `logs/MD-02-suite-exit.txt`). ГСН-путь не изменялся; старые API-тесты
  зелёные.
- Targeted frontend: 13 tests OK; новые assertions проверяют три поля,
  отсутствие legacy-полей в UI, payload `pipe_lengths`, серверные
  `total_length`/`pipe_breakdown`, отсутствие zoom/scale и внешних ресурсов.
- Diff — только allowlist (`logs/MD-02-diff-stat.txt`,
  `logs/MD-02-scope.txt`); `app/`, installer, packaging, docs workflow
  (кроме evidence) не менялись.

## Frozen acceptance checklist

| ID | Результат | Evidence |
| --- | --- | --- |
| U1 | PASS (три поля в ГСВ/combined, старых нет) | DOM assertions + `md-02-browser-desktop-gsv-d1.png`, `md-02-native-target-gsv.png` |
| U2 | PASS (`pipe_lengths` с тремя ключами, legacy не отправляется) | `MD-02-browser.json` payload; combined payload |
| U3 | PASS (метраж + length/included/billable/rate/surcharge из сервера) | DOM/JSON `MD-02-browser.json`; `*-combined-detail.png` |
| U4 | PASS (75 600 / 79 275 / 71 400 / 63 000 / 70 875) | `MD-02-browser-summary.txt`, D1–D5 screenshots |
| U5 | PASS (САКЗ→ПК, район, НДС; combined 158 550) | `MD-02-native-summary.txt`, browser DOM, combined screenshots |
| U6 | PASS (422 видим, смена режима очищает) | `md-02-browser-desktop-422.png`, `...after-switch-clear.png`, native 422 |
| U7 | PASS (объёмная труба, муфты, золотой вентиль, свечение, navy) | `md-02-native-target-gsv.png`, `md-02-compare-header.png` |
| U8 | PASS (труба, пламя, дом с тёплым окном, пейзаж) | `md-02-native-target-gsv.png`, `md-02-compare-footer.png` |
| U9 | PASS (`СС.Расчет`, эмблема, без внешних ресурсов) | static scan + network JSON + screenshots |
| U10 | PASS (800×540 / min 760×520, action+итог видны, без page scroll) | `MD-02-native.json`, native screenshots |
| U11 | PASS (mobile 390×844 все три режима без h overflow, итог/действие доступны) | `MD-02-mobile.json`, `MD-02-mobile-gsn.json`, mobile screenshots |
| U12 | PASS (три режима, ГСН без регрессии, suite 219 OK, diff в allowlist) | `MD-02-suite.txt`, `MD-02-diff-stat.txt` |

## NOT_RUN

- Installer/packaging/build — вне scope MD-02 (MD-03).
- Backend/API/calculator изменения — вне scope (MD-01).
- Commit/push/merge/deploy/release/signing — запрещены TASK; не выполнялись.
- Browser screenshots не заменяют native evidence; оба набора приложены.

## Риски / заметки

- В combined на 760×520 детализация ГСВ прокручивается внутри карточки;
  итог и кнопка остаются видимы, U10 не нарушен. Для U3 снят отдельный
  скролл-скриншот.
- В таблице детализации `₽` не повторяется в каждой ячейке: единица указана
  в заголовках/title, чтобы значения полностью помещались на минимальной
  ширине.
- Legacy `length`/`diameter` остаётся только API-контрактом MD-01; UI его
  не использует.
- Арт выполнен inline SVG, без новых файлов ассетов и без сетевых
  зависимостей.

## Итог для координатора

Все U1–U12 покрыты evidence; suite 219 OK, exit 0; изменения только в
allowlist. Продуктовый PASS не выставляется: требуется независимый Codex R2
review (vision для artwork) и решение координатора о scoped commit.
