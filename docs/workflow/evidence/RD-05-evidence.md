# RD-05 evidence — компактный UI и native geometry

Исполнитель: отдельный Orca OpenCode/DeepSeek Flash worker (task_dc32b3365d51,
dispatch ctx_b847d4877268). Это evidence исполнителя, не project PASS и не
приёмка. Ревьюер/координатор выносят решение отдельно.

Этот прогон — корректировка presentation после уточнения пользователя
(commit `98ffa83`): основной образец теперь
`docs/design/original-window-splash-reference.png`,
`docs/design/approved-variant-1-reference.png` — вспомогательный только для
эмблемы/названия.

## Workspace / revisions

- CWD: `D:\Antigravity\GasProjectCalculator`
- Ветка: `feature/ss-calculator-redesign`
- Продуктовый baseline: `4b0be03`
- Во время RD-05 координатор добавил docs-only commits `f8d8964`, `17ae4c8`,
  `98ffa83`, `2c0fff1`. Финальный HEAD worktree: `2c0fff1`. Продуктовые
  изменения RD-05 остаются незакоммиченными (commit — координатор после routed
  PASS). Посторонних незакоммиченных изменений не осталось: прежние
  `COMPACT-CORRECTION-BRIEF.md` и `REFERENCE-CLARIFICATION-2026-11-12.md`
  учтены в docs-коммитах координатора.
- Не трогались: `app/main.py`, calculators, requirements/API, `installer/`,
  `packaging/`, VISION/ARCHITECTURE/ROADMAP/workflow docs (кроме RD-05 evidence),
  `.venv`, пользовательские процессы/сессии. `:8000` PID12888 и `:8138`
  PID23152 не затрагивались.

## Изменено

- `frontend/index.html` — только presentation/CSS/разметка по основному
  референсу `original-window-splash-reference.png`: компактная тёмная шапка с
  круглой эмблемой, названием `СС.Расчет`, подписью и более заметной трубой с
  жёлтым вентилем; строка режимов внутри шапки; отдельная строка заказчика без
  «Объект в районе»; левая колонка — карточка параметров парами и **отдельная
  компактная карточка «Дополнительные параметры»** (район, гидромолот, ГРПШ, ПК
  только при САКЗ); справа тёплая карточка «Итого с НДС» и кнопка; нижняя труба
  с домом/пламенем/вентилем. Все функциональные `id`, режимы, обработчики и
  payload сохранены; добавлена только presentation-логика видимости опций по
  режиму (`updateOptionVisibility`), не меняющая payload. Embedded emblem
  побайтно сохранён.
- `app/desktop_launcher.py` — geometry `APP_WIDTH=800`, `APP_HEIGHT=540`,
  `APP_MIN_SIZE=(760, 520)` и диагностический `--eval-bridge PATH` (инертен без
  флага; используется только для снятия DOM/JS-метрик из реального native окна).
- `tests/test_desktop_launcher.py` — только geometry assertions под новые
  утверждённые константы (разрешено координатором, вариант (a), строки 192–195).
- `tests/test_frontend_redesign.py` — presentation assertions: нет `zoom:` /
  `transform: scale`, body не маскирует horizontal overflow через
  `overflow-x: hidden`, есть внутренние scroll-области формы/детализации,
  опции находятся в отдельной карточке, а `is_district` — не в строке заказчика.

`git diff --stat` (см. `logs/RD-05-git.txt`):

```
 app/desktop_launcher.py         |  75 +++-
 frontend/index.html             | 970 ++++++++++++++++++++++++++--------------
 tests/test_desktop_launcher.py  |   6 +-
 tests/test_frontend_redesign.py |  37 ++
 4 files changed, 748 insertions(+), 340 deletions(-)
```

Diff protected paths (`app/main.py`, calculators, requirements, installer,
packaging) пуст.

## Native geometry и DPI (Win32)

| Состояние | outer | client | DPI | Источник |
| --- | --- | --- | --- | --- |
| До правок (current UI) | 1050×740 | 1034×701 | 96 | `before-window.json`, `rd-05-before-1050x740.png` |
| После, target | 800×540 | 784×501 | 96 | `RD-05-native.json`, PrintWindow screenshot |
| После, min (request 760×520) | 760×520 | 744×481 | 96 | `RESIZED` + metrics |
| Clamp probe (request 400×300) | 760×520 | 744×481 | 96 | `rd-05-after-clamp-probe.png` |

