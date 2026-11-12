# MD-03 evidence — локальный installer 1.1.0 и установленная программа

Дата: 2026-11-12. Исполнитель: OpenCode (Orca dispatch MD-03).
Reviewer: Codex `gpt-6.1-sol` high (R2). **Product verdict: NOT_REVIEWED**
(исполнитель не выставляет PASS).

## Baseline, workspace, scope

- Workspace/CWD: `D:\Antigravity\GasProjectCalculator`.
- Ветка: `feature/gsv-mixed-diameters` (не переключалась).
- Baseline HEAD: `fb080aa9dfcb7420fa83ff32cdc52e223ac96dd5` — MD-02 R2 PASS
  (`feat(ui): mixed GSV lengths, server billing detail, reference artwork`).
- Изменённый tracked-файл: только `installer/GasProjectCalculator.iss`
  (AppVersion `1.1.0`, VersionInfoVersion `1.1.0.0`; AppId сохранён).
- Новые untracked-файлы: `docs/screenshots/md-03-*`,
  `docs/workflow/evidence/logs/MD-03-*`, этот evidence.
- `app/`, `frontend/`, `tests/`, `requirements*`, VISION/ARCHITECTURE/ROADMAP/
  workflow docs (кроме evidence) не изменялись.
- Commit/push/merge/deploy/release/signing не выполнялись. Артефакт передан
  локально; commit — за координатором после routed PASS.

Baseline и scope: `logs/MD-03-baseline.txt`, `logs/MD-03-git-status.txt`,
`logs/MD-03-diff-names.txt`, `logs/MD-03-diff-stat.txt`,
`logs/MD-03-scope.txt`.

```text
 installer/GasProjectCalculator.iss | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
```

## Build и artifact chain

Toolchain: Python 3.12.4 `.venv`, PyInstaller 6.22.3, Inno Setup
`C:\Users\user\AppData\Local\Programs\Antigravity IDE\resources\app\node_modules\innosetup\bin\ISCC.exe`
(with `ISCmplr.dll`), локально, без сети и без подписи.
`logs/MD-03-toolchain.txt`.

| Шаг | Команда | CWD | Exit | Evidence |
| --- | --- | --- | ---: | --- |
| Packaged app | `pwsh -NoProfile -File packaging\build.ps1` | workspace | 0 | `logs/MD-03-packaging-build.out.txt`, `.exit.txt` |
| Installer 1.1.0 | `pwsh -NoProfile -File installer\build-installer.ps1` | workspace | 0 | `logs/MD-03-installer-build.out.txt`, `.exit.txt` |

Артефакты:

| Артефакт | Path | Size | SHA256 |
| --- | --- | ---: | --- |
| Installer 1.1.0 | `installer\Output\GasProjectCalculator-Setup-1.1.0.exe` | 15 293 993 | `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710` |
| Packaged app | `dist\GasProjectCalculator\GasProjectCalculator.exe` | 6 839 201 | `F374EEED2535BBDDD024AEBFA8B562642A010F28804C7BEB4A0755C53F459690` |

Version metadata: FileVersion `1.1.0.0`, ProductVersion `1.1.0`,
ProductName/FileDescription содержат `СС.Расчет`; AppId
`{A3E4B6C1-7F2D-4B8E-9C1A-5D6E7F8091A2}` сохранён; OutputBaseFilename
`GasProjectCalculator-Setup-1.1.0`. `logs/MD-03-versioninfo.json`,
`logs/MD-03-iss-metadata.txt`. Authenticode: `NotSigned`
(`logs/MD-03-signing.txt`).

### Прежние артефакты не изменены

Pre-build и final size/SHA256 совпадают; опубликованный v1.0.0 не заменялся:

| Артефакт | Size | SHA256 | Unchanged |
| --- | ---: | --- | --- |
| `installer\Output\GasProjectCalculator-Setup-1.0.0.exe` | 15 286 980 | `71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08` | да |
| `installer\Output\legacy\GasProjectCalculator-Setup-1.0.0-pre-compact.exe` | 15 273 647 | `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A` | да |
| `installer\Output\legacy\GasProjectCalculator-Setup-1.0.0-previous-stage.exe` | 15 256 037 | `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F` | да |

