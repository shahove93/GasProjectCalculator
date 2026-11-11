# RD-03 evidence — русский Inno Setup, ярлык СС.Расчет, новая сборка (R2)

Исполнитель: отдельный Orca worker OpenCode Flash, dispatch `ctx_e4488f57f75b`,
task `task_52e983ff51d0`, terminal `term_e70ef6bf-7e8b-47ac-8c7c-ecf7f8204bfc`.
Это evidence исполнителя; проектный PASS не заявляется.

## Workspace / baseline

- CWD: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/ss-calculator-redesign`
- Продуктовый baseline: `32e77b1` (RD-02 accepted/committed).
- HEAD на момент работы: `6d91036` — координаторский workflow-коммит
  «record RD-02 acceptance and RD-03 dispatch» (`docs/workflow/HISTORY.md`,
  `STATE.md`). Worker workflow-документы не менял; `git diff HEAD --
  docs/workflow` пуст. Worktree в начале работы был чистым.
- `:8000` (PID 12888, python) и диагностический `:8138` (PID 23152) не
  останавливались и не менялись. Push/merge/deploy/signing не выполнялись.
- `installer/Output/` — игнорируемый локальный артефакт. Перед пересборкой
  прежний installer сохранён:
  `installer/Output/legacy/GasProjectCalculator-Setup-1.0.0-previous-stage.exe`
  (15 256 037 bytes, SHA256
  `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`).

## Что изменено (только allowlist)

- `installer/GasProjectCalculator.iss`:
  - `AppName`/`UninstallDisplayName` = `СС.Расчет`; ярлыки Start Menu и
    Desktop = `СС.Расчет.lnk`; target/WorkingDir = установленный exe.
  - `AppPublisher`/`VersionInfoCompany` = `ООО «Северное сияние»`.
  - Один язык `russian` (`compiler:Languages\Russian.isl`, Inno Setup 6.4.1);
    `ShowLanguageDialog=no`; сообщения мастера/ошибок/uninstaller — русские.
  - `PrivilegesRequired=lowest`, `ArchitecturesAllowed=x64compatible`,
    per-user `DefaultDirName={localappdata}\Programs\GasProjectCalculator`.
  - `UsePreviousTasks=no` — desktop-задача всегда по умолчанию выключена;
    `DisableWelcomePage=no`, `DisableDirPage=no` — welcome/dir страницы
    показываются и при первой установке, и при reinstall.
  - Start Menu ярлык всегда; Desktop — только по задаче `desktopicon`
    (`unchecked`). `[UninstallDelete]` отсутствует; user data вне `{app}`.
  - Никакой подписи, автообновления, телеметрии, cloud, публикации.
- `installer/verify-install.ps1`, `verify-runtime.ps1`,
  `verify-uninstall.ps1` — обновлены под новое имя/реестр/три режима и
  UTF-8 вывод; ASCII-only, чтобы PowerShell 5.1 не зависел от BOM.
- Не менялись: `app/`, `frontend/`, `packaging/`, расчёты/API,
  `app/main.py`, `app/*calculator*`, VISION/ARCHITECTURE/ROADMAP/workflow
  docs. `git diff 32e77b1 -- app/main.py app/calculator.py
  app/gsv_calculator.py` пуст; `git diff HEAD -- app install frontend
  packaging` пуст.

## Сборка

### Packaged app

Команда (CWD = workspace):

```text
powershell -NoProfile -ExecutionPolicy Bypass -File packaging\build.ps1
```

Exit 0; лог `logs/RD-03-packaging-build.out.txt` заканчивается
`Build complete!`; stderr-лог содержит обычный PyInstaller progress
(`logs/RD-03-packaging-build.err.txt`). Артефакт:
`dist\GasProjectCalculator\GasProjectCalculator.exe`,
SHA256 `5E25FA92A530E104AA69BC7153C068FA34C477659F375142EA7D047257A0FBA3`.
В bundle включены `frontend/index.html`, `frontend/splash.html`,
`frontend/assets/company-emblem.png`.

### Installer

Компилятор: `C:\Users\user\AppData\Local\Programs\Antigravity IDE\
resources\app\node_modules\innosetup\bin\ISCC.exe` (Inno Setup 6.4.1,
`ISCmplr.dll` рядом; не устанавливался системно, не коммитился).
Команда (CWD = workspace):

```text
powershell -NoProfile -ExecutionPolicy Bypass -File installer\build-installer.ps1
```

Exit 0; лог `logs/RD-03-installer-build-final.out.txt`:
`Successful compile (4,375 sec)`; `Packaged exe SHA256` совпадает с
`5E25…FBA3`.

Итоговый артефакт (локальный, git-ignored):

- path: `D:\Antigravity\GasProjectCalculator\installer\Output\
  GasProjectCalculator-Setup-1.0.0.exe`
- size: **15 273 647 bytes**
- SHA256: **`043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`**

## Install / reinstall / uninstall

Все команды запускались из CWD = workspace, не из elevated shell
(`shell elevated: False`). По логам Inno: `User privileges: None`,
`Administrative install mode: No`, `Install mode root key: HKEY_CURRENT_USER`.

Перед clean install прежняя установка предыдущего этапа была удалена её
штатным uninstaller (`/VERYSILENT`, exit 0); пользовательские markers вне
каталога установки сохранились. Прежний installer artifact также сохранён в
`legacy/`.

### Clean silent install без desktop task

```text
installer\Output\GasProjectCalculator-Setup-1.0.0.exe
  /VERYSILENT /SUPPRESSMSGBOXES /NORESTART
  /LOG="…\RD-03-install-no-desktop-inno.log"
```

Exit 0. HKCU uninstall key создан, HKLM-ключ отсутствует. `DisplayName:
СС.Расчет`, `Publisher: ООО «Северное сияние»`, `InstallLocation:
C:\Users\user\AppData\Local\Programs\GasProjectCalculator\`.
Start Menu ярлык `СС.Расчет.lnk` создан, target/WorkingDir = установленный
exe; Desktop ярлык отсутствует. Логи:
`logs/RD-03-install-no-desktop.txt`,
`logs/RD-03-inno-install-no-desktop.txt`.

### Reinstall поверх установки с desktop task

```text
…\GasProjectCalculator-Setup-1.0.0.exe /VERYSILENT /SUPPRESSMSGBOXES
  /NORESTART /TASKS="desktopicon" /LOG="…\RD-03-reinstall-desktop-inno.log"
```

Exit 0. Файлы заменены; Start Menu и Desktop ярлыки `СС.Расчет.lnk` указывают
на установленный exe. Пользовательские markers (Documents, Desktop,
`%LOCALAPPDATA%\GasProjectCalculator`) сохранили те же SHA256, что до
reinstall. Логи: `logs/RD-03-reinstall-desktop.txt`,
`logs/RD-03-inno-reinstall-desktop.txt`; финальный reinstall —
`logs/RD-03-reinstall-desktop-final.txt`.

### Runtime установленного приложения

`installer\verify-runtime.ps1` (PATH без Python, занятый preferred-порт):
exit 0 (`logs/RD-03-runtime.txt`).

- PE subsystem = 2 `WINDOWS_GUI (no console)`; после `PATH=C:\Windows\System32;C:\Windows` команда `python` не найдена.
- Заставка 520×320 показана до старта backend; backend ready через 0.77 s;
  main window создан скрытым и показан после readiness.
- `MainWindowTitle: СС.Расчет`; title/иконка/эмблема — реальные скриншоты.
- Preferred 8123 занят тестовым listener → приложение выбрало 127.0.0.1:8124;
  listener только `127.0.0.1`; после закрытия окна процесса/listener нет.
- Три режима: GSN total **131250**, GSV total **105525**, combined total
  **145950** (HTTP 200, реальные ответы в логе).
- Русский runtime failure path: `Не удалось запустить СС.Расчет…`, native
  message box с title `СС.Расчет`, exit 1, порт не занят.

### GUI uninstall

Интерактивный `unins000.exe` (реальные окна): подтверждение
`Вы действительно хотите удалить СС.Расчет и все компоненты программы?`
(кнопки «Да»/«Нет»), затем
`Программа СС.Расчет была полностью удалена с вашего компьютера.` (кнопка
«ОК»). Uninstaller — русский.

После uninstall: каталог установки и exe отсутствуют, Start Menu и Desktop
ярлыки удалены, HKCU uninstall key отсутствует. Пользовательские markers
Documents/Desktop/`%LOCALAPPDATA%\GasProjectCalculator` сохранены с теми же
SHA256; user data dir существует. Логи:
`logs/RD-03-uninstall-gui.txt`, `logs/RD-03-uninstall-gui-final.txt`.

## Setup error dialog (C2 correction, R3-2)

Дополнительный прогон закрывает finding RD03-F01 (R3-2): реальный error-dialog
самого установщика. Исполнитель — OpenCode Flash worker, dispatch
`ctx_2b97c2f59827`, task `task_c7fab3f54056`. Продуктовый код, installer script
и тесты не менялись; артефакт не пересобирался.

- Артефакт под тестом (exact): `installer\Output\
  GasProjectCalculator-Setup-1.0.0.exe`, 15 273 647 bytes, SHA256
  `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`.
- CWD: `D:\Antigravity\GasProjectCalculator`.
- Точная команда запуска (GUI, без silent-флагов):

  ```text
  D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe /DIR=C:\Windows\System32\RD03-Forbidden
  ```

- Метод провокации: выбран несуществующий и недоступный для записи каталог
  установки. В интерактивном мастере реальными нажатиями кнопок пройдены
  welcome → dir → tasks → ready и нажата `Установить`; Setup попытался создать
  каталог и показал нативный русский error-dialog.
- Реальный native window capture: `docs/screenshots/rd-03-setup-error.png`
  (322×179, 8 953 bytes, SHA256
  `02E788748F23C5E3B6AC1FB5991AF93FF415509F5E1162208890130F2867267C`).
- Error-dialog №1: title **`Установка`**, button **`ОК`**, body:

  ```text
  Невозможно создать папку "C:\Windows\System32\RD03-Forbidden".

  Ошибка 5: Отказано в доступе.
  ```

- После нажатия `ОК` Setup показал второй русский dialog: title **`Ошибка`**,
  button **`ОК`**, body:

  ```text
  Установка не была завершена.

  Пожалуйста, устраните проблему и запустите установку снова.
  ```

- Оба dialog закрыты нажатием `ОК`; установщик завершился сам. Exit code
  процесса installer — **4**; installer-процессов после завершения — 0.
- Cleanup proof (см. `logs/RD-03-setup-error-cleanup.txt`): каталог установки
  отсутствует; `C:\Windows\System32\RD03-Forbidden` не создан; blocker-файл
  не использовался и отсутствует; HKCU uninstall key отсутствует; Start
  Menu/Desktop ярлыки отсутствуют; лог `C:\Windows\System32\rd03-forbidden.log`
  отсутствует. `:8000` PID 12888 и `:8138` PID 23152 живы.
- SHA256 официального артефакта после попытки повторно проверен и совпадает:
  `043884…949A`; пересборка не выполнялась. Raw window/automation log:
  `logs/RD-03-setup-error.txt`.

## Frozen checklist R3-1..R3-13

| ID | Результат (кандидат) | Evidence |
| --- | --- | --- |
| R3-1 | Чистая x64-сборка installer: команды/CWD/exit 0/логи, artifact 15 273 647 bytes, SHA256 `043884…949A` | `logs/RD-03-packaging-build.out.txt`, `logs/RD-03-installer-build-final.out.txt`; Inno 6.4.1, `ArchitecturesAllowed=x64compatible` |
| R3-2 | Мастер полностью русский: welcome, dir, tasks, ready, finish; кнопки/текст русские; error-dialog мастера русский; uninstaller русский | `docs/screenshots/rd-03-wizard-welcome.png`, `-dir`, `-tasks`, `-ready`, `-finish`; `rd-03-setup-error.png`; `rd-03-uninstall-confirm.png`, `rd-03-uninstall-complete.png`; `logs/RD-03-setup-error.txt`; сборка читает `Languages\Russian.isl` (build log) |
| R3-3 | Ярлык и приложение ровно `СС.Расчет` | `RD-03-install-no-desktop.txt` (DisplayName, shortcut name/target/WorkingDir), `RD-03-reinstall-desktop-final.txt`; runtime `MainWindowTitle: СС.Расчет`; лог/скриншот окна |
| R3-4 | Start Menu всегда; Desktop опционален (без task — нет, с task — есть) | `RD-03-install-no-desktop.txt` (`exists: False`), `RD-03-reinstall-desktop-final.txt` (`exists: True`); задача `desktopicon` unchecked по умолчанию (`rd-03-wizard-tasks.png`) |
| R3-5 | Тихая per-user установка без admin/UAC | Exit 0; HKCU key есть, HKLM key нет; Inno log `User privileges: None`, `Administrative install mode: No`, `HKEY_CURRENT_USER`; shell не elevated |
| R3-6 | Установленное приложение без Python/консоли | PE subsystem 2 GUI; PATH-stripped launch, `python` not found; приложение стартует (`RD-03-runtime.txt`) |
| R3-7 | Заставка и окно после readiness в установленной версии | `rd-03-installed-splash.png` (520×320), `rd-03-installed-main.png` (1050×740, title `СС.Расчет`); `RD-03-installed-app.txt` (splash shown → backend ready 0.73 s → main shown) |
| R3-8 | Три режима 131250/105525/145950 в установленном приложении | `RD-03-runtime.txt`: реальные HTTP 200 ответы `/calculate`, `/calculate/gsv`, `/calculate/combined` с точными total |
| R3-9 | Loopback-only, port conflict, close освобождает порт | `RD-03-runtime.txt`: listener `127.0.0.1:8124` only; 8123 busy → 8124; exit 0, listeners after exit `<none>`; `RD-03-network-unchanged.txt`: :8000 PID 12888 жив, :8138 PID 23152 не тронут, 8123/8124/8125 свободны |
| R3-10 | Reinstall поверх установки, user files сохранены | `RD-03-reinstall-desktop.txt`, `-final.txt`: exit 0, shortcuts обновлены; markers SHA256 не изменились |
| R3-11 | Uninstall русский, удаляет программу/ярлыки, сохраняет user files | `rd-03-uninstall-confirm.png`, `-complete.png`; `RD-03-uninstall-gui.txt`, `-gui-final.txt`: exe/dir/shortcuts/HKCU key удалены, markers сохранены |
| R3-12 | Developer path/suite не сломаны | `RD-03-suite.txt`: `Ran 163 tests ... OK`; `RD-03-suite-exit.txt`: `SUITE_EXIT=0`; `RD-03-git.txt`: diff app/main.py/calculators пуст; :8000 PID 12888 жив |
| R3-13 | Реальные скриншоты installer и installed app | 10 файлов `docs/screenshots/rd-03-*.png` (см. таблицу ниже) |

## Скриншоты (реальные, native window capture)

| Файл | Размер | SHA256 |
| --- | --- | --- |
| `rd-03-wizard-welcome.png` | 54 587 | `ED139A2025CFDF71867535E4C31244DF891E1306E63E557BC262BE2E06D05DD4` |
| `rd-03-wizard-dir.png` | 44 791 | `8A3C56EC1ED6699DB72D2EB162433584F22D027426B12B6404302115FA3B6162` |
| `rd-03-wizard-tasks.png` | 42 151 | `C2B72DEE99DBE1409349D31DE9A723D25DE961A93646E74CE22B381CB6A1934D` |
| `rd-03-wizard-ready.png` | 44 493 | `C5681CED6D67F23F328F389CA5B519C6173E5C43949FB2B5B650B59DFB2C2AE7` |
| `rd-03-wizard-finish.png` | 53 895 | `83C10A9DC81D19D9E5F050470C4F47FA941C3D6C7AE2794EE193FA5BD3CF1204` |
| `rd-03-installed-splash.png` | 83 402 | `615D2F45DD896A1138AF0938A9FFD39774C28287ED212E7652B75C6523493657` |
| `rd-03-installed-main.png` | 144 083 | `113D31323BA0523663056EC99C4B5CAE5072B7C8DED44676073152F1CBCF82E4` |
| `rd-03-uninstall-confirm.png` | 18 990 | `94EF0071CEF9212AEA406B626404A13DD4B6CA126E5CEFFC31BF143B5A62CE48` |
| `rd-03-uninstall-complete.png` | 19 151 | `C75526B3687AE28E6EE3FD469343DE00CFCCE035EF5977DB73B9BFAB2A61413A` |
| `rd-03-setup-error.png` | 8 953 | `02E788748F23C5E3B6AC1FB5991AF93FF415509F5E1162208890130F2867267C` |

Снимок `rd-03-setup-error.png` — нативный error-dialog установщика
(`Установка` → `Невозможно создать папку … Ошибка 5: Отказано в доступе.`),
снят в C2-correction прогоне, см. раздел «Setup error dialog».

Примечание к wizard-снимкам: welcome/dir/tasks/ready/finish сняты в одном
прогоне финального установщика (`RD-03-wizard-final.txt`); install завершён,
финишная страница закрыта без запуска приложения.

## Логи

- `logs/RD-03-packaging-build.out.txt` / `.err.txt` — PyInstaller.
- `logs/RD-03-installer-build-final.out.txt` — Inno Setup compile.
- `logs/RD-03-install-no-desktop.txt`, `logs/RD-03-inno-install-no-desktop.txt` — clean silent install.
- `logs/RD-03-reinstall-desktop.txt`, `logs/RD-03-inno-reinstall-desktop.txt` — reinstall + desktop task.
- `logs/RD-03-reinstall-desktop-final.txt`, `logs/RD-03-inno-reinstall-desktop-final.txt` — финальный reinstall.
- `logs/RD-03-wizard-final.txt`, `logs/RD-03-inno-gui-install.txt` — GUI wizard (5 страниц, exit/закрытие).
- `logs/RD-03-installed-app.txt` — splash/readiness/main window установленного приложения.
- `logs/RD-03-runtime.txt` — PE/PATH/три режима/loopback/port close/русская ошибка.
- `logs/RD-03-uninstall-gui.txt`, `logs/RD-03-uninstall-gui-final.txt` — GUI uninstall и конечное состояние.
- `logs/RD-03-uninstall-reset2.txt`, `logs/RD-03-inno-uninstall-reset.txt` — сброс перед clean install.
- `logs/RD-03-old-uninstall.txt`, `logs/RD-03-inno-old-uninstall.txt` — удаление прежней установки этапа до RD-03 (markers сохранены).
- `logs/RD-03-suite.txt`, `logs/RD-03-suite-exit.txt` — полный suite.
- `logs/RD-03-git.txt` — branch/HEAD/status/diff/hashes.
- `logs/RD-03-network-unchanged.txt` — :8000/:8138 и отсутствие тестовых listeners/процессов.
- `.log`-файлы рядом — исходные Inno logs; `*.log` в `.gitignore`, поэтому
  для репозитория приложены `.txt`-копии с теми же байтами.
- `logs/RD-03-setup-error.txt` — C2 correction: raw window/automation log
  реального русского setup error dialog (title/body кнопки, exit code 4).
- `logs/RD-03-setup-error-cleanup.txt` — cleanup proof и SHA256 recheck
  артефакта/скриншота после error-прогона.
- `logs/RD-03-wizard-error.txt` — историческая неудачная попытка снять
  setup-error dialog; не используется как evidence (заменена C2-прогоном).

## NOT_RUN / остаточные риски

- RESOLVED (C2 correction): отдельный скриншот ошибки самого мастера установки
  снят реально через `/DIR=C:\Windows\System32\RD03-Forbidden`; получены два
  русских error-dialog, native screenshot `docs/screenshots/rd-03-setup-error.png`,
  exit code 4, cleanup подтверждён. Подробности — раздел «Setup error dialog
  (C2 correction, R3-2)» и `logs/RD-03-setup-error*.txt`. Предыдущая неудачная
  попытка (`logs/RD-03-wizard-error.txt`) оставлена как историческая и больше
  не используется в качестве evidence.
- Никакой подписи, автообновления, телеметрии, cloud-вызовов и публикации не
  добавлялось; артефакт остаётся локальным и не коммитится.
- GUI-автоматизация выполнялась реальными keystrokes/BM_CLICK и
  native-снимками окон в интерактивной сессии; фоновые процессы/серверы после
  проверок не оставлены.
- Прежняя установка предыдущего этапа была удалена в ходе проверки clean
  install; пользовательские данные вне каталога установки сохранены, прежний
  installer artifact сохранён в `installer/Output/legacy/`.
- Независимый R2 review и проектный PASS — за координатором/ревьюером; здесь
  PASS не заявляется.
