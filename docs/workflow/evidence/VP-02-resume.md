# VP-02 (logical MD-03 / A2) — возобновление после provider limit

Дата: 2026-11-12. Статус: **RESUMED / IN_PROGRESS** (не product PASS).
Логический TASK: **MD-03 A2**, продолжение прежнего подхода; счётчики не
сбрасываются. Координатор: OpenCode/DeepSeek Flash.

## Authority

- `docs/workflow/VISUAL-POLISH-ASTRA-BRIEF.md` (уточнённый scope 1.2.0).
- `docs/workflow/APPROVALS.md`, раздел «Явное возобновление после Codex usage
  limit — 2026-11-12»: пользователь написал «Бро, лимиты восстановлены. Можно
  продолжить работу». Это разрешение продолжить зависимую цепочку, не сброс
  бюджета и не смена модели.
- `docs/workflow/VISUAL-POLISH-RESUME.md`.
- `docs/workflow/tasks/VP-02.md` (обновлён этим возобновлением).

## Ownership и Run

- Run `run_8e5d92ad57c7`; текущий coordinator Dispatch
  `ctx_ed7166e32fdc` / task `task_d75e7fdcd753`, terminal
  `term_f61ee838-7bfb-44e4-a660-994e91dc82e4` — единственный live writer,
  проверено `orca orchestration worker-list --json` перед dispatch.
- Прежний VP-02 worker `ctx_113e19d0197a` / task `task_ef0683db9d81`
  (`term_574e5c74-8643-4b6b-a0c3-5200e66cfc1d`) остановлен/fenced,
  `worker-show`: `state=stopped`, `liveness=exited`, terminal `released`.
  Его task сейчас `blocked`; это восстанавливаемая зависимая работа, не
  product FAIL.
- Прежний coordinator Dispatch `ctx_3cdcedf304e0` завершён failed по тому же
  provider limit, terminal released. Root выполнил retry того же coordinator
  task; это не новый logical budget.
- Второго писателя нет. `checkout/clean/reset/stash` не выполнялись и не
  выполняются.

## Workspace / baseline

- CWD: `D:/Antigravity/GasProjectCalculator`.
- Branch: `feature/gsv-mixed-diameters`.
- HEAD: `1689773718c818a4ebca400afc2d8a4206b6458e` (VP-01 / MD-02 A2 PASS,
  local scoped commit).
- Исходный baseline этапа `ac59d8c27ed47be07ac9b54acf8285bcab704be0`
  сохранён в истории; VP-01 уже принят и закоммичен.

## Сохранённое незакоммиченное состояние VP-02

Не сбрасывать, не перезаписывать без причины и не коммитить до routed PASS:

- `installer/GasProjectCalculator.iss` — branding/version 1.2.0.
- `installer/build-installer.ps1` — необходимые изменения сборки.
- `installer/assets/**` — `wizard-sidebar.bmp`, `wizard-header.bmp`,
  `export-artwork.ps1`.
- `installer/Output/GasProjectCalculator-Setup-1.2.0.exe` (git-ignored).
- `docs/screenshots/visual-02-*` — 9 реальных wizard/native screenshots.
- `docs/workflow/evidence/logs/VP-02-*` — build/wizard/install/API/restore
  логи и скрипты.
- `docs/workflow/evidence/VP-02-blocked.md`, этот файл, resume/brief/STATE
  правки координатора.
- `C:/Users/user/AppData/Local/Temp/opencode/vp-02-isolated/` — изолированная
  установка, backup пользовательского HKCU/ярлыков, первая сборка
  `first-build-1.2.0.exe`.

## Факты об артефакте (перепроверено сейчас)

- `installer/Output/GasProjectCalculator-Setup-1.2.0.exe`
  - 15 373 267 B, SHA256
    `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113`
  - FileVersion `1.2.0.0`, ProductVersion `1.2.0`.