Evidence: `logs/MD-03-pre-artifact-hashes.txt`,
`logs/MD-03-post-build-legacy-hashes.txt`,
`logs/MD-03-legacy-compare.txt` (`ALL_UNCHANGED=True`),
`logs/MD-03-final-artifact-hashes.txt`.

## Isolated install, backup и restore

Изолированный test instance:
`C:\Users\user\AppData\Local\Temp\opencode\md-03\install` (вне workspace и вне
пользовательской установки). Пользовательская установка
`%LOCALAPPDATA%\Programs\GasProjectCalculator` и её процесс PID 13248 не
останавливались и не изменялись.

Backup перед тестом: HKCU uninstall key экспортирован в
`...\md-03\backup\uninstall-key.reg`; Start Menu и Desktop ярлыки скопированы
в `...\backup\start-menu.lnk`, `...\backup\desktop.lnk`.
`logs/MD-03-backup.txt`.

Интерактивный русский wizard установил 1.1.0 в изолированный каталог
(exit wizard: finish page достигнута; установка завершена), затем выполнялся
reinstall с desktop task и uninstall. После uninstall HKCU key и оба ярлыка
восстановлены из backup; восстановлены значения 1.0.0, пользовательский
install dir и ярлыки на него: `logs/MD-03-restore.txt`.

Пользовательская установка до/после/в конце: 106 файлов, 37 372 847 B,
exe SHA256 `5E25FA92A530E104AA69BC7153C068FA34C477659F375142EA7D047257A0FBA3`,
PID 13248 жив: `logs/MD-03-user-install-snapshot-before.txt`,
`...-after-wizard.txt`, `...-final.txt`.

## Installer flow (RU wizard, shortcuts, reinstall, uninstall)

- Русский wizard: welcome, directory, tasks, ready, finish —
  `docs/screenshots/md-03-wizard-{welcome,dir,tasks,ready,finish}.png`.
- На tasks page виден optional task «Создать ярлык на рабочем столе»,
  checkbox по умолчанию **снят** (`md-03-wizard-tasks.png`). Start Menu
  создаётся всегда.
- После интерактивной установки HKCU: DisplayVersion `1.1.0`,
  InstallLocation = isolated dir; Start Menu на isolated exe.
  `logs/MD-03-install-state.txt`.
- Reinstall (silent, `/DIR=<isolated> /TASKS="desktopicon"`): exit 0,
  DisplayVersion 1.1.0; Start Menu и Desktop ярлыки указывают на isolated exe;
  `logs/MD-03-reinstall.txt`.
- Uninstall (`unins000.exe /VERYSILENT`): exit 0; program files, обе ярлыка и
  HKCU key удалены; пользовательские marker-файлы в Documents, Desktop и
  `%LOCALAPPDATA%\GasProjectCalculator` сохранены; user data dir сохранён.
  `logs/MD-03-uninstall.txt`, `.exit.txt`.
- Пользовательские ярлыки/HKCU восстановлены; опубликованный v1.0.0 и
  пользовательская установка не затронуты (`logs/MD-03-restore.txt`).

## Установленная программа без Python/CLI, lifecycle

`installer\verify-runtime.ps1` на установленном 1.1.0: exit 0.
`logs/MD-03-runtime.txt`, `.exit.txt`.

- PE subsystem 2 (`WINDOWS_GUI`, без консоли); PATH очищен от Python —
  установленный exe всё равно запускается.
- Backend только `127.0.0.1`; занятый тестовый порт `8123` пропущен,
  выбран `8124`.
- Native splash → readiness → main window; title `СС.Расчет`; окно появляется
  после readiness.
- Закрытие окна завершает backend: процесс exit 0, listener на порту исчез,
  дочерних процессов после выхода нет.
- Русский native launch-failure dialog, exit 1, `status=failed` port file.

