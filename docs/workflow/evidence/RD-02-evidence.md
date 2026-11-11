# RD-02 evidence — бренд native window и локальная startup-заставка (R2)

Исполнитель: отдельный Orca worker OpenCode Flash, dispatch `ctx_b89935976cc0`,
task `task_e59117ab6038`, terminal `term_4c6fe15a-4003-4cb9-92d0-a80e6dfb27a1`.
Это evidence исполнителя; проектный PASS не заявляется.

## Workspace / baseline

- CWD: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/ss-calculator-redesign`
- Продуктовый baseline RD-02: `041b13d` (RD-01 accepted/committed).
- HEAD на момент работы: `2703e83` — координаторский workflow-коммит
  «record RD-01 PASS and RD-02 dispatch», сделанный во время работы worker.
  Он затронул только `docs/workflow/HISTORY.md` и `STATE.md`; worker их не
  менял и не отбрасывал.
- В начале работы worktree содержал незакоммиченные `STATE.md`/`HISTORY.md`
  координатора; они сохранены. Своих коммитов worker не делал.
- :8000 (PID 12888) и диагностический :8138 (PID 23152) не останавливались и
  не менялись. Push/merge/deploy не выполнялись.

## Что изменено (только allowlist)

- `app/desktop_launcher.py`:
  - `APP_TITLE = "СС.Расчет"`; `APP_WIDTH=1050`, `APP_HEIGHT=740`,
    `APP_MIN_SIZE=(860, 620)`.
  - Локальная frameless splash-заставка 520×320 из `file://`-URI; backend
    стартует только после события `shown` заставки; main window создаётся
    скрытой после readiness, затем заставка закрывается и main показывается.
  - Ошибки старта: заставка закрывается, показывается русское сообщение,
    backend останавливается в `finally`.
  - Диагностические хуки: `--splash-hold-seconds` и `--force-reduced-motion`
    (не влияют на обычный запуск), плюс прежние `--port-file`,
    `--auto-close-seconds`, `--simulate-startup-failure`, `--no-error-dialog`.
  - Русский текст ошибки брендирован: «Не удалось запустить СС.Расчет.».
- `frontend/splash.html` (новый): локальная русская страница, SVG-труба с
  потоком газа к дому, relative asset `assets/company-emblem.png`, CSS
  `prefers-reduced-motion`, без внешних URL/шрифтов/сети.
- `app/resources.py`: `splash_page_path()` (+ читаемая ошибка при отсутствии).
- `packaging/GasProjectCalculator.spec`: splash и `frontend/assets` добавлены
  в `datas`.
- `tests/test_desktop_launcher.py`: +10 новых и 1 изменённый тест
  (title/geometry/splash/no-network/reduced-motion/error brand).
- Evidence/screenshots в разрешённых путях. `app/main.py`,
  `app/calculator.py`, `app/gsv_calculator.py`, `frontend/index.html`,
  installer и user data не менялись.

## Команды / exit codes

| Команда (CWD = workspace) | Exit |
| --- | --- |
| `python -m app.desktop_launcher --preferred-port 8099 --auto-close-seconds 5 --log-file <RD-02-normal.log>` | 0 |
| `python -m app.desktop_launcher --preferred-port 8000 --auto-close-seconds 5 --log-file <RD-02-portskip.log>` | 0 |
| `python -m app.desktop_launcher --preferred-port 8098 --splash-hold-seconds 10 --auto-close-seconds 15 ...` | 0 |
| `python -m app.desktop_launcher --preferred-port 8093 --simulate-startup-failure --no-error-dialog ...` | 1 |
| `python -m app.desktop_launcher --preferred-port 8094 --simulate-startup-failure ...` (диалог закрыт WM_CLOSE) | 1 |
| `python -m unittest tests.test_desktop_launcher -v` | 0 (23 OK) |
| `python -m unittest discover -s tests` | 0 (163 OK) |
| Windows PowerShell: `Get-NetTCPConnection`, enumeration Win32 окон, screen capture | 0 |
| Orca agent-browser: `tab create`, `eval`, `set media`, `screenshot` | 0 |

Полный suite после финального изменения: `Ran 163 tests ... OK`, EXIT=0
(`logs/RD-02-suite.txt`). До RD-02 baseline было 152 теста; +11.

