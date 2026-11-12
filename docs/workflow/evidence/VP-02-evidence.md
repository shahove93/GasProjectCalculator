# VP-02 / logical MD-03 A2 C1 — installer 1.2.0 evidence

2026-11-12. **Исполнитель завершил evidence; NOT_REVIEWED.** Это не проектный PASS.
Возобновлён прежний незавершённый подход после разрешения пользователя, без
сброса counters и без новой продуктовой реализации.

## Идентификация и границы

- CWD всех shell-команд ниже: `D:/Antigravity/GasProjectCalculator`.
- Ветка `feature/gsv-mixed-diameters`; HEAD/baseline
  `1689773718c818a4ebca400afc2d8a4206b6458e` (VP-01 принят ранее).
- Текущий Run `run_51b48d1d96cc`, Task `task_150bb380db2c`, Dispatch
  `ctx_988a8c02d5c3`, terminal `term_879889ea-ac9e-48ad-bc89-978a67a20e10`.
- Прежний logical-task container `task_ef0683db9d81` / `ctx_113e19d0197a`
  сохранён в [resume](VP-02-resume.md) и [blocked](VP-02-blocked.md).
- Реальные requested **и** effective: `agent=codex`, `model=gpt-6-astra`,
  `effort=high`; см. [worker-show](logs/VP-02-resume-effective.json),
  `result.worker.launch.config.requested/effective` (поля в сохранённом receipt).
  Модель/аккаунт/глобальные настройки не менялись; helper workers не создавались.
- Счётчики MD-03 A1/C1 и текущий A2/C1 не менялись. Независимый review и
  финальная приёмка остаются за координатором и отдельными ревьюерами.

В этом возобновлении добавлены **только** данный evidence pack,
`docs/workflow/evidence/logs/VP-02-resumed-*` и
`docs/screenshots/visual-02-resumed-*`; использованы разрешённые temp-каталоги
`vp-02-resume`, `vp-02-resume-cycle` и прежний `vp-02-isolated`.
Существовавшие installer/assets/документы координатора сохранены.
**Пересборки, продуктовых правок и коммитов в этом dispatch нет.**

## Артефакт и неизменность предыдущих версий — W1–W3, W11

Каноничный local artifact:
`D:/Antigravity/GasProjectCalculator/installer/Output/GasProjectCalculator-Setup-1.2.0.exe`.
Размер **15 373 267 B**, FileVersion **1.2.0.0**, ProductVersion **1.2.0**,
SHA256 **4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113**.

| Артефакт относительно `installer/Output` | Bytes | SHA256 до и после возобновления |
| --- | ---: | --- |
| `GasProjectCalculator-Setup-1.0.0.exe` | 15286980 | `71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08` |
| `GasProjectCalculator-Setup-1.1.0.exe` | 15293993 | `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710` |
| `legacy/GasProjectCalculator-Setup-1.0.0-pre-compact.exe` | 15273647 | `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A` |
| `legacy/GasProjectCalculator-Setup-1.0.0-previous-stage.exe` | 15256037 | `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F` |

До первоначальной сборки: [old-artifacts-before](logs/VP-02-old-artifacts-before.json).
До этого dispatch: [preflight](logs/VP-02-resumed-preflight.json).
После всех проверок: [manifest](logs/VP-02-resumed-manifest.json), `artifacts`.
Все пять файлов, включая 1.2.0, совпали по bytes/SHA256. Remote releases не
запрашивались и не изменялись; никаких push/merge/deploy/release операций.

Повторно использованы завершённые build evidence:

| Эффективная команда / точка входа | Exit | Доказательство |
| --- | ---: | --- |
| `powershell -ExecutionPolicy Bypass -File packaging/build.ps1` → `.venv/Scripts/python.exe -m PyInstaller --noconfirm --clean --distpath D:/Antigravity/GasProjectCalculator/dist --workpath D:/Antigravity/GasProjectCalculator/build D:/Antigravity/GasProjectCalculator/packaging/GasProjectCalculator.spec` | 0 | [build log](logs/VP-02-packaging-build.txt), [exit](logs/VP-02-packaging-build.exit.txt) |
| `powershell -ExecutionPolicy Bypass -File installer/build-installer.ps1` → установленный `ISCC.exe` с `installer/GasProjectCalculator.iss` | 0 | [final build log](logs/VP-02-installer-build.txt), [exit](logs/VP-02-installer-build.exit.txt) |

