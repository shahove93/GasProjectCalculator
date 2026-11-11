# Evidence — TASK GSV-03 (R1 retry): browser verification

- Исполнитель: Orca dispatch `ctx_513a316e9b89`, task `task_9c1860cce2f1`,
  agent opencode, requested model `deepseek/deepseek-flash`.
- Workspace: `D:/Antigravity/GasProjectCalculator`; ветка `feature/gsv`;
  baseline HEAD `dab59a94c86c8c6251c6f68d3d29bf6fa531de90`.
- В рабочем дереве на старте уже был `M frontend/index.html` от предыдущей
  попытки (`git diff --stat`: `frontend/index.html | 587 +, 82 -`). В этой
  попытке продуктовый код не менялся: по frozen checklist дефектов не найдено.
- Изменения исполнителя: только новые скриншоты `docs/screenshots/gsv-03-*.png`
  и этот evidence-файл. Коммитов и push нет.

## Окружение и сервер

1. `Test-Path .\.venv\Scripts\python.exe` → `True`; порт 8011 был свободен.
2. Запуск сервера:
   `$p = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList '-m','uvicorn','app.main:app','--port','8011' -WorkingDirectory "D:\Antigravity\GasProjectCalculator" -PassThru -WindowStyle Hidden; $p.Id | Set-Content C:\Users\user\AppData\Local\Temp\opencode\gsv03b-uvicorn.pid; Start-Sleep -Seconds 4; (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8011/).StatusCode`
   → `200` (CWD `D:/Antigravity/GasProjectCalculator`).
3. `orca tab create --url http://127.0.0.1:8011 --worktree current --json`
   → `ok: true`, `browserPageId = fb70063c-6031-4d93-963c-3aedf6c7ec15`.
4. Все браузерные команды ниже выполнялись с `--page fb70063c-6031-4d93-963c-3aedf6c7ec15`
   из CWD `D:/Antigravity/GasProjectCalculator`; каждая вернула `ok: true`
   (exit code 0 процесса `orca`).

## C1–C8: результат проверки

- C1: селектор трёх режимов `data-mode="gsn|gsv|combined"` — переключение
  кнопками работало. PASS.
- C2: в режиме ГСН поля прежние, расчёт ушёл в `/calculate` (суммы ГСН
  совпали с эталоном). PASS.
- C3: поля ГСВ `length`, `diameter`, `drilling_holes`, `sakz_sets`, `has_panel`,
  район; расчёт через `/calculate/gsv`. PASS.
- C4: combined — общие `customer_type`/район, отдельные параметры разделов,
  детализация обоих разделов и общие subtotal/vat/total через
  `/calculate/combined`. PASS.
- C5: ПК disabled+unchecked при САКЗ 0, доступен при 1, сбрасывается в
  unchecked+disabled при возврате к 0. PASS.
- C6: смена режима очищает прежний результат и ошибку (возвращается
  placeholder). PASS.
- C7: client validation диаметра 1..57 и целых ≥0; серверный 422 показывается
  понятным сообщением. PASS (см. раздел «Ошибка диаметра»).
- C8: desktop- и mobile-скриншоты ниже; на mobile
  `scrollWidth <= innerWidth`. PASS.

## Сценарий 1 — ГСН, desktop

Ввод: режим ГСН, `customer_type=частное лицо`, район вкл., длина 14,
углы 2, ГНБ выкл., экскаватор 4 ч, гидромолот/ГРПШ выкл.

Команды:

```sh
orca fill --page <id> --element e10 --value "14" --json
orca fill --page <id> --element e11 --value "2" --json
orca fill --page <id> --element e14 --value "4" --json
orca click --page <id> --element e9 --json        # Объект в районе
orca click --page <id> --element e4 --json        # Рассчитать стоимость
orca screenshot --page <id> --json
```

Результат (текст страницы после клика): базовая 65 000 ₽; доплата за длину
12 000 ₽; углы 6 000 ₽; экскаватор 15 000 ₽; район 7 000 ₽;
**подытог 105 000 ₽, НДС 5 250 ₽, итого 110 250 ₽** — совпадает с эталоном.

- Скриншот: `docs/screenshots/gsv-03-gsn-desktop.png`.
- Viewport: desktop по умолчанию (viewport не переопределялся).

## Сценарий 2 — ГСВ, desktop

Ввод: режим ГСВ, частное лицо, район вкл., длина 8, диаметр 25, отверстий 2,
САКЗ 1, ПК вкл.

Команды (после `orca click --element e7`):

```sh
orca fill --page <id> --element e15 --value "8" --json
orca fill --page <id> --element e16 --value "25" --json
orca fill --page <id> --element e17 --value "2" --json
orca fill --page <id> --element e18 --value "1" --json
orca click --page <id> --element e23 --json        # ПК
orca click --page <id> --element e4 --json
orca screenshot --page <id> --json
```

Результат: базовая 60 000 ₽; длина 7 500 ₽; бурение 8 000 ₽; САКЗ 14 000 ₽;
ПК 4 000 ₽; район 7 000 ₽; **подытог 100 500 ₽, НДС 5 025 ₽,
итого 105 525 ₽** — совпадает с эталоном.

- Скриншот: `docs/screenshots/gsv-03-gsv-desktop.png`.
- Viewport: desktop по умолчанию.

## Сценарий 3 — Combined, desktop

Ввод: режим «ГСН + ГСВ», частное лицо, район вкл.; ГСН 10 м, углы 0, ГНБ и
экскаватор 0, гидромолот/ГРПШ выкл.; ГСВ 5 м, Ø25, отверстий 0, САКЗ 0, ПК
недоступен/выкл.