## Final diff / status

`git status --short` (продуктовые/тестовые файлы и evidence):

```
 M app/desktop_launcher.py
 M app/resources.py
 M packaging/GasProjectCalculator.spec
 M tests/test_desktop_launcher.py
?? frontend/splash.html
?? docs/screenshots/rd-02-*.png
?? docs/workflow/evidence/logs/RD-02-*
```

`git diff --stat` (без evidence): 4 files, +342/−59. API/calculator diff и
`frontend/index.html` diff от `041b13d` пустые (`RD-02-git.txt`).

SHA256:

- `frontend/splash.html`: `56B6E257D506F9CC2E4D487419BBA2FF3E1E6A354BF24641BAB8CEAE65BE3755`
- `app/desktop_launcher.py`: `36A33602D2993FF5B5417DF4DEADE12903BBFED2FA1ECFD75CAEF6882A91E1AC`
- `docs/screenshots/rd-02-splash.png`: `51222A957253F803451B97B1E6BE03143CF03961BC95176ACEC2721BD8C10032`
- `docs/screenshots/rd-02-main-window.png`: `2C6D675124C15F9496FB696D795144E5116A5725E0BE6202359776425ACCDD86`
- `docs/screenshots/rd-02-splash-reduced-motion.png`: `4FF6D07B42125F45D49D5872067BF6C1C034FC44EF22EECF8FD09E5B404531D2`
- `docs/screenshots/rd-02-failure-dialog.png`: `24ADB4FC7A0164980B1292997CC89F732B5E7D581C1B12FECC03162A1A2252D6`

## Frozen checklist R2-1..R2-11

| ID | Результат (кандидат) | Evidence |
| --- | --- | --- |
| R2-1 | Title окна ровно `СС.Расчет` | `RD-02-title-size.json` (`title: "СС.Расчет"`), `RD-02-main-window.json`, лог строка `title='СС.Расчет'`; title bar виден на `rd-02-main-window.png` |
| R2-2 | Размер 1050×740; минимум 860×620 | `RD-02-title-size.json`: outer `[1050,740]`, client `[1034,701]`, dpi 96; `RD-02-main-window.txt`: `AFTER_RESIZE_REQUEST 300x200 -> outer=860x620`; лог `width=1050 height=740 min_size=(860, 620)` |
| R2-3 | Реальная заставка видна во время старта backend | `rd-02-splash.png` (реальный native-снимок 520×320); `RD-02-splash-window.json` (splash visible=true 520×320, main hidden 1050×740); лог: `shown 00:22:32.851` → `starting backend` → `ready 00:22:34.354` |
| R2-4 | Заставка исчезает при readiness; main после readiness | `RD-02-normal-launcher.txt`: readiness `00:23:51.142` → main created `…51.183` → splash closed `…51.225` → main shown `…51.249`; `rd-02-main-window.png` после readiness |
| R2-5 | Нет искусственной задержки | readiness elapsed `0.75s`; main shown через ~107 мс после readiness (нормальный запуск без hold). `--splash-hold-seconds` в обычном запуске не задаётся |
| R2-6 | Reduced motion уважается | CSS `prefers-reduced-motion: reduce` + `data-reduced-motion`; `RD-02-browser.txt`: emulated `media=true`, `.g1 animationName=none`, duration `0s`, статичные transform 0/70/140/210px; `rd-02-splash-reduced-motion.png` |
| R2-7 | Заставка не использует сеть | `splash.html` без `http://`/`https://`/`@import`/CDN (тест); URI лога `file:///D:/…/splash.html`; `RD-02-browser.txt`: `protocol:"file:"`, `resourceEntries:[]`, element URLs только локальный `assets/company-emblem.png` |
| R2-8 | Ошибка старта: заставка закрыта, русская ошибка, backend не оставлен | `RD-02-failure-nodialog-launcher.txt`: splash shown → failure → `splash closed after startup failure` → русский текст → exit 1 → `Backend stopped`; listener :8093 = 0; `rd-02-failure-dialog.png` — реальный MessageBox «Не удалось запустить СС.Расчет…»; `RD-02-failure-dialog-launcher.txt` |
| R2-9 | Lifecycle: loopback-only, port skip, close stops backend | `RD-02-network.txt`: preferred 8000 занят → selected `127.0.0.1:8001`, во время работы listener только `127.0.0.1:8001`, после close — 0; :8000 PID 12888 всё время жив; developer uvicorn :8138 PID 23152 не затронут |
| R2-10 | Developer uvicorn и suite не сломаны | `RD-02-suite.txt`: `Ran 163 tests ... OK`, EXIT=0; `RD-02-git.txt`: diff `app/main.py`/calculators/`frontend/index.html` пуст; :8000 работает |
| R2-11 | Новые/изменённые тесты покрывают title/size/splash helper | `tests.test_desktop_launcher` 23 OK: `test_app_title_is_exact_brand`, `test_window_geometry_matches_approved_design`, `test_splash_page_resolves_from_source`, `test_splash_is_russian_local_page`, `test_splash_has_no_network_references`, `test_splash_emblem_is_a_local_file`, `test_splash_respects_reduced_motion`, `test_splash_animates_gas_flow_to_house`, `test_splash_url_is_local_file_uri`, `test_splash_url_diagnostic_reduced_motion_flag`, `test_error_message_uses_brand` |

