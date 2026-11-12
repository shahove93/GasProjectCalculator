# RD-06 evidence — пересборка package/installer и проверка реальной программы

Исполнитель: отдельный реальный Orca OpenCode/DeepSeek Flash worker,
`task_cfc31f1035c5`, dispatch `ctx_94c225a27a49`. Это evidence исполнителя,
не project PASS и не приёмка: решение R2 (Codex) и commit — за координатором.

## Workspace / revisions

- CWD: `D:\Antigravity\GasProjectCalculator`
- Ветка: `feature/ss-calculator-redesign`
- Настоящий HEAD на момент работы: `7ce34f2` (`docs(workflow): record RD-05
  commit and RD-06 dispatch`). Продуктовый baseline RD-05 — `1af13d6`;
  `git diff --stat 1af13d6..HEAD -- app frontend packaging installer tests`
  пуст (docs-only commits `7ce34f2` между baseline и HEAD).
- Продуктовый код, calculator/API/requirements, `app/main.py`, VISION/
  ARCHITECTURE/ROADMAP/workflow docs не менялись. Рабочее дерево содержит
  только новые RD-06 evidence/logs/screenshots; артефакты
  `installer/Output/` и `dist/` — git-ignored.
- Не трогались: `:8000` PID 12888, `:8138` PID 23152 и уже запущенное
  пользовательское приложение `GasProjectCalculator.exe` PID 13248
  (стартовало 06:20:30, путь установки по умолчанию). Их состояние после
  работы проверено и совпадает с исходным.
- Branch switch/reset/rebase, push/merge/deploy/release/signing не выполнялись.

## B1. Новая сборка packaged app и installer (из RD-05)

Команды запускались из CWD = workspace.

| Шаг | Команда | Exit | Лог |
| --- | --- | --- | --- |
| Package | `powershell -NoProfile -ExecutionPolicy Bypass -File packaging\build.ps1` | 0 | `logs/RD-06-packaging-build.txt` |
| Installer | `powershell -NoProfile -ExecutionPolicy Bypass -File installer\build-installer.ps1` | 0 | `logs/RD-06-installer-build.txt` |

PyInstaller: `Build complete!`; packaged frontend соответствует исходнику:

| Файл | Size | SHA256 |
| --- | --- | --- |
| `dist\GasProjectCalculator\GasProjectCalculator.exe` | 6 836 651 | `5403540C4172779ED6F97381A9618FE423D0915A6BEC1710BAE2B578F6ACDD2C` |
| `dist\GasProjectCalculator\_internal\frontend\index.html` | 70 922 | `60B15F15245B834913ACF25445237146F773628AD674E5EF3E8FE15D26894037` |
| `frontend\index.html` (source) | 70 922 | `60B15F15245B834913ACF25445237146F773628AD674E5EF3E8FE15D26894037` |

Inno Setup build log подтверждает источник сборки: `Packaged exe SHA256:
5403540C…CDD2C` и строку `Compressing: …\dist\GasProjectCalculator\_internal\
frontend\index.html`; `Successful compile (7,843 sec)`.

Новый локальный installer (git-ignored):

- path: `D:\Antigravity\GasProjectCalculator\installer\Output\
  GasProjectCalculator-Setup-1.0.0.exe`
- size: **15 286 980 bytes**
- SHA256: **`71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08`**

## B2. Legacy installer

Перед пересборкой текущий accepted installer скопирован, прежний
previous-stage не перезаписывался:

| Файл | Size | SHA256 |
| --- | --- | --- |
| `installer\Output\legacy\GasProjectCalculator-Setup-1.0.0-pre-compact.exe` (новый backup) | 15 273 647 | `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A` |
| `installer\Output\legacy\GasProjectCalculator-Setup-1.0.0-previous-stage.exe` (не изменён) | 15 256 037 | `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F` |

Доказательство: `logs/RD-06-backup-legacy.txt`.

## B3. Изолированная установка нового installer

Перед установкой сохранены:

- HKCU uninstall key `{A3E4B6C1-7F2D-4B8E-9C1A-5D6E7F8091A2}_is1`
  (`reg export` → `backup-uninstall-key.reg`, exit 0).
- Start Menu shortcut `%APPDATA%\Microsoft\Windows\Start Menu\Programs\
  СС.Расчет.lnk` (copy + SHA256 `B3D7A0C6…9153`).

Команда (CWD = workspace, non-elevated):