Внешний shell wrapper старой сборки в логах не сохранён; таблица указывает
entrypoints и эффективные аргументы из scripts/logs, а не новую сборку.
Первый build-log с obsolete-color warnings сохранён отдельно
(`VP-02-installer-build-initial.txt`); итоговый build-log без этих warnings.
Старая первая копия `vp-02-isolated/first-build-1.2.0.exe` не тронута.

Packaged EXE: `dist/GasProjectCalculator/GasProjectCalculator.exe`, SHA256
`DD9AF5486B3A5C93C6AAD2A0D9C4AFE6ADF14DEF340F7FEDE371B70E709E6888`.
Новый static evidence сопоставил **все 111 payload files** установленной
версии с `dist`, все frontend files с принятым source, подтвердил bundled
Python DLL и PE subsystem=2 (Windows GUI, без console). Backend/frontend
source относительно HEAD — zero-diff. Сборка соответствует сохранённому
VP-01, основания пересобирать не обнаружено.

## Русский wizard и branding — W4

Повторно использованы реальные PNG первоначальной установки (просмотрены
при возобновлении):

- [welcome](../../screenshots/visual-02-wizard-welcome.png),
  [dir](../../screenshots/visual-02-wizard-dir.png),
  [tasks](../../screenshots/visual-02-wizard-tasks.png),
  [ready](../../screenshots/visual-02-wizard-ready.png),
  [installing](../../screenshots/visual-02-wizard-installing.png),
  [finish](../../screenshots/visual-02-wizard-finish.png) — **598×464** каждый.
- Welcome/finish: тёмная боковая иллюстрация, труба/дом/тёплое окно;
  внутренние страницы: малая верхняя иллюстрация. Русские названия и кнопки
  читаемы, sidebar не перекрывает controls, task Desktop изначально выключен.
- Штатный Inno Setup 6.4.1, единственный `russian` language,
  `ShowLanguageDialog=no`, `PrivilegesRequired=lowest`, прежний AppId.
- BMP sidebar 328×628, header 110×110; pixel-for-pixel соответствуют
  принятым `frontend/assets/installer-*.png`; [static JSON](logs/VP-02-resumed-static.json).

Исходный GUI запуск:
`installer/Output/GasProjectCalculator-Setup-1.2.0.exe /DIR="C:\Users\user\AppData\Local\Temp\opencode\vp-02-isolated\install" /LOG="D:\Antigravity\GasProjectCalculator\docs\workflow\evidence\logs\VP-02-wizard-install.log" /NORESTART`.
В [raw log](logs/VP-02-resumed-wizard-original-raw.txt) зафиксированы target,
установка, Finish и postinstall запуск EXE без аргументов. Отдельный numeric
exit первоначального GUI wrapper не сохранён; finish/log подтверждают
завершение, а текущий isolated install-cycle дал numeric exits 0.

## Installed app, размеры и реальные расчёты — W6–W7

Прежний запуск **без CLI** подтверждается Finish → native окно и
[process record](logs/VP-02-ui-launched-process.json): установленный EXE,
CommandLine только путь EXE, без python/uvicorn. Screenshots
[normal launch](../../screenshots/visual-02-native-normal-launch.png),
[splash 560×450](../../screenshots/visual-02-native-splash.png) сохранены.

Текущий диагностический запуск выполнил именно installed EXE при
`PATH=C:\Windows\System32;C:\Windows`, `pythonResolved=false`:

