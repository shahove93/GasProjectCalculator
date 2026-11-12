# TASK: VP-02 resume (logical MD-03 A2) — дозавершить installer 1.2.0 evidence

## Роль и модель

Ты — **исполнитель VP-02**, настоящий Orca **Codex** worker с моделью
**`gpt-6-astra`**, reasoning effort **`high`**. Это явное ограниченное
исключение пользователя для визуального scope 1.2.0; не заменяй модель, не
меняй глобальные model/account config. Координатор уже проверил
requested/effective launch перед выдачей этой работы.

Работа — продолжение прежнего logical TASK **MD-03 A2** (Orca task
`task_ef0683db9d81`, dispatch `ctx_113e19d0197a`), прерванного реальным provider
usage limit, а не FAIL-вердиктом. Счётчики/история/артефакты не сбрасываются.
Новый Orca Run/Task — только техническое пересоздание контейнера координации;
logical TASK и бюджет сохраняются.

## Обязательное чтение ДО любых изменений

1. `AGENTS.md`
2. `docs/workflow/VISUAL-POLISH-ASTRA-BRIEF.md`
3. `docs/workflow/VISUAL-POLISH-RESUME.md`
4. `docs/workflow/evidence/VP-02-resume.md` (текущее доказанное состояние)
5. `docs/workflow/tasks/VP-02.md` (Resume-раздел + W1–W11)
6. `docs/workflow/APPROVALS.md`, `docs/workflow/STATE.md`,
   `docs/workflow/HISTORY.md`, `docs/workflow/MODEL-ROUTING.md`
7. `C:/Users/user/.agents/skills/autonomous-development/references/review-policy.md`
   и `routing-and-budget.md`

## Workspace / baseline / ownership

- CWD: `D:/Antigravity/GasProjectCalculator`.
- Branch: `feature/gsv-mixed-diameters`.
- Baseline/HEAD: `1689773718c818a4ebca400afc2d8a4206b6458e` (VP-01 PASS).
- В рабочем дереве есть незакоммиченные VP-02 installer/assets/evidence и
  документы координатора. **Сохранить их.** Не выполнять
  `checkout/clean/reset/stash`; не коммитить.
- Пользовательская установка `%LOCALAPPDATA%\Programs\GasProjectCalculator`
  (106 файлов), HKCU uninstall key (`DisplayVersion=1.0.0`), Start Menu/Desktop
  ярлыки, процесс PID 13248, серверы `:8000`/`:8138`, `.venv` и чужие процессы
  — **не изменять**. Все install/reinstall/uninstall проверки — только в
  изолированном каталоге `C:/Users/user/AppData/Local/Temp/opencode/vp-02-*`,
  с backup/restore HKCU и ярлыков до/после.
- Второй writer отсутствует. Не создавай helper workers; работай сам.

## Сохранённый артефакт

- `installer/Output/GasProjectCalculator-Setup-1.2.0.exe` уже собран:
  15 373 267 B, SHA256
  `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113`,
  FileVersion `1.2.0.0`, ProductVersion `1.2.0`.
- **Не пересобирай без реальной необходимости.** Если evidence докажет, что
  артефакт не соответствует исходникам, разрешена пересборка при условии:
  сначала записать прежние bytes/hash, после сборки доказать неизменность
  1.0.0/1.1.0/legacy. Результат — новый `GasProjectCalculator-Setup-1.2.0.exe`.
- Прежние installers 1.0.0/1.1.0/legacy сохранять; remote releases не трогать.

## Allowlist

Разрешено менять только:

- `installer/GasProjectCalculator.iss`, `installer/build-installer.ps1`,
  `installer/verify-*.ps1` — только если реально нужно для 1.2.0/branding.
- `installer/assets/**` — локальные BMP/PNG/SVG/exporter, уже созданные.
- `installer/Output/GasProjectCalculator-Setup-1.2.0.exe` — артефакт
  (git-ignored).
- `packaging/**` — только необходимые под новый frontend/asset.
- `scripts/visual-*` — exporter helper при необходимости.
- `tests/test_installer_packaging.py` и существующие presentation/installer
  static tests — только необходимые version/asset assertions; не ослаблять
  функциональные/безопасностные проверки.
- `docs/workflow/evidence/VP-02-*` (включая `VP-02-evidence.md`),
  `docs/workflow/evidence/logs/VP-02-*`, `docs/screenshots/visual-02-*`.
- Временные каталоги `C:/Users/user/AppData/Local/Temp/opencode/vp-02-*`.