Площадь окна уменьшена с 1050×740 до 800×540 (~56% прежней), min — 760×520.
Корректировка под реальный client area/DPI: client 784×501 / 744×481.

## Viewport / scroll metrics (реальное native окно, `scrollY=0`)

Метрики сняты через `evaluate_js` в WebView2 самого native окна
(`logs/RD-05-native.json`), не через внешний браузер.

| Размер | Режим | inner | window.scroll | doc scroll/client | body overflow | hScroll | vScroll | submit в viewport | итог в viewport |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| target 800×540 | ГСН | 784×501 | 0,0 | 784×501 / 784×501 | auto / hidden | нет | нет | да (bottom 439) | да (bottom 203) |
| target | ГСВ | 784×501 | 0,0 | 784×501 / 784×501 | auto / hidden | нет | нет | да | да |
| target | combined | 784×501 | 0,0 | 784×501 / 784×501 | auto / hidden | нет | нет | да | да |
| min 760×520 | ГСН | 744×481 | 0,0 | 744×481 / 744×481 | auto / hidden | нет | нет | да (bottom 419) | да (bottom 202) |
| min | ГСВ | 744×481 | 0,0 | 744×481 / 744×481 | auto / hidden | нет | нет | да | да |
| min | combined | 744×481 | 0,0 | 744×481 / 744×481 | auto / hidden | нет | нет | да | да |

- `scrollWidth == clientWidth` и `scrollHeight == clientHeight` во всех шести
  состояниях; page h/v scroll отсутствует при `scrollY=0`.
- `overflow-x: hidden` на body удалён: computed `overflow-x` = `auto`,
  horizontal overflow не маскируется. GСН/ГСВ полностью помещаются в карточку
  параметров без внутренней прокрутки: target 193/193 и 211/211 px, min
  173/173 и 182/182 px.
- Combined честно использует внутреннюю прокрутку: форма target 193/292 px,
  min 164/292 px; детализация target 189/199 px, min 171/199 px. Итог и кнопка
  находятся вне этих областей и постоянно видимы.
- Шрифты (computed): body 13 px, field label 11.5 px, input 13 px,
  total 22.7 px (target) / 21.6 px (min), button 13.5 px. CSS `zoom`/`scale`
  отсутствует (проверяется targeted test).

## Эталонные значения (реальные запросы/ответы в UI)

| Режим | Сценарий (RD-01) | Подытог | НДС 5% | Итого |
| --- | --- | --- | --- | --- |
| ГСН | юрлицо, район, 14 м, 2 угла, 4 ч экскаватора | 125 000 ₽ | 6 250 ₽ | **131 250 ₽** |
| ГСВ | физлицо, район, 8 м, Ø25, 2 отверстия, САКЗ 1 + ПК | 100 500 ₽ | 5 025 ₽ | **105 525 ₽** |
| combined | 10 м ГСН без опций + 5 м ГСВ Ø25 без опций, район | 139 000 ₽ | 6 950 ₽ | **145 950 ₽** |

Проверено в native UI (чтение DOM после реального submit) и на скриншотах
после расчёта.

## САКЗ/ПК и 422

- САКЗ=0 → switch ПК `disabled=true`, `checked=false`; САКЗ=1 → `disabled=false`,
  затем switch включается (`misc.sakzPanel`).
- Реальный 422 через UI: видимое сообщение
  «Тип заказчика: допустимы только «частное лицо» или «юридическое лицо»»;
  синхронный fetch из native-окна вернул HTTP 422 с `literal_error` по
  `customer_type`. Скриншот `rd-05-after-422.png`.

## Mobile / reduced motion / внешние ресурсы

- Mobile viewport 390×844 (Orca browser, реальный Chromium): combined режим —
  `scrollWidth=375 == clientWidth=375` (вертикальный scrollbar), horizontal
  overflow нет; вертикальная прокрутка 889 px, поля/опции доступны, кнопка
  «Рассчитать стоимость» достижима (bottom 800 при viewport 844). Скриншот
  `rd-05-after-mobile-390x844.png`. Это browser viewport, не native окно.
- Reduced motion (`set media --reduced-motion reduce`): `matches=true`,
  `.pipe-flow` `animation-name: none`, transition ≈0; скриншот
  `rd-05-after-reduced-motion.png`.
- Внешние ресурсы: `performance.getEntriesByType("resource")` = `[]`;
  в документе только inline `data:image/png;base64,...` эмблема. Внешних
  http(s)/CDN/шрифтов нет.