Отдельный native instance 1.1.0: pid 1684, port 8160. Splash снят реальным
`PrintWindow` (`md-03-native-splash.png`, 520×320); main window 800×540
(`md-03-native-window.png`); close → process exited, listener 8160 отсутствует,
дочерних процессов 0 (`logs/MD-03-native-close.txt`).

## Native screenshots и метрики

Win32 `PrintWindow` с `PW_RENDERFULLCONTENT`, DPI 96. `scrollY=0` после каждого
расчёта; action и итог в viewport.

| Размер | Outer | Client | DPI |
| --- | --- | --- | ---: |
| target | 800×540 | 784×501 | 96 |
| min | 760×520 | 744×481 | 96 |

| Состояние | Итог | scroll | hScroll/vScroll | submit в viewport | итог в viewport | таблица влезает |
| --- | ---: | --- | --- | --- | --- | --- |
| target ГСН | 68 250 ₽ | 0,0 | нет/нет | да | да | — |
| target ГСВ D1 | 75 600 ₽ | 0,0 | нет/нет | да | да | да |
| target ГСВ D2 | 79 275 ₽ | 0,0 | нет/нет | да | да | да |
| target ГСВ D3 | 71 400 ₽ | 0,0 | нет/нет | да | да | да |
| target ГСВ D4 | 63 000 ₽ | 0,0 | нет/нет | да | да | да |
| target ГСВ D5 | 70 875 ₽ | 0,0 | нет/нет | да | да | да |
| target combined | 158 550 ₽ | 0,0 | нет/нет | да | да | да |
| min ГСН | 68 250 ₽ | 0,0 | нет/нет | да | да | — |
| min ГСВ D1 | 75 600 ₽ | 0,0 | нет/нет | да | да | да |
| min combined | 158 550 ₽ | 0,0 | нет/нет | да | да | да |

Скриншоты: `md-03-native-target-{gsn,combined}.png`,
`md-03-native-target-gsv-D1..D5.png`, `md-03-native-min-{gsn,combined}.png`,
`md-03-native-min-gsv-D1.png`, `md-03-native-422.png`,
`md-03-native-target-combined-detail.png`,
`md-03-native-min-combined-detail.png`. Полные метрики:
`logs/MD-03-native.json`, `logs/MD-03-native-summary.txt`,
`logs/MD-03-native-run.txt`.

Три поля (`до Ø25`, `Ø32–40`, `Ø57`), общий метраж и серверная детализация
видны в target и min; нулевые позиции отображаются. В combined детализация
ГСВ прокручивается внутри карточки, итог/кнопка остаются вне её; для полной
детализации снят `*-combined-detail.png`.

## Mixed-эталоны (реальные запросы/ответы установленного backend)

`logs/MD-03-api-summary.txt`, `logs/MD-03-api.json`,
`logs/MD-03-api-run.txt` (exit 0).

| Case | Ввод (до25/32–40/57) | total_length | total | Ожидалось |
| --- | --- | ---: | ---: | ---: |
| D1 | 4 / 0 / 4 | 8 | 75 600 | 75 600 |
| D2 | 2 / 4 / 3 | 9 | 79 275 | 79 275 |
| D3 | 0 / 5 / 2 | 7 | 71 400 | 71 400 |
| D4 | 3 / 1 / 1 | 5 | 63 000 | 63 000 |
| D5 | 8 / 0 / 0 | 8 | 70 875 | 70 875 |

- Combined: GSN 10 м 75 600 + ГСВ 4/0/4 82 950 (район) → subtotal 151 000,
  НДС 7 550, total **158 550**.
- Mixed + САКЗ 1 + ПК + район: 97 000 + НДС 4 850 = **101 850**.
- `pipe_breakdown` содержит category/length/included_length/billable_length/
  rate/surcharge для всех трёх позиций, включая нулевые; `total_length`
  серверный.
- Legacy форма `length`+`diameter`: 200, total **105 525**, старые ключи без
  `total_length`/`pipe_breakdown`.
- Смешение `pipe_lengths` с `length`/`diameter`: **422**; `has_panel` при
  `sakz_sets=0`: **422** (русский текст). WebView-запросы к установленному
  backend подтверждают те же ответы: `logs/MD-03-native-summary.txt`
  (`webview_legacy`, `webview_mixed_conflict`).