```text
installer\Output\GasProjectCalculator-Setup-1.0.0.exe
  /VERYSILENT /SUPPRESSMSGBOXES /NORESTART
  /DIR="C:\Users\user\AppData\Local\Temp\opencode\rd06-install"
  /NOICONS /LOG="…\rd06\rd06-inno-install.log"
```

Exit 0; установлен только test instance в temp. Проверено:

| Проверка | Результат |
| --- | --- |
| installed exe | `…\rd06-install\GasProjectCalculator.exe` |
| installed exe SHA256 | `5403540C4172779ED6F97381A9618FE423D0915A6BEC1710BAE2B578F6ACDD2C` = dist exe |
| installed `_internal\frontend\index.html` SHA256 | `60B15F15…4037` = source index |
| HKCU key после установки | `InstallLocation = …\rd06-install\` (test instance) |
| пользовательская установка по умолчанию | exe `5E25FA92…FBA3`, index `586C3A62…B4EC`, `unins000.dat` `B1728FEA…28D0` — не изменены |

Доказательство: `logs/RD-06-install.txt`, `logs/RD-06-inno-install.txt`.

Важное наблюдение для reviewer: несмотря на `/NOICONS`, Inno Setup перезаписал
существующий Start Menu ярлык на test instance (target →
`…\rd06-install\GasProjectCalculator.exe`). Поэтому ярлык восстановлен из
backup после uninstall; итоговый SHA256 снова `B3D7A0C6…9153`, target —
пользовательская установка по умолчанию. Пользовательские файлы установки по
умолчанию при этом не менялись.

## B4/B5. Реальная программа: packaged и установленная

### Запуск

- Packaged: `dist\GasProjectCalculator\GasProjectCalculator.exe
  --preferred-port 8180 --port-file … --log-file … --eval-bridge …`,
  PID 14912; backend ready 0.75 s; main window shown; закрыто WM_CLOSE,
  exit 0, listener 8180 освобождён (`logs/RD-06-packaged-launcher.txt`,
  `logs/RD-06-packaged-close.txt`).
- Установленная версия: `…\rd06-install\GasProjectCalculator.exe` запущен с
  `PATH=C:\Windows\System32;C:\Windows` (в этом PATH `python` не найден).
  PE subsystem нового exe = 2 (`WINDOWS_GUI`, без консоли;
  `logs/RD-06-pe-subsystem.txt`). PID 28136;
  preferred 8181 → выбран 8182; backend ready 0.76 s; закрыто WM_CLOSE,
  exit 0, listener освобождён
  (`logs/RD-06-installed-launcher.txt`, `logs/RD-06-installed-lifecycle.txt`).
- Native screenshots сняты Win32 `PrintWindow` с `PW_RENDERFULLCONTENT` из
  реального окна (не full-page, не склейка). Окно могло быть за IDE.

### Win32 geometry (real client area, DPI)

| Состояние | outer | client | DPI |
| --- | --- | --- | --- |
| Packaged target | 800×540 | 784×501 | 96 |
| Packaged min (request 760×520) | 760×520 | 744×481 | 96 |
| Installed target | 800×540 | 784×501 | 96 |
| Installed min (request 760×520) | 760×520 | 744×481 | 96 |

### Viewport metrics (installed; packaged — те же значения)

Метрики сняты `evaluate_js` в WebView2 реального окна; `scrollY=0` во всех
состояниях.

| Размер | Режим | inner | scroll | page h/v scroll | submit в viewport | итог в viewport | form client/scroll | detail client/scroll |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| target 800×540 | ГСН | 784×501 | 0,0 | нет/нет | да | да | 193/193 | 189/189 |
| target | ГСВ | 784×501 | 0,0 | нет/нет | да | да | 211/211 | 189/189 |
| target | combined | 784×501 | 0,0 | нет/нет | да | да | 193/292 | 189/199 |
| min 760×520 | ГСН | 744×481 | 0,0 | нет/нет | да | да | 173/173 | 171/171 |
| min | ГСВ | 744×481 | 0,0 | нет/нет | да | да | 182/182 | 171/171 |
| min | combined | 744×481 | 0,0 | нет/нет | да | да | 164/292 | 171/199 |

`scrollWidth == clientWidth` и `scrollHeight == clientHeight` для страницы;
horizontal overflow не маскируется (`body overflow-x: auto`). Combined честно
использует внутреннюю прокрутку формы/детализации; итог и кнопка вне этих
областей и постоянно видимы. Шрифты: body 13 px, field label 11.5 px,
input 13 px, total 22.736 px, button 13.5 px; CSS zoom/scale отсутствует.

Полные метрики: `logs/RD-06-packaged-native.json`,
`logs/RD-06-installed-native.json`.

### Screenshots (real native)

`docs/screenshots/rd-06-installed-*` и `rd-06-packaged-*`:

- `target-window` / `min-window` — реальное окно в target/min;
- для каждого размера и каждого режима: `…-{gsn,gsv,combined}-before.png` и
  `…-{gsn,gsv,combined}.png` (до/после submit, `scrollY=0`, action+итог
  видимы);
- `…-422.png` — видимая ошибка 422;
- `rd-06-installed-splash.png` — заставка 520×320.

Сопоставление с before: `docs/screenshots/rd-03-installed-main.png` (старое
окно 1050×740), `rd-05-before-1050x740.png`; производное сравнение
`docs/screenshots/rd-06-compare-installed-before-after.png` (1050×740 слева,
800×540 справа). Полные размеры/хэши всех файлов — `logs/RD-06-final-state.txt`.

## B6. Значения и САКЗ/ПК/422 (установленная версия)

| Режим | Сценарий RD-01 | Подытог | НДС 5% | Итого |
| --- | --- | --- | --- | --- |
| ГСН | юрлицо, район, 14 м, 2 угла, 4 ч экскаватора | 125 000 ₽ | 6 250 ₽ | **131 250 ₽** |
| ГСВ | физлицо, район, 8 м, Ø25, 2 отверстия, САКЗ 1 + ПК | 100 500 ₽ | 5 025 ₽ | **105 525 ₽** |
| combined | 10 м ГСН без опций + 5 м ГСВ Ø25 без опций, район | 139 000 ₽ | 6 950 ₽ | **145 950 ₽** |

САКЗ/ПК (реальные DOM-состояния): САКЗ=0 → ПК `disabled=true`,
`checked=false`; САКЗ=1 → `disabled=false`, switch включается
(`sakzZeroPanelDisabled=true`, `sakzZeroPanelChecked=false`,
`sakzOnePanelDisabled=false`, `sakzOnePanelChecked=true`).

422: реальный UI submit с недопустимым `customer_type` показал видимое
сообщение «Тип заказчика: допустимы только «частное лицо» или «юридическое
лицо»»; синхронный fetch из native-окна вернул HTTP **422** с
`literal_error` по `customer_type` (`input: недопустимый тип`). Скриншот
`rd-06-installed-422.png`; сырые значения — `RD-06-installed-native.json`.

## B7. Mobile 390×844 (browser viewport) — C2 correction

C2 исправляет RD06-F01 (C1 FAIL): прежний
`docs/screenshots/rd-06-installed-mobile-390x844.png` (size 187 567, SHA256
`BA0D59196C6457407F2E5F5574BF8722E7E93339370F586ED92889FA59D9455C`) был
склейкой/full-page: повтор шапки около y=426 и обрезанные полосы справа около
x=362. Этот файл **superseded**; продукт/CSS не менялись.

Для C2 тот же installer (`71232EE4…7E08`) изолированно переустановлен в temp
`/DIR` с backup/restore HKCU key и Start Menu ярлыка; пользовательская
установка по умолчанию и PID 13248 не трогались. Установленное приложение
(port 8185) открыто в Orca browser. Финальный снимок сделан как **настоящий
viewport-only**:

```text
orca exec --command "set viewport 390 844" --page <id> --json
  -> {"deviceScaleFactor":1,"height":844,"mobile":false,"width":390}