- Прежние installer bytes сейчас совпадают с зафиксированными до build:
  - 1.0.0: 15 286 980 B `71232EE4…7E08`;
  - 1.1.0: 15 293 993 B `3BFFFFB2…B710`;
  - legacy pre-compact: `04388410…949A`;
  - legacy previous-stage: `2973278F…428F`.
- Installer 1.2.0 пересобирать без необходимости не нужно; существующий
  артефакт каноничен для этой ревизии. Если worker обнаружит недостаточность
  evidence и пересоберёт — обязан сохранить прежние bytes и заново записать
  hash/version.

## Пользовательская среда (сохранена)

- Пользовательская установка `%LOCALAPPDATA%\Programs\GasProjectCalculator`:
  106 файлов, 37 372 847 B; HKCU uninstall key `DisplayVersion=1.0.0`,
  `InstallLocation` пользовательский; Start Menu и Desktop ярлыки указывают на
  пользовательский `GasProjectCalculator.exe`.
- Пользовательский процесс `GasProjectCalculator` PID 13248 работает.
- `:8000` PID 12888 и `:8138` PID 23152 сохранены.
- Изолированная установка находится только в
  `Temp/opencode/vp-02-isolated/install` (113 files), изолированных процессов
  не осталось.
- Все эти объекты нельзя изменять как постоянное состояние; изоляция
  install/upgrade/uninstall обязательна.

## Восстановленные counters (не сбрасывать)

| Logical TASK | Прежние подходы | Full reviews | FAIL | Codex calls | Текущий шаг |
| --- | --- | ---: | ---: | ---: | --- |
| MD-02 visual | A1/C1 PASS формально, A2/C1 PASS после новых refs | 2 | 0 | 2/4 | завершён VP-01 |
| MD-03 installer | A1/C1 PASS, A2/C1 возобновлён | 1 + текущий незавершённый | 0 | 1/4 до текущего цикла; резерв 2-й call | VP-02 |
| FINAL-MIXED-STAGE | A1/C1 stage PASS | 1 stage acceptance | 0 | 1 | новая отдельная приёмка этапа |

- Текущий VP-02 A2/C1 — тот же первый полный review этого подхода: его
  прервал provider limit, а не verdict. Повторный запуск после восстановления
  доступа не добавляет второй цикл.
- Резерв на этот подход: один полный R2 review Codex `gpt-6.1-sol` high
  (call 2/4). Отдельная финальная stage-приёмка Codex `gpt-6-astra` high
  выполняется в независимом контексте, не исполнителем.
- Полный integrated suite исполняет координатор один раз по конечной
  продуктовой ревизии.

## Замороженный checklist

Чек-лист **VP-02.md W1–W11** не меняется; уточнение — только наблюдаемые
критерии уже принятого scope:

- W1: packaged app и installer 1.2.0 из принятого VP-01, exit 0,
  path/size/SHA256.
- W2: FileVersion/ProductVersion 1.2.0, AppId сохранён, имя артефакта 1.2.0.
- W3: 1.0.0/1.1.0/legacy bytes и опубликованные releases не изменены.
- W4: реальный RU wizard welcome/dir/tasks/installing/finish, фирменная
  графика, читаемые кнопки.
- W5: изолированная установка; пользовательские install/HKCU/ярлыки
  восстановлены; чужие files сохранены.
- W6: установленное приложение без Python/CLI; splash/readiness и новое
  основное окно.
- W7: mixed-эталоны 75600/79275/71400/63000/70875, combined 151000/7550/
  158550, legacy/422, ГСН-регрессия, САКЗ/ПК/район/НДС 5% — в установленной
  версии.
- W8: loopback-only, занятый test-порт, закрытие завершает backend, без
  дочерних процессов.
- W9: install/upgrade/reinstall/uninstall сохраняет user files; RU-only;
  без network/signing.
- W10: diff строго в allowlist; backend/API/calculator/frontend zero-diff;
  targeted packaging/installer/presentation tests зелёные.
