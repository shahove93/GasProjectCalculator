# Evidence — TASK GSV-03 REGRESSION (R1): состояния UI после финальной приёмки

- Исполнитель: Orca dispatch `ctx_7f43727686c5`, task `task_b32cc76236e9`,
  терминал `term_6a806efc-38c3-4d38-9ae1-fb88d8d22da9`, agent opencode,
  requested model `deepseek/deepseek-flash`.
- Workspace: `D:/Antigravity/GasProjectCalculator`; ветка `feature/gsv`;
  baseline HEAD `0cd48bc1482b3b205beee270cb69290bb1d622e9`.
- Изменён только `frontend/index.html` (+55/−9). Добавлены новые скриншоты
  `docs/screenshots/gsv-03-initial-gsn.png`, `gsv-03-race-guard.png`,
  `gsv-03-hidden-validation.png`, `gsv-03-mobile.png` и этот evidence-файл.
  Коммитов, push и изменения файлов вне allowlist нет.

## Исправления в `frontend/index.html`

1. **FINAL-GSV-02 — реальное начальное состояние.** Добавлен вызов
   `setMode("gsn")` при загрузке; `setMode` скрывает/показывает группы и
   применяет заголовок. На старте видна только группа ГСН.
2. **FINAL-GSV-01 — защита от устаревшего ответа.** Введён счётчик
   `activeRequest`; при submit захватываются `requestId = ++activeRequest` и
   `mode`, после `fetch`/`json` ответ применяется только при
   `requestId === activeRequest && currentMode === mode`. `setMode` инкрементирует
   `activeRequest` и восстанавливает кнопку/текст.
3. **FINAL-GSV-03 — скрытые поля вне нативной валидации.** `setMode` через
   `setGroupEnabled` ставит `disabled = true` всем input/select/button скрытой
   группы и включает активную; для ГСН повторно вызывается
   `updateExcavatorAvailability()`, для ГСВ — `updatePanelAvailability()`.
4. **GSV03-NIT-01 — суффикс «ГСВ» в 422.** `fieldLabel` теперь добавляет
   «(ГСВ)» к `length`, `diameter`, `drilling_holes`, `sakz_sets`, `has_panel`
   внутри location `gsv`; поля ГСН по-прежнему получают «(ГСН)».

## Полный suite

Команда (CWD `D:/Antigravity/GasProjectCalculator`):

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Результат:

```text
Ran 134 tests in 0.179s

OK
EXIT:0
```

В stderr только `StarletteDeprecationWarning` про `httpx2`; exit code 0.

## Browser verification

### Окружение

1. Порт 8011 свободен; `Test-Path .\.venv\Scripts\python.exe` → `True`.
2. Сервер запущен из CWD `D:/Antigravity/GasProjectCalculator`:

```powershell
$p = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList '-m','uvicorn','app.main:app','--port','8011' -WorkingDirectory "D:\Antigravity\GasProjectCalculator" -PassThru -WindowStyle Hidden
$p.Id | Set-Content C:\Users\user\AppData\Local\Temp\opencode\gsv03r-uvicorn.pid
Start-Sleep -Seconds 4
(Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8011/).StatusCode
```

`→ 200`, PID `5936`.

3. `orca tab create --url http://127.0.0.1:8011 --worktree current --json`
   (CWD `D:/Antigravity/GasProjectCalculator`) → `ok: true`,
   `browserPageId = f097af61-a45c-4290-9b09-c1382e7ffc14`.
4. Все browser-команды ниже выполнены с
   `--page f097af61-a45c-4290-9b09-c1382e7ffc14` из CWD
   `D:/Antigravity/GasProjectCalculator`; каждая вернула `ok: true` (exit 0).

### 1. Начальная загрузка — только ГСН (FINAL-GSV-02)

Сразу после reload/открытия страницы accessibility snapshot содержал только
`ГСН · ПАРАМЕТРЫ ТРАССЫ`, заголовок `Расчёт стоимости — ГСН`, кнопку
`Рассчитать стоимость`; полей ГСВ в дереве не было.

Точная проверка:

```powershell
orca eval --page f097af61-a45c-4290-9b09-c1382e7ffc14 --expression "JSON.stringify({title:document.getElementById('result-title').textContent,gsnHidden:document.getElementById('group-gsn').hidden,gsvHidden:document.getElementById('group-gsv').hidden,gsvDiameterDisabled:document.getElementById('gsv-diameter').disabled,gsvPanelDisabled:document.getElementById('gsv-panel').disabled,gsnLengthDisabled:document.getElementById('length').disabled,submitText:document.getElementById('submit-btn').textContent,submitDisabled:document.getElementById('submit-btn').disabled,calcInfoText:document.getElementById('calc-info').textContent})" --json
```