```powershell
Start-Process -FilePath 'C:/Users/user/AppData/Local/Temp/opencode/vp-02-isolated/install/GasProjectCalculator.exe' -ArgumentList @('--preferred-port',65531,'--port-file','C:/Users/user/AppData/Local/Temp/opencode/vp-02-resume/port.json','--log-file','D:/Antigravity/GasProjectCalculator/docs/workflow/evidence/logs/VP-02-resumed-native.log','--eval-bridge','C:/Users/user/AppData/Local/Temp/opencode/vp-02-resume/bridge.json') -WindowStyle Normal -PassThru
```

PID 2236, shell exit 0; [launch](logs/VP-02-resumed-launch.json),
[process tree](logs/VP-02-resumed-process-tree-before.json),
[native raw log](logs/VP-02-resumed-native-raw.txt). Python использовался
только для внешних тестов/анализа изображений, не для запуска приложения.
Диагностические параметры не меняют UI/CSS. В этом запуске нет splash-hold.

Native UI управлялся `@oai/sky` через `list_windows/get_window`, с выбором
**полного пути изолированного EXE**. Ввод — `set_value`/`click`, смена режима
обычными кнопками, resize — штатное меню Alt+Space → Размер и стрелки до
min-size, закрытие — кнопка Закрыть. `--eval-bridge` использован **только
для чтения** DOM-метрик, не для подмены результатов или изменения CSS/zoom.
Результаты capture/доступности/метрик: [native-ui JSON](logs/VP-02-resumed-native-ui.json).
Для этих tool API нет shell exit; вызовы завершились успешно, наблюдаемые
результаты сохранены. Неудачная первая попытка drag не изменила размер;
последующий штатный resize довёл окно до минимума.

| Native геометрия | ГСН | ГСВ | Общая смета |
| --- | --- | --- | --- |
| target 800×540, WebView client 784×501, DPR=1 | [68 250](../../screenshots/visual-02-resumed-native-target-gsn.png) | [75 600](../../screenshots/visual-02-resumed-native-target-gsv.png) | [158 550](../../screenshots/visual-02-resumed-native-target-combined.png) |
| min 760×520, WebView client 744×481, DPR=1 | [68 250](../../screenshots/visual-02-resumed-native-minimum-gsn.png) | [75 600](../../screenshots/visual-02-resumed-native-minimum-gsv.png) | [158 550](../../screenshots/visual-02-resumed-native-minimum-combined.png) |

На этих страницах scrollX=scrollY=0, document dimensions равны viewport,
action и total находятся внутри viewport. Target ГСН DOM-метрики также есть
в прежнем `VP-02-native-metrics.json`; новые target ГСВ/combined и min всех
режимов — в `VP-02-resumed-native-ui.json`. Внутренние панели формы/деталей
прокручиваются по принятому дизайну; общий итог и action остаются видимы.
Основной размер фиксируется launcher log и client geometry; системная рамка
занимает 16×39 px. Bounded native capture исключает невидимые рамки Windows:
реальные PNG **786×533** (target) и **746×513** (min), а не искусственно
растянутые 800×540/760×520. Sky вернул JPEG; они перекодированы в PNG без
обрезки, ресайза, дорисовки и композиции. [Export map](logs/VP-02-resumed-png-export.json).

Browser проверен **на backend установленного EXE** `http://127.0.0.1:65532`,
не на source server. Команда `node docs/workflow/evidence/logs/VP-02-resumed-browser.cjs`,
exit **0**; [stdout](logs/VP-02-resumed-browser-run.txt),
[exit](logs/VP-02-resumed-browser-run.exit.txt), [requests/responses/metrics](logs/VP-02-resumed-browser.json).
Реальный Edge/Playwright: desktop800×540, minimum760×520, mobile390×844;
14 основных случаев (9 device/mode + 5 mixed), дополнительные options/422.
Desktop/min: scrollY=0, action/total visible. Mobile: вертикальная прокрутка
обычная, горизонтального overflow нет. PNG `visual-02-resumed-{desktop,minimum,mobile}-*`;
точные размеры/hash каждого — в manifest (full-page mobile может быть выше844).
Page errors **[]**, external requests **[]**. Все три режима переключаются,
после 422 переключение убирает старую ошибку и чужой result.

