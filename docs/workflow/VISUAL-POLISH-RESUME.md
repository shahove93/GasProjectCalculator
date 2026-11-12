# Возобновление визуального этапа 1.2.0 после provider limit

> Новейшее решение пользователя: см. `VISUAL-POLISH-LEAN-FINISH.md`.
> После второго BLOCKED evidence почти завершён. Не запускать старый план
> целиком: пять снимков/команды — OpenCode, review и финальная приёмка — Sol/high.

Пользователь 2026-11-12: «Бро, лимиты восстановлены. Можно продолжить работу».
Это явное разрешение продолжить зависимую цепочку после остановки, записано
в APPROVALS.md. Не нужен повторный вопрос о старте или смена модели.

Ты OpenCode/DeepSeek Flash coordinator, не исполнитель продуктового кода.
Возобновляется **тот же** Orca task `task_d75e7fdcd753` в run
`run_8e5d92ad57c7`, прежний coordinator dispatch `ctx_3cdcedf304e0`
завершён failed по реальному provider limit, terminal released, exit proven.
Root запускает retry того же task, без сброса project counters.

## Доказанное состояние

- Ветка feature/gsv-mixed-diameters, HEAD
  `1689773718c818a4ebca400afc2d8a4206b6458e`: VP-01/MD-02 A2/C1 принят
  независимым Sol/high vision review, panels/splash уже готовы. Не переделывать
  и не повторять доказанные проверки без причины по review-policy.
- VP-02 / logical MD-03 / A2 / C1 не закончен из-за usage limit. Сохрани
  исходные counters; это не product FAIL и не новый визуальный подход.
- Старый VP-02 worker `ctx_113e19d0197a` / `task_ef0683db9d81`: stop/fence,
  liveness exited доказан worker-show; root исполнил его next release,
  receipt state=released, archive transcript captured, processAction=none.
- Root worker-list --include-remote по этому run не увидел live/in_progress
  workers перед retry. Повторно сверить ownership перед child dispatch.
- Состояние/история/blocked evidence/task:
  STATE.md, HISTORY.md, evidence/VP-02-blocked.md, tasks/VP-02.md.
- Сохранены uncommitted installer/GasProjectCalculator.iss,
  installer/build-installer.ps1, installer/assets/**, VP-02 evidence/screenshots
  и изменённые workflow docs. Никаких clean/reset/stash/checkout или потери
  чужих изменений.
- Готовый artifact installer/Output/GasProjectCalculator-Setup-1.2.0.exe:
  15 373 267 B, SHA256
  4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113.
  Сохранить до любых rebuild; не пересобирать без изменения/недостаточности
  доказательств, старые installers1.0.0/1.1.0/legacy сохраняются.
- Уже выполнены build, wizard screenshots, часть installed app/lifecycle/API
  проверок; exact logs/artifacts перечислены в VP-02-blocked. Обычная user
  установка/HKCU/ярлыки/106 files восстановлены, user процессы/серверы сохранены.

## Действие координатора

1. Реконструировать checklist/counters и evidence, записать пользовательское
   возобновление в STATE/history, IDs и resource ownership. Не обнулять истории
   или прежний расход, не создавать второй writer.
2. По поддерживаемому recovery protocol возобновить **тот же VP-02 task**
   task_ef0683db9d81 (retry-of старого stopped dispatch при допустимости runtime).
   Если spec дополнить нельзя, составить контекст восстановления в evidence
   VP-02-resume.md и обновить tasks/VP-02.md до dispatch; старый task уже требует
   чтение этих документов. Не выдавать новый task за новый logical budget.
3. Единственный исполнитель продуктового визуального scope и исправлений —
   настоящий Orca Codex **gpt-6-astra/high**, requested/effective подтвердить
   receipt/worker-show ДО работы. DeepSeek не пишет продуктовый код. Никакой
   смены модели/account/config. При реальном новом limit опять BLOCKED.
4. Доделать только недостающее: installed app все три режима/mixed-эталоны,
   lifecycle/reinstall/uninstall/сохранение данных, evidence pack, независимый
   R2 Sol/high review actual diff/artifacts, затем scoped commit по PASS.
5. OpenCode executes integrated full suite один раз на конечной product
   ревизии, отдельный финальный Sol/high reviewer, финальные README/report/
   STATE и передача root local installer/hash/screenshots. Не подменять final
   acceptance самоличным заключением coordinator/implementer.
6. Не трогать user установку/сессию/чужие процессы, .venv, :8000/:8138;
   изоляция install/HKCU/shortcut обязательна. Push/merge/deploy/releases нет.

Перед Orca читать installed guide/help; следовать receipt.next. После dispatch
конец хода, Orca wake; без polling. Root не является терминальным sender,
поэтому не использовать его отсутствие ORCA_TERMINAL_HANDLE как повод
имитировать сообщения или подставлять чужой handle. Работать со своим
реальным Dispatch preamble и законным child workflow. Вернуть настоящий
worker_done с конечным PASS/COMPLETE или точным blocker/evidence.