orca screenshot --page <id> --json       # viewport, не full-page
```

`set device --name "iPhone 12"` в этом Orca runtime давал именно stitched/
full-page артефакт RD06-F01, поэтому для финального evidence использован
viewport-resize, а не device emulation; PNG не PrintWindow/не склейка.

Метрики при `scrollY=0` (combined, `documentElement`):

- `inner = 390×844`, dpr 1;
- `scrollWidth / clientWidth = 375 / 375`;
- `scrollHeight / clientHeight = 889 / 844`;
- `window.scrollX / scrollY = 0 / 0`; `hScroll = false`;
- max right edge не-SVG элементов = **375.0** (`HEADER.topbar`);
  max right edge SVG-контейнера = 365.0; декоративные `path` выходят за
  контейнер, но клипаются и не создают horizontal scroll;
- кнопка: left 22, right 353, top 769, bottom 800 — в viewport.

Новые viewport-only скриншоты (оба ровно 390×844):

| Файл | Size | SHA256 | Условие |
| --- | --- | --- | --- |
| `docs/screenshots/rd-06-installed-mobile-390x844.png` | 82 172 | `FFB848567864F2C5E5A9ABD977189E4F4564CCFA06BF30A509E3CB8E2A3243A5` | scrollY=0 |
| `docs/screenshots/rd-06-installed-mobile-390x844-result.png` | 67 398 | `DF9009759173626132DE390B04231B17422FA35FB9FF8E4976D79F27CC577572` | после реального scroll к итогу; scrollY=45 |

Визуальная проверка нового основного снимка: шапка ровно одна, повтора на
y≈426 нет, правый край не обрезан, полос на x≈362 нет; средняя абсолютная
разница пикселей строк 0–99 и 426–525 = 186.143 (не дубликат). Лог:
`logs/RD-06-mobile-390.txt`; raw install/uninstall/cleanup:
`logs/RD-06-c2-inno-install.txt`, `RD-06-c2-inno-uninstall.txt`,
`RD-06-c2-cleanup.txt`. Это browser viewport, не native окно.

## B8. Lifecycle (реальный установленный артефакт)

Примечание к первому installed-прогону (`RD-06-installed-lifecycle.txt`):
test listener на 8181 запускался через automation shell и был остановлен
таймаутом самой оболочки, поэтому port-conflict перепроверен отдельным
контролируемым прогоном ниже; в обоих логах приложение выбрало следующий
порт после занятого preferred.

Контролируемый прогон: test listener заранее занял `127.0.0.1:8183`;
установленное приложение запущено с `--preferred-port 8183`,
`--splash-hold-seconds 5`.

- Заставка: реальное окно 520×320, DPI 96; лог `splash window shown event` →
  backend started. Скриншот `rd-06-installed-splash.png`.
- Backend ready за 0.77 s; main window создан скрытым и показан после
  readiness (800×540, client 784×501).
- Port conflict: выбран **8184** при занятом preferred 8183; listener
  приложения только `127.0.0.1:8184`; test listener — `127.0.0.1:8183`.
- Закрытие окна WM_CLOSE: процесс завершился, exit 0, listener 8184 исчез;
  после остановки test listener 8183 также свободен.
- Логи: `logs/RD-06-installed-lifecycle-conflict.txt`,
  `logs/RD-06-lifecycle-launcher.txt`.

Reuse: lifecycle-механика (in-process uvicorn, splash, loopback bind, close →
stop backend) не менялась с RD-02/RD-03; в этом прогоне она перепроверена на
реальном новом установленном артефакте. Неизменные части RD-02/RD-03
(например, русский failure dialog) повторно не воспроизводились.

## B9. Installer flow / uninstall и user files

Uninstall test instance:

```text
…\rd06-install\unins000.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART
  /LOG="…\rd06\rd06-inno-uninstall.log"
