# RD-FINAL evidence — интегрированная финальная проверка (R0)

Проверяющий: OpenCode verifier (Orca worker), dispatch `ctx_1cb546ad517e`,
task `task_e08ed7f8ac7b`, terminal `term_2f6a9d9f-6bff-4ead-af43-d3ececc27e11`.
Роль — read-only проверка: файлы продукта не изменялись, коммитов/push/merge/
deploy/signing не выполнялось. Записаны только этот evidence pack и raw-логи
`docs/workflow/evidence/logs/RD-FINAL-*`. Проектный или этапный PASS здесь не
заявляется; итоговое решение — за координатором/Codex.

## Workspace / ревизии

- CWD: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/ss-calculator-redesign`
- Продуктовый baseline: `e24d806`
- Ревизия, назначенная dispatch: `c72979a`
- Фактический HEAD на момент проверки: `8c87e44`
  (`docs(workflow): record RD-04 acceptance and final verification dispatch`)
- `c72979a..8c87e44` затрагивает только `docs/workflow/HISTORY.md` и
  `docs/workflow/STATE.md` (+15/−6); продуктовые файлы идентичны. Все проверки
  выполнены на `8c87e44`.
- В начале проверки worktree был чист, кроме собственного
  `RD-FINAL-suite.txt`; в конце — только `RD-FINAL-*` логи verifier'а.
- `:8000` PID 12888 и `:8138` PID 23152 живы, не останавливались и не
  перезапускались (read-only spot check в `RD-FINAL-spotcheck.txt`).
- Push/merge/deploy/signing не выполнялись; сборка не пересобиралась.

## Frozen checklist RF-1..RF-10

| ID | Проверка | Наблюдаемый результат | Evidence |
| --- | --- | --- | --- |
| RF-1 | `git diff --stat e24d806..HEAD` соответствует scope редизайна | 111 files changed, 8156 insertions(+), 255 deletions(-). Продуктовый diff ограничен RD-01..RD-04 allowlist; `app/main.py`, `app/calculator.py`, `app/gsv_calculator.py`, `requirements.txt` не изменены. Координаторские — ARCHITECTURE/ROADMAP/workflow docs. Неожиданных файлов нет | `logs/RD-FINAL-git.txt` |
| RF-2 | Полный unittest suite, exit 0, точное число тестов | `Ran 163 tests in 2.045s`, `OK`, `SUITE_EXIT=0` | `logs/RD-FINAL-suite.txt` |
| RF-3 | Artifact существует; size/SHA256 совпадают с README и RD-03 evidence | `installer\Output\GasProjectCalculator-Setup-1.0.0.exe`, **15 273 647 bytes**, SHA256 **`043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`**, совпадает с README и RD-03 | `logs/RD-FINAL-artifact.txt` |
| RF-4 | App/installer screenshots существуют и непустые | 26 файлов `docs/screenshots/rd-*.png`, `ZERO_SIZE_COUNT=0`; evidence/reviews RD-01..RD-04 существуют и непустые | `logs/RD-FINAL-files.txt` |
| RF-5 | Title/shortcut `СС.Расчет`, subtitle, window/sizes | Reuse RD-02 (R2-1..R2-3) и RD-03 (R3-3/R3-5); spot check: `APP_TITLE="СС.Расчет"`, 1050×740, min 860×620, `<title>`/h1 `СС.Расчет`, subtitle `Калькулятор ГСН и ГСВ`, Inno `AppName="СС.Расчет"`, Start Menu всегда, Desktop по `desktopicon` unchecked | `logs/RD-FINAL-spotcheck.txt`, `RD-02-evidence.md`, `RD-03-evidence.md` |
| RF-6 | Три режима 131250/105525/145950 подтверждены | Reuse RD-01 (browser: 131 250 / 105 525 / 145 950 MATCH) и RD-03 (installed runtime HTTP 200: `131250.0`, `105525`, `145950`) | `logs/RD-01-browser.txt` L32-49, `logs/RD-03-runtime.txt` L51-62 |
| RF-7 | Splash lifecycle/no network/reduced motion доказаны | Reuse RD-02: `protocol:"file:"`, `resourceEntries:[]`, emulated `prefers-reduced-motion` → animation `none`/`0s`, splash shown → ready → main shown; R2 PASS | `RD-02-evidence.md` R2-6/R2-7, `logs/RD-02-browser.txt`, `logs/RD-02-normal-launcher.txt` |
| RF-8 | Installer RU; reinstall/uninstall сохраняют user files | Reuse RD-03: RU wizard + RU setup-error + RU uninstaller; reinstall exit 0; uninstall удаляет программу/ярлыки, markers Documents/Desktop/`%LOCALAPPDATA%` сохранены с теми же SHA256; C2 PASS, RD03-F01 CLOSED | `RD-03-evidence.md`, `logs/RD-03-reinstall-desktop-final.txt`, `logs/RD-03-uninstall-gui-final.txt`, `RD-03-review.md` |
| RF-9 | Расчёты/API/rates не изменены | Diff `e24d806..HEAD` по `app/main.py`, `app/calculator.py`, `app/gsv_calculator.py`, `requirements.txt` и по `tests/test_calculator.py`, `tests/test_gsv_calculator.py`, `tests/test_gsv_api.py` пуст; suite 163 OK | `logs/RD-FINAL-rf9-rf10.txt`, `logs/RD-FINAL-git.txt` |
| RF-10 | Нет undeclared файлов/secrets/binaries в git | Untracked только `RD-FINAL-*` логи verifier'а; добавленные binary/asset-файлы — только задекларированные PNG (эмблема/исходник/скриншоты); `SUSPICIOUS_COUNT=0`, `SECRET_HIT_COUNT=0`; installer artifact git-ignored и не tracked | `logs/RD-FINAL-rf9-rf10.txt`, `logs/RD-FINAL-spotcheck.txt` |

## Suite (единственный прогон)

- Команда: `.\.venv\Scripts\python.exe -m unittest discover -s tests`
- CWD: `D:\Antigravity\GasProjectCalculator`
- Exit: **0**
- Результат: `Ran 163 tests in 2.045s`, `OK`
- Raw log: `docs/workflow/evidence/logs/RD-FINAL-suite.txt`
- Прогон выполнен один раз на `8c87e44`. Лог был снят PowerShell-редиректом в
  UTF-16LE и затем перекодирован в UTF-8 без повторного запуска suite; текст
  вывода сохранён.

## Diff scope (RF-1)

`git diff --stat e24d806..HEAD` — 111 files, 8156 insertions(+), 255 deletions(-).
Категории:

- RD-01: `frontend/index.html`, `frontend/assets/company-emblem.png`,
  `tests/test_frontend_redesign.py`, `tests/test_main.py`,
  `assets/company-logo-source.png`, 12 скриншотов `rd-01-*`, RD-01 evidence/logs.
- RD-02: `app/desktop_launcher.py`, `app/resources.py`,
  `packaging/GasProjectCalculator.spec`, `frontend/splash.html`,
  `tests/test_desktop_launcher.py`, 4 скриншота `rd-02-*`, RD-02 evidence/logs.
- RD-03: `installer/GasProjectCalculator.iss`, `installer/verify-install.ps1`,
  `installer/verify-runtime.ps1`, `installer/verify-uninstall.ps1`,
  10 скриншотов `rd-03-*`, RD-03 evidence/logs.
- RD-04: `README.md`, RD-04 evidence.
- Координаторские workflow/design-документы: `ARCHITECTURE.md`, `ROADMAP.md`,
  `docs/workflow/APPROVALS.md`, `HISTORY.md`, `STATE.md`,
  `REDESIGN-BRIEF.md`, `REDESIGN-RECOVERY.md`, reviews, tasks.

Не изменены: `app/main.py`, `app/calculator.py`, `app/gsv_calculator.py`,
`requirements.txt`, calculation-тесты. Неожиданных/undeclared файлов нет.

## Artifact (RF-3)

| Поле | Значение |
| --- | --- |
| path | `installer\Output\GasProjectCalculator-Setup-1.0.0.exe` |
| exists | True |
| size | 15 273 647 bytes |
| SHA256 | `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A` |
| совпадение с README | да |
| совпадение с RD-03 evidence | да |
| git | `installer/Output/` в `.gitignore`; в git не tracked |

## File checks (RF-4/RF-5)

- 26 `docs/screenshots/rd-*.png`; все size > 0 (`ZERO_SIZE_COUNT=0`).
- RD-02 screenshots SHA256 совпадают с RD-02 evidence (splash, main-window,
  splash-reduced-motion, failure-dialog).
- RD-03 screenshots SHA256 совпадают с RD-03 evidence (wizard ×5, installed
  splash/main, uninstall ×2, setup-error).
- Evidence packs `RD-01..RD-04-evidence.md` и reviews `RD-01..RD-04-review.md`
  существуют и непустые.
- `README.md` содержит корректные ссылки на эти screenshot/evidence/review
  (проверено в RD-04 R0 PASS).

## Reuse mapping (evidence reuse)

| Источник | Переиспользовано для |
| --- | --- |
| `docs/workflow/evidence/RD-01-evidence.md`; `docs/workflow/reviews/RD-01-review.md` (R1 PASS) | RF-6 browser totals 131250/105525/145950; responsive 1050×740/860×620/390×844; RF-4 rd-01 screenshots |
| `docs/workflow/evidence/RD-02-evidence.md`; `docs/workflow/reviews/RD-02-review.md` (R2 PASS) | RF-5 title/geometry; RF-7 splash lifecycle, no-network, reduced motion; RF-4 rd-02 screenshots |
| `docs/workflow/evidence/RD-03-evidence.md`; `docs/workflow/reviews/RD-03-review.md` (C1 FAIL RD03-F01 → C2 PASS, CLOSED) | RF-3 artifact hash; RF-5 RU shortcut/title; RF-6 installed-runtime totals; RF-8 RU install/reinstall/uninstall + user-file preservation; RF-4 rd-03 screenshots |
| `docs/workflow/evidence/RD-04-evidence.md`; `docs/workflow/reviews/RD-04-review.md` (R0 PASS) | README product/installer claims, screenshot/evidence links, no unsupported signing/publication claims |

Повторно выполненные проверки: только полный suite (один раз) и read-only
artifact/file/hash/diff проверки. Browser, installer install/reinstall/uninstall,
splash runtime, PyInstaller/Inno build не повторялись — RD-01..RD-03 evidence
полные и однозначные, per review-policy.

## NOT_RUN

- Browser verification (desktop/mobile), splash runtime и desktop window
  launch — NOT_RUN; reuse RD-01/RD-02/RD-03.
- Installer install/reinstall/uninstall и setup-error dialog — NOT_RUN; reuse
  RD-03.
- PyInstaller/Inno rebuild, повторная проверка packaged exe — NOT_RUN; артефакт
  не пересобирался, size/SHA256 сверены с README/RD-03.
- Signing, push, merge, deploy, release — NOT_RUN (вне разрешения).
- Отдельный `GET /`/API smoke в этой проверке не запускался; неизменность API
  подтверждена пустым diff и suite, поведение — RD-01/RD-03 evidence.

## Discrepancies / observations

1. **HEAD изменился во время проверки**: dispatch назначал `c72979a`, но
   координатор сделал коммит `8c87e44` (только `HISTORY.md`/`STATE.md`,
   +15/−6) до/во время сбора evidence. Продуктовое дерево идентично
   (`git diff c72979a..HEAD -- app frontend installer packaging tests assets`
   пуст по продуктовым файлам; подробный name-status — в `RD-FINAL-git.txt`).
   Suite и все проверки относятся к `8c87e44`; для продуктового состояния
   `c72979a` результат тот же.
2. Лог suite первоначально записан PowerShell в UTF-16LE и перекодирован в
   UTF-8 без повторного прогона; содержимое не изменено.
3. Mojibake в некоторых исторических RD-01/RD-03 логах (кодировка терминала)
   уже отмечен в ревью как NIT; на текущую проверку не влияет и новых evidence
   не подменяет.
4. Иных расхождений artifact/screenshot/hash/scope не обнаружено.

## Raw logs

- `docs/workflow/evidence/logs/RD-FINAL-git.txt` — branch/HEAD/status/log/
  diff-stat/name-status/c72979a..HEAD/untracked/tracked count.
- `docs/workflow/evidence/logs/RD-FINAL-suite.txt` — единственный прогон suite.
- `docs/workflow/evidence/logs/RD-FINAL-artifact.txt` — artifact path/size/SHA256.
- `docs/workflow/evidence/logs/RD-FINAL-files.txt` — screenshots/evidence/log
  existence и размеры.
- `docs/workflow/evidence/logs/RD-FINAL-rf9-rf10.txt` — calculation/API diff,
  untracked files, added binaries, secret scan.
- `docs/workflow/evidence/logs/RD-FINAL-spotcheck.txt` — branding/geometry
  константы, installer shortcut/config, git-ignore artifact, off-limits listeners.

## Итог проверяющего

Наблюдаемые результаты RF-1..RF-10 соответствуют ожидаемым; блокирующих
расхождений в продуктовом состоянии не обнаружено. Проектный/этапный PASS не
заявляется: вердикт и финальная приёмка остаются за координатором и Codex.