## Порядок событий (нормальный запуск, PID 20960)

```
00:23:49.067  splash window created 520x320 (file:///…/splash.html)
00:23:49.640  splash shown; starting backend
00:23:50.341  selected loopback 127.0.0.1:8099
00:23:51.142  backend ready (elapsed 0.75s)
00:23:51.183  main window created hidden (title СС.Расчет, 1050x740)
00:23:51.225  splash closed
00:23:51.249  main window shown
00:23:56.727  main closed → backend stopped → exit 0
```

Заставка показывается до старта backend и живёт только до readiness; main
появляется после readiness. Время от readiness до появления main — 107 мс,
искусственной минимальной длительности нет.

## Скриншоты

- `docs/screenshots/rd-02-splash.png` — реальная native-заставка (520×320).
- `docs/screenshots/rd-02-main-window.png` — реальное окно после readiness
  (title `СС.Расчет`, 1050×740).
- `docs/screenshots/rd-02-splash-reduced-motion.png` — splash под emulated
  `prefers-reduced-motion: reduce` (статичное состояние).
- `docs/screenshots/rd-02-failure-dialog.png` — реальный русский error dialog.

## Логи

- `RD-02-normal-launcher.txt` — нормальный запуск/ready/close (raw launcher log).
- `RD-02-splash-hold-launcher.txt` — диагностический hold для снимка заставки.
- `RD-02-portskip-launcher.txt` — preferred 8000 busy → 8001.
- `RD-02-failure-nodialog-launcher.txt` — failure без диалога.
- `RD-02-failure-dialog-launcher.txt` — failure с реальным диалогом.
- `RD-02-network.txt` — netstat до/во время/после, :8000/:8138.
- `RD-02-title-size.json`, `RD-02-main-window.json`, `RD-02-splash-window.json` —
  реальные Win32 title/outer/client/DPI.
- `RD-02-main-window.txt`, `RD-02-splash-capture.txt` — PowerShell capture и
  min-size clamp.
- `RD-02-browser.txt` — Orca browser computed styles, emulated reduced motion,
  локальные URL.
- `RD-02-suite.txt` — полный suite.
- `RD-02-git.txt` — branch/HEAD/status/diff.
- `.log`-файлы рядом — исходные launcher-логи; `*.log` в `.gitignore`,
  поэтому в репозиторий включены `.txt`-копии.

## NOT_RUN / остаточные риски

- NOT_RUN: пересборка PyInstaller/installer и проверка splash в упакованном
  артефакте — это RD-03; installer не менялся.
- NOT_RUN: изменение глобальной настройки Windows «animation effects»;
  reduced motion проверен CDP-эмуляцией `prefers-reduced-motion` и
  диагностическим флагом. Диагностические флаги на обычный запуск не влияют.
- NOT_RUN: независимое R2-ревью, commit/push/merge/deploy — за координатором.
- Остаточный риск: splash требует инициализации WebView2 (~0.5–0.6 c) до старта
  backend; это время отрисовки заставки, не искусственная задержка. Main
  появляется сразу после readiness.
- Остаточный риск: splash и главное окно используют один title; splash
  frameless и закрывается автоматически.