- W11: артефакт передан локально path/size/SHA256; push/merge/deploy/release
  отсутствуют.

Дополнительно для стадии: side-by-side header/footer/splash с refs и
установщик в том же стиле уже приняты в VP-01; installer visual coherence
оценивается фактическими wizard screenshots, а не текстовым заявлением.

## Что осталось сделать (только недостающее)

1. Дозавершить installed-app проверки по W6–W9: все три режима, mixed/
   combined/legacy/422/ГСН, САКЗ/ПК/район/НДС, native screenshots/размеры,
   lifecycle/закрытие/loopback/занятый порт, isolated reinstall/uninstall и
   сохранение пользовательских файлов.
2. Дополнить evidence pack `docs/workflow/evidence/VP-02-evidence.md`
   реальными командами/CWD/exit/logs/screenshots/NOT_RUN.
3. Передать пакет независимому R2 Codex `gpt-6.1-sol` high; не выставлять
   PASS самостоятельно, не коммитить.
4. После R2 PASS координатор: full suite один раз, отдельный final
   Astra/high reviewer, FINAL-REPORT/README/STATE, local scoped commit.
   Push/merge/deploy/release не выполнять.

## Dispatch protocol (выполнено)

### Runtime note: почему новый Run/Task-контейнер, а не reopen старого

Попытки строго возобновить прежний Orca task `task_ef0683db9d81` в
`run_8e5d92ad57c7` отклонены самим Orca runtime:

- `worker-start --task task_ef0683db9d81 --retry-of ctx_113e19d0197a` →
  `task_not_found`: задача не была последней запущена helper-ом текущего
  coordinator dispatch;
- `task-update --id task_ef0683db9d81 --status ready --run run_8e5d92ad57c7` →
  `worker_cannot_coordinate_own_run`: текущий dispatch работает в этом Run и не
  может его координировать; `run-current` = `null`.

Это ограничение контейнера координации, **не** reset logical TASK, не новый
подход, не обнуление counters и не смена бюджета. Поэтому та же работа
возобновлена в дочернем Run с полным self-contained resume-spec, а прежние
task/dispatch/blocked evidence сохранены в истории.

### Фактический dispatch

- Parent coordinator: `ctx_ed7166e32fdc` / `task_d75e7fdcd753`
  (Run `run_8e5d92ad57c7`), terminal
  `term_f61ee838-7bfb-44e4-a660-994e91dc82e4`.
- Новый Run контейнера: `run_51b48d1d96cc`.
- Новый task: `task_150bb380db2c` (title «VP-02 resume installer 1.2.0
  isolated verify (MD-03 A2)»), spec:
  `docs/workflow/evidence/VP-02-resume-spec.md`.
- Worker dispatch: `ctx_988a8c02d5c3`, terminal
  `term_879889ea-ac9e-48ad-bc89-978a67a20e10`, workspace
  `bcec44b9-39b7-4f68-9903-85dad7eaaa26::D:/Antigravity/GasProjectCalculator`.
- Launch receipt: `docs/workflow/evidence/logs/VP-02-resume-receipt.json`.
- Effective worker-show: `docs/workflow/evidence/logs/VP-02-resume-effective.json`.
- **Проверено requested/effective:** `agent=codex`, `model=gpt-6-astra`,
  `effort=high` — совпадают; state `ready`, liveness `live`. Молчаливой
  замены нет.
- После dispatch координатор заканчивает ход и ждёт Orca wake; без
  polling/watch.

## Явно НЕ выполнялось

- Никаких reset-credit, покупки кредитов, смены аккаунта/тарифа, обхода
  provider limit, молчаливой замены модели.
- Никаких `checkout/clean/reset/stash`, потери чужих/незакоммиченных
  изменений, изменений пользовательской установки, HKCU/ярлыков, `.venv`,
  `:8000`, `:8138`.
- Никаких commit/push/merge/deploy/release/signing.