API повторён один раз, потому что старый `VP-02-api-run.exit.txt` был пуст:
`pwsh -NoProfile -File docs/workflow/evidence/logs/VP-02-resumed-api-check.ps1`,
exit **0**. [Точные JSON requests/responses](logs/VP-02-resumed-api.json),
[summary](logs/VP-02-resumed-api-summary.txt), [stdout](logs/VP-02-resumed-api-run.txt),
[exit](logs/VP-02-resumed-api-run.exit.txt). Старые evidence не переписаны.

| Проверка установленной версии | Получено |
| --- | --- |
| ГСВ 4/0/4 | 75600; доплата12000, included 4/0/1, billable0/0/3 |
| ГСВ 2/4/3 | 79275 |
| ГСВ 0/5/2 | 71400 |
| ГСВ 3/1/1 | 63000 |
| ГСВ 8/0/0 | 70875 |
| Combined: ГСН10м + ГСВ4/0/4, район | subtotal151000 / VAT7550 / total158550; район7000 в каждом разделе |
| ГСВ4/0/4 + САКЗ1 + ПК + район | subtotal97000 / VAT4850 / total101850 |
| Browser: ГСВ8/0/0 + САКЗ2 + ПК + район | subtotal106500 / VAT5325 / total111825; САКЗ28000, ПК4000 |
| САКЗ0 в UI | ПК disabled и unchecked; при САКЗ2 enabled |
| Legacy ГСВ8м, Ø25, 2 отверстия, САКЗ1/ПК/район | 105525; response без mixed-only keys |
| Смешанный и legacy payload одновременно | HTTP422 |
| ПК без САКЗ | HTTP422 и русская UI error |
| ГСН10м city без опций | 68250 |
| Legacy ГСН: юрлицо14м,2угла,4часа,район | 131250 |

## Lean finish: пять settled browser-кадров и full suite (2026-11-12)

Закрыт прежний единственный evidence-gap: пять кадров mixed-эталонов
`visual-02-resumed-desktop-gsv-D1..D5.png` были сняты во время `fadeUp`.
Новые кадры сняты **после** завершения всех `document.getAnimations()` и
проверки `opacity=1`; старые кадры не перезаписаны.

Управляемый запуск установленного изолированного EXE (не source server,
без reinstall/rebuild):

```powershell
Start-Process -FilePath 'C:/Users/user/AppData/Local/Temp/opencode/vp-02-isolated/install/GasProjectCalculator.exe' -ArgumentList @('--preferred-port','18081','--port-file','C:/Users/user/AppData/Local/Temp/opencode/vp-02-resume/settled-port.json','--log-file','D:/Antigravity/GasProjectCalculator/docs/workflow/evidence/logs/VP-02-resumed-settled-native.log') -WindowStyle Normal -PassThru
```

CWD `D:/Antigravity/GasProjectCalculator`; PID 25216; readiness **0.78 s**;
`http://127.0.0.1:18081/` HTTP **200**; shell exit **0**. Evidence:
[launch](logs/VP-02-resumed-settled-launch.json),
[native log](logs/VP-02-resumed-settled-native.log). Прежний отказ
`ERR_UNSAFE_PORT`/port 0 сохранён: [failed port](logs/VP-02-resumed-settled-port-failed.json),
[old run](logs/VP-02-resumed-settled-shots.txt).

Съёмка:

```powershell
& 'C:/Program Files/nodejs/node.exe' docs/workflow/evidence/logs/VP-02-resumed-settled-shots.cjs
```

CWD `D:/Antigravity/GasProjectCalculator`; exit **0**; stdout:
[run](logs/VP-02-resumed-settled-shots-run.txt),
[exit](logs/VP-02-resumed-settled-shots-run.exit.txt),
[JSON](logs/VP-02-resumed-settled-shots.json). Viewport 800×540, DPR=1;
`scrollX=scrollY=0`; action и total внутри viewport; `opacity=1`.