Результат:

```json
{"title":"Расчёт стоимости — ГСН","gsnHidden":false,"gsvHidden":true,"gsvDiameterDisabled":true,"gsvPanelDisabled":true,"gsnLengthDisabled":false,"submitText":"Рассчитать стоимость","submitDisabled":false,"calcInfoText":"Укажите параметры объекта и нажмите «Рассчитать стоимость»"}
```

Проверка «значения в скрытой группе ГСВ не влияют на стартовый вид»:
после reload значения скрытых полей установлены программно
(`gsv-length=99`, `gsv-diameter=57`, `gsv-holes=3`, `gsv-sakz=2`) без
переключения режима; повторный eval вернул:

```json
{"title":"Расчёт стоимости — ГСН","gsnHidden":false,"gsvHidden":true,"gsvDiameterDisabled":true,"gsvLengthHiddenValue":"99","gsvDiameterHiddenValue":"57","gsvHolesHiddenValue":"3","gsvSakzHiddenValue":"2","gsvSectionVisible":false}
```

Последующий ГСН-submit дал прежние `65 000 / 3 250 / 68 250 ₽` — скрытые
значения ГСВ не повлияли ни на вид, ни на расчёт.

Скриншот: `docs/screenshots/gsv-03-initial-gsn.png`.

### 2. Гонка: отложенный ответ ГСН после переключения в ГСВ (FINAL-GSV-01)

`fetch` в странице обёрнут так, что запрос к `/calculate` отвечает через 5 с:

```powershell
orca eval --page f097af61-a45c-4290-9b09-c1382e7ffc14 --expression "(() => { const orig = window.fetch; window.fetch = function(url, options) { if (String(url).indexOf('/calculate') === 0) { return new Promise(function(resolve) { setTimeout(function() { resolve(orig(url, options)); }, 5000); }); } return orig(url, options); }; return 'fetch-delayed-5000ms'; })()" --json
```

Затем `orca fill --element e10 --value "14"`, `orca click --element e4`
(submit ГСН), сразу `orca click --element e7` (режим ГСВ), ожидание 7 с и eval:

```json
{"title":"Расчёт стоимости — ГСВ","gsnResultDisplay":"none","gsvResultDisplay":"none","calcInfoDisplay":"","submitText":"Рассчитать стоимость","submitDisabled":false,"errorDisplay":"none","errorText":"","gsnTotalText":"—","bodyHas65000":false}
```

Отложенный ответ ГСН проигнорирован: заголовок остался «ГСВ», результат ГСН
не показан, сумма `65 000 ₽` отсутствует, кнопка восстановлена, ошибки нет.

Скриншот: `docs/screenshots/gsv-03-race-guard.png`.

### 3. Скрытый diameter=58 не блокирует ГСН submit (FINAL-GSV-03)

Последовательность: режим ГСВ → `fill #gsv-diameter = 58` → переключение в ГСН
→ проверка → submit ГСН.

Перед submit:

```json
{"gsvDiameterValue":"58","gsvDiameterDisabled":true,"gsvLengthDisabled":true,"gsvHolesDisabled":true,"gsvSakzDisabled":true,"gsvPanelDisabled":true,"gsnLengthDisabled":false,"formValid":true,"title":"Расчёт стоимости — ГСН"}
```

`form.checkValidity()` → `true`: скрытое поле `diameter=58` отключено и не
участвует в нативной валидации. `orca click --element e27` выполнил расчёт:

```json
{"title":"Расчёт стоимости — ГСН","gsnResultDisplay":"","gsvResultDisplay":"none","errorDisplay":"none","errorText":"","subtotal":"65 000 ₽","vat":"3 250 ₽","total":"68 250 ₽","submitText":"Рассчитать стоимость","submitDisabled":false}
```

При возврате в ГСВ поле снова активно и валидируется:

```json
{"gsvDiameterDisabled":false,"gsvDiameterValue":"58","valid":false,"validationMessage":"Значение должно быть меньше или равно 57.","gsnGroupHidden":true,"title":"Расчёт стоимости — ГСВ"}
```

Скриншот: `docs/screenshots/gsv-03-hidden-validation.png`.

### 4. Прежние суммы трёх режимов не изменились

Проверялись те же сценарии, что в `GSV-03-browser.md`.