## ГСН/опции/НДС регрессия

- GSN 10 м, город, без опций: **68 250 ₽** (native + API).
- GSN legacy RD-03 пример: **131 250 ₽** (verify-runtime + API).
- Legacy GSV RD-03 пример: **105 525 ₽** (verify-runtime + API).
- САКЗ 0 → ПК `disabled=true, checked=false`; САКЗ 1 → `disabled=false`;
  возврат к 0 → снова disabled/снят (`logs/MD-03-native-summary.txt`,
  `sakz_panel`).
- Район +7 000 на раздел и НДС 5% применены в mixed/combined (101 850;
  158 550).
- 422 ПК при 0 САКЗ видим в native окне с русским текстом
  (`md-03-native-422.png`).

## Frozen acceptance checklist

| ID | Результат | Evidence |
| --- | --- | --- |
| B1 | Packaged app и installer 1.1.0 собраны из MD-02, exit 0 | build logs/exit, artifact hashes |
| B2 | FileVersion 1.1.0.0 / ProductVersion 1.1.0; AppId сохранён | `MD-03-versioninfo.json`, `MD-03-iss-metadata.txt` |
| B3 | 1.0.0, legacy и release bytes не изменены | pre/post/final hashes, `MD-03-legacy-compare.txt` |
| B4 | Изолированная установка; HKCU/ярлыки восстановлены; пользовательская установка не тронута | backup/install/restore logs, user snapshots |
| B5 | Установленная программа запускается без Python/CLI; splash/readiness | runtime log, `md-03-native-splash.png` |
| B6 | 75 600 / 79 275 / 71 400 / 63 000 / 70 875 и combined 158 550 | `MD-03-api-summary.txt`, native screenshots |
| B7 | Три длины, метраж, детализация; legacy/422 проверены | native screenshots, `MD-03-native-summary.txt`, API |
| B8 | ГСН-регрессия, САКЗ/ПК/район/НДС | values, runtime log, `md-03-native-422.png` |
| B9 | loopback-only, занятый test-порт, close завершает backend | `MD-03-runtime.txt`, `MD-03-native-close.txt` |
| B10 | Русский wizard, Start Menu/optional Desktop, reinstall/uninstall с сохранением файлов | wizard screenshots, install/reinstall/uninstall logs |
| B11 | Нет diff в app/frontend/tests/requirements; suite отложен в MD-05 | `MD-03-diff-names.txt`, `MD-03-scope.txt` |
| B12 | Артефакт локально; signing/push/merge/deploy/release отсутствуют | artifact hash, `MD-03-signing.txt`, `MD-03-git-status.txt` |

## NOT_RUN

- Полный unit suite — отложен в MD-05 по TASK.
- Повторная browser-верификация не выполнялась: MD-02 browser evidence
  переиспользуется по review-policy; для MD-03 использованы real native
  screenshots и API установленной программы.
- Commit/push/merge/deploy/release/signing не выполнялись (запрещены TASK).
- Изменения `app/`, `frontend/`, `tests/`, `requirements*` не выполнялись.

## Риски / заметки

- Автоматизация интерактивного wizard потребовала повторов из-за стандартного
  Inno-диалога «Папка существует» (test install dir создавался заранее);
  итоговая установка, reinstall и uninstall завершились успешно. Промежуточные
  automation-логи сохранены как `MD-03-wizard-*`.
- `md-03-wizard-finish.png` снят `CopyFromScreen` и содержит фон Explorer по
  краю; содержимое finish-страницы (русский текст, checkbox запуска,
  «Завершить») читаемо. Welcome/dir/tasks/ready пересняты `PrintWindow` без
  перекрытия.
- В combined детализация ГСВ может прокручиваться внутри карточки на
  минимальном размере; итог и action видимы, page-level scroll отсутствует.
- Продуктовый PASS не выставляется: требуется независимый Codex R2 review и
  решение координатора о scoped commit.