| Кадр | Длины 25/32–40/57 | Итог | Файл (SHA256) |
| --- | --- | ---: | --- |
| D1 | 4/0/4 | 75 600 | [PNG](../../screenshots/visual-02-resumed-desktop-gsv-D1-settled.png) `C722EA40C7FE287F4591EA68B6238CE67C12CDD6FDF302252B7CC69FC7AEBBAE` |
| D2 | 2/4/3 | 79 275 | [PNG](../../screenshots/visual-02-resumed-desktop-gsv-D2-settled.png) `C40FA7907D1547F0A9D1A3698AB9C7F708CFACF8CA18C9F3CCF5644A52BE13CA` |
| D3 | 0/5/2 | 71 400 | [PNG](../../screenshots/visual-02-resumed-desktop-gsv-D3-settled.png) `920C2B3BC7CDE98D02821CCF358ED033EC8F45E23C954C77B39F0442BF4CD594` |
| D4 | 3/1/1 | 63 000 | [PNG](../../screenshots/visual-02-resumed-desktop-gsv-D4-settled.png) `77098F8DDB8098D73E54CC7F477656BB102CF131D6744A4F6C232FFD2FB29D7D` |
| D5 | 8/0/0 | 70 875 | [PNG](../../screenshots/visual-02-resumed-desktop-gsv-D5-settled.png) `E81A4680186531702308E567B5FEE5B231BC7D6862E4E74D14DBACAA1E3B8D78` |

Закрытие — штатное `CloseMainWindow()`: process exited, `forced=false`,
listener 18081 и дочерние процессы отсутствуют; native log завершился
`exiting with code 0`. Evidence: [close](logs/VP-02-resumed-settled-close.json).

Полный integrated suite исполнен **один раз** по конечной продуктовой ревизии
HEAD `1689773718c818a4ebca400afc2d8a4206b6458e`:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

CWD `D:/Antigravity/GasProjectCalculator`; exit **0**; **219 tests OK**;
[stdout](logs/VP-02-final-full-suite.txt),
[exit](logs/VP-02-final-full-suite.exit.txt).

## Lifecycle / splash — W8

Собственный занятый порт создан через Node `net.createServer().listen(0,'127.0.0.1')`:
получен **65531**. Installed EXE выбрал **65532**, listener **127.0.0.1**;
порт принадлежит PID2236. [Connections](logs/VP-02-resumed-connections.json).
Ни :8000, ни :8138 для этих тестов не использовались.

В native log порядок: splash shown16:39:05.159 → backend ready16:39:06.618
→ splash closed16:39:06.683 → main shown16:39:06.690. Readiness **0.76s**,
без искусственной задержки. Backend — thread в том же EXE, не child Python.

Закрытие кнопкой окна:16:47:23.863; backend stopped16:47:25.190, launcher
exit0. Первая проверка16:47:25.825 слишком рано увидела ещё PID2236 при уже
отсутствующих listener и WebView children — [initial observation](logs/VP-02-resumed-close.json),
shell exit1 этой немедленной проверки **сохранён как timing observation**.
Следующая ограниченная проверка `Get-Process -Id 2236` / `WaitForExit(15000)`
и сравнение всего прежнего дерева процессов в16:47:37.760: **exited=true,
aliveOriginalProcessTree=[], listeners=[]**, shell exit0;
[final close](logs/VP-02-resumed-close-final.json). Force kill не применялся.
Node listener закрыт `busyServer.close()`.

Error path:

```powershell
Start-Process -FilePath 'C:/Users/user/AppData/Local/Temp/opencode/vp-02-isolated/install/GasProjectCalculator.exe' -ArgumentList @('--preferred-port','0','--simulate-startup-failure','--port-file','C:/Users/user/AppData/Local/Temp/opencode/vp-02-resume/error-port.json','--log-file','D:/Antigravity/GasProjectCalculator/docs/workflow/evidence/logs/VP-02-resumed-error.log') -WindowStyle Normal -PassThru
```