```

Exit 0; каталог `rd06-install` удалён, HKCU key удалён, Start Menu ярлык
удалён. Затем восстановлены HKCU key (`reg import`, exit 0) и ярлык из backup;
итоговые значения: `InstallLocation = C:\Users\user\AppData\Local\Programs\
GasProjectCalculator\`, ярлык target — пользовательская установка, SHA256
`B3D7A0C6F77FF174D81E72BABF4697062BBC8E1BBD930E1F07DD11990A499153`.
Доказательство: `logs/RD-06-uninstall.txt`, `logs/RD-06-inno-uninstall.txt`.

Reuse RD-03 (R3-10/R3-11): `installer/GasProjectCalculator.iss` и
uninstall-flow не менялись; reinstall-поверх-пользовательской-установки и
user-files markers не переигрывались. В этом прогоне минимально доказано:
изолированный uninstall удаляет только test instance, а пользовательская
установка по умолчанию после restore имеет те же exe/index/unins.dat SHA256,
что и до работы.

## B10. Scope / suite

- `git diff --stat 1af13d6 -- app/main.py app/calculator.py
  app/gsv_calculator.py requirements.txt app calculators` — пуст.
- `git diff --stat -- app frontend packaging installer tests` — пуст.
- Полный suite не запускался (по плану — RD-07); targeted unit tests не
  переигрывались, т.к. продуктовый код не менялся, а RD-05 уже дал 33 OK.
  Реальное поведение нового packaged/installed артефакта проверено native-
  прогонами выше.
- `git status` содержит только новые RD-06 evidence/logs/screenshots.
  Доказательство: `logs/RD-06-final-state.txt`.

## B11. Передача артефакта

Новый installer остаётся локальным git-ignored файлом:
`D:\Antigravity\GasProjectCalculator\installer\Output\
GasProjectCalculator-Setup-1.0.0.exe`, 15 286 980 bytes, SHA256
`71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08`.
Signing, push, merge, deploy, release не выполнялись. Legacy-копии сохранены
локально.

## Frozen checklist — evidence map (кандидат, не PASS)

| ID | Evidence |
| --- | --- |
| B1 | Команды/exit 0 + `RD-06-packaging-build.txt`, `RD-06-installer-build.txt`, path/size/SHA256 |
| B2 | `RD-06-backup-legacy.txt`: pre-compact + нетронутый previous-stage |
| B3 | `RD-06-install.txt`, `RD-06-inno-install.txt`: exit 0, isolated temp install, hashes |
| B4 | `RD-06-packaged-launcher.txt`, `RD-06-installed-launcher.txt`; окно запускается без Python; native screenshots |
| B5 | `RD-06-installed-native.json` + screenshots target/min, 3 режима, `scrollY=0` |
| B6 | `RD-06-installed-native.json` (131250/105525/145950, САКЗ/ПК, 422) + screenshot |
| B7 | `RD-06-mobile-390.txt` + `rd-06-installed-mobile-390x844.png` + `…-390x844-result.png` (C2 viewport-only) |
| B8 | `RD-06-installed-lifecycle-conflict.txt`, `RD-06-lifecycle-launcher.txt`, `rd-06-installed-splash.png`, reuse statement |
| B9 | `RD-06-uninstall.txt`, `RD-06-inno-uninstall.txt`, restore proof + reuse RD-03 |
| B10 | `RD-06-final-state.txt`, empty protected diff, suite NOT_RUN |
| B11 | artifact path/size/SHA256, git status, отсутствие signing/push/merge/deploy |

## NOT_RUN / остаточные риски

- Полный suite — не запускался (RD-07). Targeted unit tests не переигрывались
  (reuse RD-05); реальные native-прогоны выполнены.
- Reinstall поверх пользовательской установки и user-files markers — reuse
  RD-03 (installer script/flow не менялся), здесь не переигрывались.
- Reduced-motion и external-resources — reuse RD-05 (frontend index байт-в-байт
  совпадает: SHA256 `60B15F15…4037`).
- Setup error dialog / русский wizard / uninstaller GUI — reuse RD-03
  (installer script не менялся).
- Signing, push, merge, deploy, release — не выполнялись.
- R2 review и project PASS — не выставлялись.
- `/NOICONS` не предотвратил перезапись Start Menu ярлыка; ярлык восстановлен
  из backup, пользовательская установка по умолчанию не изменена. Это
  фактическое поведение installer, а не workaround evidence.
- Пользовательская установка по умолчанию остаётся старой (pre-compact) — она
  намеренно не обновлялась; её запущенный процесс PID 13248 не затрагивался.
- `--eval-bridge` — диагностический opt-in хук RD-05 (F2), активен только с
  флагом; в обычном запуске не используется.

## Логи

- `logs/RD-06-baseline.txt` — HEAD/status/пользовательская установка/порты.
- `logs/RD-06-backup-legacy.txt` — registry/shortcut backup, legacy hashes.
- `logs/RD-06-packaging-build.txt`, `logs/RD-06-installer-build.txt` — сборка.
- `logs/RD-06-install.txt`, `logs/RD-06-inno-install.txt` — установка.
- `logs/RD-06-packaged-launcher.txt`, `logs/RD-06-installed-launcher.txt` — запуск.
- `logs/RD-06-packaged-native-driver.txt`, `logs/RD-06-installed-native-driver.txt`
  и `.json` — native metrics.
- `logs/RD-06-installed-lifecycle.txt`, `RD-06-installed-lifecycle-conflict.txt`,
  `RD-06-lifecycle-launcher.txt` — lifecycle/port conflict.
- `logs/RD-06-mobile-390.txt`, `RD-06-mobile-launcher.txt` — mobile browser.
- `logs/RD-06-uninstall.txt`, `logs/RD-06-inno-uninstall.txt` — uninstall/restore.
- `logs/RD-06-final-state.txt` — финальные процессы/порты/артефакты/screenshots.