- **ГСВ:** частник, район, 8 м, Ø25, 2 отверстия, 1 комплект САКЗ, ПК.
  Результат: база `60 000 ₽`, длина `7 500 ₽`, бурение `8 000 ₽`,
  САКЗ `14 000 ₽`, ПК `4 000 ₽`, район `7 000 ₽`,
  **подытог `100 500 ₽`, НДС `5 025 ₽`, итого `105 525 ₽`**; ошибок нет.
- **Combined:** частник, район; ГСН 10 м без опций; ГСВ 5 м, Ø25, без опций.
  Результат: **ГСН `75 600 ₽`, ГСВ `70 350 ₽`, общий подытог `139 000 ₽`,
  НДС `6 950 ₽`, итого `145 950 ₽`**; ошибок нет; при САКЗ 0 ПК
  `disabled` и `checked=false`.
- **ГСН:** частник, район, длина 14, углы 2, экскаватор 4 ч.
  Результат: база `65 000 ₽`, длина `12 000 ₽`, углы `6 000 ₽`,
  экскаватор `15 000 ₽`, район `7 000 ₽`,
  **подытог `105 000 ₽`, НДС `5 250 ₽`, итого `110 250 ₽`**; ошибок нет.

Все три значения совпадают с прежним evidence и VISION.

### 5. Mobile 390×844 без горизонтального скролла

```powershell
orca viewport --page f097af61-a45c-4290-9b09-c1382e7ffc14 --width 390 --height 844 --mobile --json
```

→ `{"width":390,"height":844,"deviceScaleFactor":1,"mobile":true}`, `ok: true`.
В режиме ГСВ:

```json
{"scrollWidth":390,"innerWidth":390,"bodyScrollWidth":390,"fits":true}
```

Горизонтального скролла нет.

Скриншот: `docs/screenshots/gsv-03-mobile.png`.

### 6. GSV03-NIT-01 — суффикс «ГСВ» в combined 422

```powershell
orca eval --page f097af61-a45c-4290-9b09-c1382e7ffc14 --expression "JSON.stringify({diameter:fieldLabel(['body','gsv','diameter']),drilling:fieldLabel(['body','gsv','drilling_holes']),sakz:fieldLabel(['body','gsv','sakz_sets']),panel:fieldLabel(['body','gsv','has_panel']),gsvLength:fieldLabel(['body','gsv','length']),gsnLength:fieldLabel(['body','gsn','length'])})" --json
```

→ `{"diameter":"Диаметр (ГСВ)","drilling":"Количество отверстий (ГСВ)","sakz":"Количество комплектов САКЗ (ГСВ)","panel":"ПК (ГСВ)","gsvLength":"Длина (ГСВ)","gsnLength":"Длина (ГСН)"}`.

Реальный combined-запрос с `gsv.diameter=58` из страницы:

```powershell
orca eval --page f097af61-a45c-4290-9b09-c1382e7ffc14 --expression "(async () => { const r = await fetch('/calculate/combined',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({customer_type:'частное лицо',is_district:false,gsn:{length:5,angles:0,hdd:false,excavator_hours:0,hydraulic_hammer:false,has_grpsh:false},gsv:{length:5,diameter:58,drilling_holes:0,sakz_sets:0,has_panel:false}})}); const j = await r.json(); return JSON.stringify({status:r.status,message:formatApiError(j),detail:j.detail}); })()" --json
```

→ `status: 422`, `message: "Диаметр (ГСВ): должно быть не больше 57"`,
`detail[0].loc = ["body","gsv","diameter"]`.

## Остановка сервера

```powershell
Stop-Process -Id (Get-Content C:\Users\user\AppData\Local\Temp\opencode\gsv03r-uvicorn.pid)
```

Последующий `Invoke-WebRequest http://127.0.0.1:8011/` завершился ошибкой
соединения — сервер остановлен. Browser tab закрыт:
`orca tab close --page f097af61-a45c-4290-9b09-c1382e7ffc14` → `closed: true`.

## git status --short (на момент завершения)

```text
 M frontend/index.html
?? docs/screenshots/gsv-03-hidden-validation.png
?? docs/screenshots/gsv-03-initial-gsn.png
?? docs/screenshots/gsv-03-mobile.png
?? docs/screenshots/gsv-03-race-guard.png
?? docs/workflow/evidence/GSV-03-regression.md
```

`docs/screenshots/gsv-03-*.png` из прежней приёмки не изменялись. Коммит не
выполнялся; продуктовый код вне `frontend/index.html` не менялся.