PID1800, `status=failed`, splash закрыта до native сообщения, backend не
запущен, **ожидаемый app exit1** / harness exit0 после проверки кода.
[Русский диалог412×276](../../screenshots/visual-02-resumed-native-startup-error.png),
[raw log](logs/VP-02-resumed-error-raw.txt), [exit](logs/VP-02-resumed-error-exit.json).
После ОК нет изолированных окон/процессов.

Reduced motion проверен реальным browser рендером **installed**
`_internal/frontend/splash.html` при560×450: normal animation=`gas-flow`,
OS reduce и diagnostic query flag — animation=`none`, opacity=`0.8`.
[OS reduce](../../screenshots/visual-02-resumed-splash-os.png),
[flag](../../screenshots/visual-02-resumed-splash-flag.png),
[animated](../../screenshots/visual-02-resumed-splash-animated.png).
Компоновка/надписи/дом/труба сохраняются. Windows settings не менялись.

## Изоляция, upgrade/reinstall/uninstall — W5, W9

Команда:
`pwsh -NoProfile -File docs/workflow/evidence/logs/VP-02-resumed-cycle.ps1`,
exit **0**; [script](logs/VP-02-resumed-cycle.ps1),
[полный журнал с точными EXE/ARGS/CWD/exits](logs/VP-02-resumed-cycle.txt),
[exit](logs/VP-02-resumed-cycle.exit.txt).

Каталог только `C:/Users/user/AppData/Local/Temp/opencode/vp-02-resume-cycle/install`.
Перед запуском: fresh backup HKCU uninstall key, обоих ярлыков, SHA256 всех
106 файлов пользовательской установки и start time PID13248/12888/23152.
Backup не перезаписывается при повторном запуске script.

1. Silent install прежней1.1.0 в temp (`/DIR` явно), exit0; key1.1.0 и оба ярлыка
   указывают только в temp. Созданы `user-notes.txt` и `_internal/user-data/custom.txt`.
2. Upgrade тем же AppId до1.2.0, exit0; key1.2.0, оба sentinel unchanged.
3. Reinstall1.2.0, exit0; payload EXE hash и оба sentinel unchanged.
4. `unins000.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /LOG=...`, exit0;
   EXE/registration/созданные ярлыки удалены, оба пользовательских файла остались.
5. `finally`: HKCU exact export восстановлен, Start Menu/Desktop exact SHA256,
   все106 user files unchanged, исходные process start times unchanged.

Raw Inno logs: `VP-02-resumed-cycle-{install-old,upgrade,reinstall,uninstall}-raw.txt`.
В upgrade log явно `Will append to existing uninstall log`, target temp.
HKCU backup/restore export hash и shortcut hashes опубликованы в
[manifest](logs/VP-02-resumed-manifest.json). Backup `.reg` остаётся локально
в temp; в репозиторий не копируется. Обычная registration снова1.0.0.

Предыдущая GUI установка и её восстановление также сохранены:
`VP-02-backup.txt`, `VP-02-restore.txt`, `VP-02-isolation.ps1`.
Никаких постоянных изменений `%LOCALAPPDATA%/Programs/GasProjectCalculator`,
HKCU/ярлыков; `.venv` и чужие процессы сохранены. Изолированные backup,
исходный installed payload и sentinel dirs намеренно оставлены для reviewer.
Installer не скачивает компоненты и не подписывается; source/build directives
проверены, external app requests в browser отсутствуют.

## Targeted checks / scope — W10