Команды:

```sh
orca click --page <id> --element e8 --json
orca fill --page <id> --element e10 --value "10" --json
orca fill --page <id> --element e11 --value "0" --json
orca fill --page <id> --element e14 --value "0" --json
orca fill --page <id> --element e15 --value "5" --json
orca fill --page <id> --element e16 --value "25" --json
orca fill --page <id> --element e17 --value "0" --json
orca fill --page <id> --element e18 --value "0" --json
orca click --page <id> --element e4 --json
orca screenshot --page <id> --json
```

Результат: ГСН базовая 65 000 ₽ + район 7 000 ₽ → **итого по ГСН 75 600 ₽**;
ГСВ базовая 60 000 ₽ + район 7 000 ₽ → **итого по ГСВ 70 350 ₽**;
**общий подытог 139 000 ₽, НДС 6 950 ₽, итого 145 950 ₽** — совпадает с
эталоном.

- Скриншот: `docs/screenshots/gsv-03-combined-desktop.png`.
- Viewport: desktop по умолчанию.

## C6 — смена режима очищает результат

После показа combined-результата выполнен `orca click --page <id> --element e6`
(ГСН). Снимок страницы: удалено 50 строк результата, заголовок стал
«Расчёт стоимости — ГСН», в панели снова виден placeholder
«Укажите параметры объекта и нажмите «Рассчитать стоимость»». Ранее то же
наблюдалось при переходе ГСВ → combined и ГСН → ГСВ.

## C5 — ПК и САКЗ (desktop)

- Начальное состояние (САКЗ 0): snapshot
  `checkbox [checked=false, disabled, ref=e23]`.
- После `fill e18 = 1`: `checkbox [checked=false, ref=e23]` (disabled снят).
- После `click e23`: `checkbox [checked=true, ref=e23]`.
- После `fill e18 = 0`: `checkbox [checked=false, disabled, ref=e23]` —
  значение сброшено и поле снова недоступно.

## C7 — ошибка диаметра

1. Client validation: при режиме ГСВ введён диаметр 58 и нажата кнопка расчёта.
   Браузерная проверка `max=57` не дала отправить форму и показала видимое
   сообщение `Значение должно быть меньше или равно 57.`
   Скриншот: `docs/screenshots/gsv-03-diameter-error-desktop.png`.
2. Серверный 422 и его понятное отображение проверены реальным запросом из
   страницы (обход нативной блокировки ввода, payload с `diameter=58`):

```sh
orca eval --page <id> --expression "(async () => { const r = await fetch('/calculate/gsv',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({customer_type:'частное лицо',length:5,diameter:58,drilling_holes:0,sakz_sets:0,has_panel:false,is_district:false})}); const j = await r.json(); return JSON.stringify({status:r.status, detail:j.detail, message: formatApiError(j)}); })()" --json
```

   Результат: `status: 422`, detail `less_than_equal` по `body.diameter`,
   сообщение через `formatApiError`: `Диаметр: должно быть не больше 57`.

## C8 — mobile verification (390×844, mobile)

Команда: `orca viewport --page <id> --width 390 --height 844 --mobile --json`
→ `{width:390, height:844, deviceScaleFactor:1, mobile:true}`, `ok: true`.

Повторён ГСВ-сценарий (8 м, Ø25, 2 отверстия, 1 САКЗ, ПК, район): суммы
**100 500 / 5 025 / 105 525 ₽** — те же, что на desktop.
Скриншот: `docs/screenshots/gsv-03-gsv-mobile.png`.

Повторён combined-сценарий (ГСН 10 м без опций, ГСВ 5 м Ø25 без опций, район):
**ГСН 75 600 ₽, ГСВ 70 350 ₽, общий 139 000 / 6 950 / 145 950 ₽** — те же.
Скриншот: `docs/screenshots/gsv-03-combined-mobile.png`.

Проверка переполнения для обоих mobile-состояний:

```sh
orca eval --page <id> --expression "JSON.stringify({scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth, fits: document.documentElement.scrollWidth <= window.innerWidth})" --json
```

→ `{"scrollWidth":390,"innerWidth":390,"fits":true}` в обоих случаях
(горизонтального скролла нет).

## Остановка сервера

`Stop-Process -Id (Get-Content C:\Users\user\AppData\Local\Temp\opencode\gsv03b-uvicorn.pid)`;
последующий `Invoke-WebRequest http://127.0.0.1:8011/` завершился ошибкой
соединения — сервер остановлен.

## Полный suite

`.\.venv\Scripts\python.exe -m unittest discover -s tests`
(CWD `D:/Antigravity/GasProjectCalculator`):

```text
Ran 131 tests in 0.152s

OK
EXIT:0
```

(в stderr присутствует только `StarletteDeprecationWarning` про httpx2;
exit code 0.)

## git status --short (на момент завершения)

```text
 M frontend/index.html
?? docs/screenshots/gsv-03-combined-desktop.png
?? docs/screenshots/gsv-03-combined-mobile.png
?? docs/screenshots/gsv-03-diameter-error-desktop.png
?? docs/screenshots/gsv-03-gsn-desktop.png
?? docs/screenshots/gsv-03-gsv-desktop.png
?? docs/screenshots/gsv-03-gsv-mobile.png
?? docs/workflow/evidence/GSV-03-browser.md
```

`M frontend/index.html` — существовавшее до этой попытки изменение предыдущего
исполнителя; новых правок продуктового кода нет. Коммит не выполнялся.