Запрещено: `app/` (backend/lifecycle), `frontend/` (принят VP-01),
`requirements*`, VISION/ARCHITECTURE/ROADMAP/workflow docs кроме evidence,
пользовательская установка/HKCU/ярлыки как постоянные изменения,
signing/network, push/merge/deploy/release, глобальные конфиги, чужие
процессы/сессии, commit.

## Уже выполнено (не повторять без причины)

- Installer 1.2.0 собран и проверен по metadata/hash; прежние bytes неизменны.
- RU wizard screenshots: welcome, dir, tasks, installing, finish, ready.
- Native screenshots: splash, normal launch, target GSN; isolated install,
  HKCU/shortcut backup, restore и сохранение 106 user files.
- Part of API/calculator checks (`VP-02-api-*`); targeted desktop tests и
  packaging build logs.

## Доделать (недостающее)

1. **Installed-app проверки по W6–W9**: установленное приложение из
   изолированного install без Python/CLI; splash/readiness; новое основное
   окно; все три режима (ГСН, ГСВ, общая смета); mixed-эталоны
   `4/0/4→75600`, `2/4/3→79275`, `0/5/2→71400`, `3/1/1→63000`, `8/0/0→70875`;
   combined `151000/7550/158550`; legacy/422; ГСН-регрессия; САКЗ/ПК (ПК только
   с САКЗ)/район 7000/НДС 5%.
2. **Native/browser screenshots**: target 800×540 и min 760×520, `scrollY=0`,
   action/total доступны; реальные PNG, не макеты.
3. **Lifecycle**: loopback-only; занятый test-порт ≠8000/8138; закрытие окна
   завершает backend без дочерних процессов; splash readiness/error path;
   reduced motion не ломает статичный вид.
4. **Изолированный install/upgrade/reinstall/uninstall**: сохранение user
   files, HKCU/ярлыки восстановлены; RU-only; без network/signing; прежняя
   установка не затронута.
5. **Evidence pack** `docs/workflow/evidence/VP-02-evidence.md`: exact
   command/CWD/exit/log/artifact для каждой проверки, baseline/diff, scope,
   pre/post hashes, screenshots/размеры, значения, NOT_RUN явно.
6. Targeted tests (packaging/installer/presentation) с exact exit; полный
   integrated suite не запускать — его выполнит координатор по конечной
   ревизии.

## Замороженный checklist (W1–W11)

- W1: packaged app и installer 1.2.0 из VP-01, exit 0, path/size/SHA256.
- W2: metadata 1.2.0/1.2.0.0, AppId сохранён, имя артефакта 1.2.0.
- W3: 1.0.0/1.1.0/legacy bytes и опубликованные releases не изменены.
- W4: реальный RU wizard welcome/dir/tasks/installing/finish, фирменная
  графика, читаемые кнопки.
- W5: изолированная установка; user install/HKCU/ярлыки восстановлены; чужие
  files сохранены.
- W6: installed app без Python/CLI; splash/readiness и новое окно.
- W7: mixed/combined/legacy/422/ГСН/САКЗ/ПК/район/НДС в installed версии.
- W8: loopback-only, занятый test-порт, закрытие завершает backend, без детей.
- W9: install/upgrade/reinstall/uninstall сохраняет user files; RU-only; no
  network/signing.
- W10: diff строго в allowlist; backend/API/calculator/frontend zero-diff;
  targeted tests зелёные.
- W11: local artifact path/size/SHA256; push/merge/deploy/release отсутствуют.

## Ограничения выполнения

- Свои процессы — только на свободных портах ≠8000/8138; после проверок
  остановить только свои процессы.
- Не имитировать скриншоты/review/completion; реальные browser/native checks.
- При реальном provider limit/недоступности Astra — остановить зависимую
  цепочку, записать точную ошибку, вернуть BLOCKED; не менять модель молча,
  не покупать кредиты, не reset-credit, не менять аккаунт.
- Не выставлять project PASS и не коммитить; commit делает координатор после
  независимого routed PASS.

## Reporting (worker_done)

Верни: изменённые файлы/diff scope; artifact exact path/size/SHA256 и
FileVersion/ProductVersion; unchanged legacy hashes; install/restore evidence;
native/browser screenshots и размеры; значения/requests; lifecycle; wizard
flow; targeted tests command/CWD/exit; requested/effective model; Task/Dispatch
IDs; риски/NOT_RUN. Не объявлять PASS и не коммитить.
