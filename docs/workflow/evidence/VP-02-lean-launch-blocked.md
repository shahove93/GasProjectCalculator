# Экономное завершение: модель уточнена, launch BLOCKED инфраструктурой

2026-11-12, около22:30 МСК. Root выполнил только read-only recovery и
обновление инструкций/approval по новым сообщениям пользователя. Продуктовый
код, installer bytes и прежние review/counters не менялись.

## Что исправлено в маршруте

Решение пользователя «Давай да, поручим Sol» перенесено в AGENTS,
MODEL-ROUTING и текущие briefs: independent R2 и final stage — разные
Codex gpt-6.1-sol/high reviewers. Astra остаётся только для продуктовых
визуальных правок. Screenshots, evidence scripts, тестовые команды, logs и
docs — OpenCode. Подробный минимальный остаток в VISUAL-POLISH-LEAN-FINISH.md.

Из истории установлен факт: последний Astra resume не менял продуктовый код,
а занимался extensive evidence. Exact token/cost totals не получены и не
утверждаются. Повторные дорогие вызовы ради этого evidence запрещены новым
brief; функциональные критерии W1–W11 не ослаблены.

## Read-only ownership preflight

CLI: C:/Users/user/AppData/Local/Programs/orca/resources/bin/orca.exe.
Installed orchestration guide и recovery/help прочитаны.
`worker-show --dispatch ctx_ed7166e32fdc --json --full`: failed/settled,
liveness exited/resource_release, released.
`worker-show --dispatch ctx_988a8c02d5c3 --json --full`: stopped, exited,
released. Child worker-list run_51b48d1d96cc содержит только этот stopped
worker. Worker-list run_8e5d92ad57c7 не выявил live/in_progress workers.

Первоначальный read-only CLI получил runtime_access_denied/EPERM из sandbox;
повтор с одобренным require_escalated успешно прочитал состояние. Orca не
перезапускалась, orca open не вызывался.

## Точная причина невозможности launch

Авторизованный require_escalated вызов из cwd D:/Antigravity/GasProjectCalculator:

```text
orca orchestration worker-start --task task_d75e7fdcd753 --retry-of ctx_ed7166e32fdc --run run_8e5d92ad57c7 --worktree current --agent opencode --json
```

Exit1, runtime error:

```text
no_active_sender_terminal
Codex ran this orchestration command without ORCA_TERMINAL_HANDLE.
Pass --from only with your own terminal's handle — another pane's handle
would act on its mailbox.
```

Нового Dispatch/Task/терминала receipt не создал. Не делались подстановка
чужого --from/ORCA_TERMINAL_HANDLE, смена глобального config, повторный launch,
неподдерживаемый fallback или обход sandbox/provider limit. Это runtime identity
blocker, не отказ auto-review и не product FAIL. Новых тестов/review нет.

Следующий законный шаг: выполнить тот же worker-start в настоящем терминале
Orca с собственным runtime-issued ORCA_TERMINAL_HANDLE либо восстановить
официальную интеграцию чата. Восстановление среды не обнуляет logical MD-03/A2/C1.
После запуска coordinator обязан первым читать актуальный lean brief; старый
task spec ссылается на VISUAL-POLISH-ASTRA-BRIEF.md, где этот приоритет закреплён.
Нужны только five settled shots → Sol R2 → full suite once → Sol final →
report/local commit/local artifact. Повтор старой очереди запрещён.