## Screenshots (real native, PrintWindow PW_RENDERFULLCONTENT)

- `docs/screenshots/rd-05-before-1050x740.png` — текущее окно до правок.
- `docs/screenshots/rd-05-after-target-gsn-before.png` / `...-gsn.png`
- `docs/screenshots/rd-05-after-target-gsv-before.png` / `...-gsv.png`
- `docs/screenshots/rd-05-after-target-combined-before.png` / `...-combined.png`
- `docs/screenshots/rd-05-after-min-gsn-before.png` / `...-gsn.png`
- `docs/screenshots/rd-05-after-min-gsv-before.png` / `...-gsv.png`
- `docs/screenshots/rd-05-after-min-combined-before.png` / `...-combined.png`
- `docs/screenshots/rd-05-after-422.png`
- `docs/screenshots/rd-05-after-min-probe.png`, `...-min-restored.png`,
  `...-clamp-probe.png`
- `docs/screenshots/rd-05-after-mobile-390x844.png`
- `docs/screenshots/rd-05-after-reduced-motion.png`
- `docs/screenshots/rd-05-compare-reference.png` — основной референс
  `original-window-splash-reference.png` (окно слева) рядом с реальным native
  окном 800×540. `approved-variant-1-reference.png` больше не основной образец
  (только эмблема/название).

После правок скриншоты снимались реальным Win32 `PrintWindow` с флагом
`PW_RENDERFULLCONTENT` (окно может быть за IDE; это не full-page workaround и
не склейка). Before — реальный `CopyFromScreen` окна 1050×740.

## Commands / exit codes

| Команда (CWD = workspace) | Exit |
| --- | --- |
| `.\.venv\Scripts\python.exe -m py_compile app\desktop_launcher.py` | 0 |
| `.\.venv\Scripts\python.exe -m unittest tests.test_frontend_redesign tests.test_desktop_launcher -v` (33 tests) | 0 |
| `.\.venv\Scripts\python.exe -m app.desktop_launcher --preferred-port 8160 --port-file ... --eval-bridge ...` | запущен, затем корректно закрыт worker'ом |
| `.\.venv\Scripts\python.exe ...\drive_native.py 27168` | 0 |
| `orca tab create/eval/exec/screenshot/set media` | 0 |

Логи: `logs/RD-05-targeted-tests.txt`, `logs/RD-05-native.json`,
`logs/RD-05-git.txt`, `logs/RD-05-artifacts.txt`,
`logs/RD-05-before-window.json`, `logs/RD-05-before-launcher.log`,
`logs/RD-05-native-launcher.log`, `logs/RD-05-native-driver.txt`.

## NOT_RUN

- Полный suite — не запускался (по плану один раз в RD-07).
- Пересборка/установка installer, подпись, release — не выполнялись
  (отдельный этап; evidence installer переиспользуется позже).
- R1/R2/R3 review и project PASS — не выставлялись.
- Push/merge/deploy — не выполнялись.
- API/calculators/requirements не менялись и не перепроверялись полным suite.

## Known risks / notes

- В `app/desktop_launcher.py` добавлен диагностический `--eval-bridge`; он не
  активен без флага, не меняет нормальный запуск и не добавляет сеть. Ревьюеру
  стоит подтвердить приемлемость этого диагностического хука.
- Combined в target/min требует внутренней прокрутки формы и детализации; это
  заявленное поведение U4/U5 (итог и действие постоянно видимы). GСН/ГСВ
  полностью помещаются без внутренней прокрутки на target и min.
- Опции вынесены из карточек параметров в отдельную карточку. Чтобы режимные
  опции не показывались в чужом режиме, в `setMode` добавлена только
  presentation-функция `updateOptionVisibility`; payload, обработчики и
  значения не изменены. В combined видны все четыре опции, ПК остаётся
  disabled без САКЗ.
- Заставка не менялась: остаётся отдельным стартовым окном с прежним
  lifecycle/reduced-motion; `frontend/splash.html` вне allowlist.
- Обновление `tests/test_desktop_launcher.py` — только ожидаемые geometry
  значения, по явному разрешению координатора; прочие проверки не ослаблены.
- Before-скриншот снят CopyFromScreen, after — PrintWindow; оба реальные и
  сопоставимы по outer size (1050×740 vs 800×540).
- Собственные test backend/окно закрыты после проверок; чужие процессы не
  затрагивались.
