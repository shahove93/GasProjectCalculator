# VP-02 (logical MD-03 / A2 / C1) — BLOCKED: Codex provider usage limit

Дата: 2026-11-12. Статус: **BLOCKED**, не product PASS.
Координатор: OpenCode/DeepSeek Flash. Исполнитель VP-02: настоящий Orca Codex
`gpt-6-astra`, effort `high` (`ctx_113e19d0197a` / `task_ef0683db9d81`,
terminal `term_574e5c74-8643-4b6b-a0c3-5200e66cfc1d`).
Requested и effective модель подтверждены launch receipt/worker-start:
`agent=codex`, `model=gpt-6-astra`, `effort=high`.

## Точная причина остановки

В ходе проверки установленной программы worker получил реальный отказ
Codex по usage limit:

```text
You've hit your usage limit. Upgrade to Pro ... or try again at 4:28 PM.
Approaching rate limits
Switch to gpt-6-luna for lower credit usage?
```

Последнее наблюдённое состояние 5h limit: `8% left`, `resets at 16:28`
(локальное время, 2026-11-12). Это фактический provider limit, не ошибка
продукта. Согласно правилу задания и `routing-and-budget.md`:

- зависимая цепочка остановлена;
- **не** выполнялись reset-credit, покупка кредитов, переключение
  аккаунта/тарифа, пересоздание сессии ради обхода;
- **не** выполнялась молчаливая замена модели; предложенный `gpt-6-luna`
  отклонён, поскольку визуальный scope по решению пользователя закреплён
  только за `gpt-6-astra`/high;
- автоматическое продолжение после сброса не запускалось; решение за root.

## Что уже сделано к моменту BLOCKED

- VP-01 (MD-02 A2/C1) принят независимым R2 Codex `gpt-6.1-sol` high **PASS**,
  MD02-N1 закрыт, local commit
  `1689773718c818a4ebca400afc2d8a4206b6458e`.
- VP-02 собрал packaged app и настоящий Inno Setup installer **1.2.0**:
  `installer/Output/GasProjectCalculator-Setup-1.2.0.exe`,
  **15 373 267 B**, SHA256
  `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113`.
- Прежние артефакты не изменены (проверено после build):
  1.0.0 15 286 980 B `71232EE4…7E08`;
  1.1.0 15 293 993 B `3BFFFFB2…B710`;
  legacy `04388410…949A` / `2973278F…428F`.
- Сняты реальные RU wizard screenshots (welcome, dir, tasks, installing,
  finish, ready), native splash/main/GSN screenshots; выполнены isolated
  install, HKCU/shortcut backup, API/calculator checks и часть installed-app
  проверок. Evidence/logs: `docs/workflow/evidence/logs/VP-02-*`,
  `docs/screenshots/visual-02-*`.
- Незавершённый вечер: полная installed-app проверка (ГСН/ГСВ/combined,
  mixed-эталоны, lifecycle/reinstall/uninstall), R2 review, финальный full
  suite, отдельная финальная Astra stage-приёмка, FINAL-REPORT/README/STATE
  и local commit.

## Безопасная очистка и сохранение пользовательской установки

Worker был остановлен/fenced (`worker-stop`, `closed_agent_terminal`).
Изолированная установка использовала отдельный temp-каталог
`C:\Users\user\AppData\Local\Temp\opencode\vp-02-isolated\install`.

Запущен собственный проверочный restore-script worker:

```text
RESTORED: HKCU exact export, shortcut SHA256, all 106 user install files unchanged
```

Проверено после restore:

- HKCU uninstall key восстановлен на
  `DisplayVersion 1.0.0`, `InstallLocation` = пользовательский
  `%LOCALAPPDATA%\Programs\GasProjectCalculator\`;
- Start Menu и Desktop ярлыки указывают на пользовательскую установку;
- все 106 файлов пользовательской установки не изменены;
- исходный пользовательский процесс PID 13248 `GasProjectCalculator`
  продолжает работать;
- `:8000` (PID 12888) и `:8138` (PID 23152) сохранены;
- изолированных процессов `vp-02-isolated` не осталось.
- Температурный isolated-каталог и все VP-02 evidence сохранены для
  возможного возобновления; пользовательские данные не удалялись.

## Состояние рабочего дерева на момент BLOCKED

Baseline/HEAD: `1689773718c818a4ebca400afc2d8a4206b6458e` (VP-01 commit).
Незакоммиченные VP-02 изменения сохранены, **не** сброшены и **не**
закоммичены без routed PASS:

- `installer/GasProjectCalculator.iss` (branding/version 1.2.0),
- `installer/build-installer.ps1`,
- `installer/assets/**`,
- `docs/workflow/tasks/VP-02.md` (baseline note),
- `docs/workflow/evidence/logs/VP-02-*`,
  `docs/screenshots/visual-02-*`,
- `docs/workflow/evidence/VP-02-blocked.md` (этот файл).

## Возобновление

После реального восстановления доступа Codex `gpt-6-astra` (не смена модели,
не обход лимита) root может возобновить logical TASK MD-03/A2 с сохранением
текущих counters, uncommitted состояния, artifact bytes и evidence. Новый
provider limit сам по себе не является product FAIL и не сбрасывает бюджет;
повторная приёмка должна быть отдельным review-циклом.