| Команда | Exit / результат | Log |
| --- | --- | --- |
| `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_launcher tests.test_frontend_redesign` | 0, **36 tests OK** | [stdout](logs/VP-02-resumed-targeted-tests.txt), [exit](logs/VP-02-resumed-targeted-tests.exit.txt) |
| `.\.venv\Scripts\python.exe docs/workflow/evidence/logs/VP-02-resumed-static.py` | 1, **ModuleNotFoundError: PIL**, до checks | [первый запуск](logs/VP-02-resumed-static.txt), [exit](logs/VP-02-resumed-static.exit.txt) |
| `C:/Users/user/AppData/Local/Programs/Python/Python312/python.exe docs/workflow/evidence/logs/VP-02-resumed-static.py` | 0, **137 assertions**,111 payload files | [stdout](logs/VP-02-resumed-static-system.txt), [exit](logs/VP-02-resumed-static-system.exit.txt), [JSON](logs/VP-02-resumed-static.json) |
| `git diff --check` | 0 | [log](logs/VP-02-resumed-diff-check.txt), [exit](logs/VP-02-resumed-diff-check.exit.txt) |
| `C:/Users/user/AppData/Local/Programs/Python/Python312/python.exe docs/workflow/evidence/logs/VP-02-resumed-manifest.py` | 0;5 artifacts unchanged,48 screenshots (39 PNG + 9 JPEG stored as .png),106 user files unchanged | [stdout](logs/VP-02-resumed-manifest.txt), [exit](logs/VP-02-resumed-manifest.exit.txt), [manifest](logs/VP-02-resumed-manifest.json) |

Использован уже установленный Python312 с Pillow для image/hash evidence;
зависимости не устанавливались, `.venv` не менялась. Первый import error
сохранён, не скрыт. Старые23 targeted tests имели exit0, но не сохранили
точную команду; текущая explicit36 command устраняет этот пробел.
`tests/test_installer_packaging.py` в репозитории отсутствует; новый тестовый
модуль ради формальности не добавлялся — installer/payload assertions в
отдельном evidence script. Существующие functional/security tests не менялись.

Actual product diff относительно VP-01:
[product.diff](logs/VP-02-resumed-product.diff): только версия/branding Inno
и version-specific overwrite guard/build output selection. Новые assets
`installer/assets/wizard-sidebar.bmp`, `wizard-header.bmp`, `export-artwork.ps1`
существовали до возобновления. `app/`, `frontend/`, `packaging/`,
`requirements.txt`, `tests/` zero-diff.
[git status](logs/VP-02-resumed-status.txt) включает предсуществовавшие
координаторские APPROVALS/HISTORY/STATE/brief/task/resume docs; их этот worker
не менял. Полный список добавленных этим dispatch evidence — `workerAddedFiles`
в manifest. Все изменения worker находятся в allowlist.

## Передача и явные ограничения

- [Final state](logs/VP-02-resumed-final-state.json): HEAD/ветка прежние,
  PID13248/12888/23152 и :8000/:8138 сохранены; isolatedProcesses=[], testListeners=[].
- Все48 screenshots (39 PNG + 9 JPEG с расширением .png) перечислены с точными pixels/bytes/SHA256 в manifest.
  Correction VP02-R2-N1: ранее здесь было сказано «48 real PNG».
  `.log` продублированы в `*-raw.txt`, чтобы evidence не потерялось из-за
  общего gitignore для logs. Старые screenshots/logs не перезаписаны.
- **NOT_RUN:** независимый R2 review и final stage acceptance — следующий
  владелец coordinator/reviewers, по заданию. Полный integrated suite теперь
  исполнен (раздел Lean finish: 219 tests OK, exit 0).
- **NOT_RUN:** новая сборка (не нужна); новая remote/release проверка/публикация;
  чистая VM без Python/WebView2; полная packet capture всего ОС. Bundled Python
  и stripped PATH доказаны на текущей машине с установленным WebView2.
- Первоначальный GUI wizard exit wrapper не сохранён; его finish/log и
  текущие install/upgrade/reinstall/uninstall numeric exit0 приведены раздельно.
- Native captures получены из настоящих окон; различие outer/client/capture
  размеров объяснено выше. Никаких CSS/JS/zoom workaround или макетов.
- Commit/push/merge/deploy/release/signing не выполнялись. Артефакт1.2.0
  готов для **независимого review**, не объявлен принятым исполнителем.
