# Экономно завершить 1.2.0 — приоритетный brief 2026-11-12

> Root launch22:30 МСК остановлен `no_active_sender_terminal`, новых workers
> не создано. См. `evidence/VP-02-lean-launch-blocked.md`. Законный resume —
> тот же task из настоящего Orca terminal, без подстановки чужого sender.

Роль: OpenCode/DeepSeek Flash coordinator. Пользователь разрешил закончить
после второго limit и потребовал снизить расход. Ранее явно выбрал **Sol**
для финальной приёмки. APPROVALS/AGENTS/MODEL-ROUTING обновлены root.
Не исполняй старый первоначальный план заново.

## Осталось только это

1. **OpenCode** доснимает пять settled кадров D1–D5, не меняя продуктовый код.
   Все прочие W1–W11 evidence уже собраны в `evidence/VP-02-evidence.md`.
2. Независимый bounded R2 **Codex gpt-6.1-sol/high** review VP-02.
3. OpenCode выполняет full integrated suite ОДИН раз по конечному состоянию,
   если такого доказанного прогона ещё нет; результаты не дублируются.
4. Отдельная финальная stage acceptance **Codex gpt-6.1-sol/high**;
   затем FINAL-REPORT/README/STATE и local scoped commit, local artifact/root.

Astra для evidence/тестовых команд/финального review НЕ запускать.
При необходимости настоящей продуктовой визуальной правки остаётся только
Astra/high по ограниченному исключению пользователя. OpenCode может исправлять
evidence scripts/запуск server/screenshots, не SVG/CSS/продуктовый код.

## Состояние для восстановления, без повторного исследования всего проекта

- Workspace D:/Antigravity/GasProjectCalculator; feature/gsv-mixed-diameters.
- HEAD `1689773718c818a4ebca400afc2d8a4206b6458e`: VP-01 PASS (MD-02 A2),
  независимый Sol/high уже принял header/footer/splash, MD02-N1 CLOSED.
  Не открывать это review заново, если product diff не затронул эти файлы.
- VP-02 = logical MD-03/A2/C1, counters/история сохраняются: A1 один полный
  review/0FAIL, A2 ещё без verdict; резерв нового review call2/4. Оба provider
  limit прерывали работу, не были product FAIL. Не скрывать расход этих dispatch.
- Coordinator task `task_d75e7fdcd753`, run `run_8e5d92ad57c7`; предыдущий
  dispatch `ctx_ed7166e32fdc` failed worker_report, exited/released.
- Child run `run_51b48d1d96cc`, task `task_150bb380db2c`, предыдущий worker
  `ctx_988a8c02d5c3` stopped/exited/released. Root подтвердил оба worker-show
  и child worker-list в 22:28–22:29 МСК 2026-11-12. Живых writers там нет.
  Не пытаться восстанавливать закрытые terminal handles.
- Сохрани все dirty installer/assets/docs/evidence/screenshots и user files.
- Artifact уже готов: installer/Output/GasProjectCalculator-Setup-1.2.0.exe,
  15 373 267B, SHA256
  4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113.
  Не rebuild без изменения product source/неустранимого пробела доказательств.
- Последний block: `evidence/VP-02-blocked-resume.md`, только gap five shots
  во время fadeUp. Последний reported reset21:31 прошёл по wall clock, но
  доступность провайдера не предполагать; при реальном отказе вновь BLOCKED.

## Как закрыть пять кадров без нового дорогого агента

Готовый script `evidence/logs/VP-02-resumed-settled-shots.cjs` уже ждёт
document.getAnimations().finished и проверяет opacity=1, ожидаемые итоги
75600/79275/71400/63000/70875; сохраняет новые *-settled.png без перезаписи
прежних кадров. Последняя ошибка не продукта: `ERR_UNSAFE_PORT` из-за port0.
Script читает `Temp/opencode/vp-02-resume/settled-port.json`; нужен реальный
неравный нулю порт из readiness launcher. Исправлять только evidence script/
test launch, не продуктовый код. Выбери browser-safe свободный порт 18081
(предварительно проверь) или другой >1024, не запрещённый браузером; не порт0.
Собственный управляемый server/launcher, готовность отдельным запросом;
никаких висящих shell tools с background Start-Process. Изолированный
installed payload может остаться после прежних проверок; сверь manifest.
Не устанавливай приложение заново ради браузерных кадров. Если запускаешь
готовый exe, никаких постоянных изменений user HKCU/ярлыков не требуется.
Собственные процессы закрыть, user :8000/:8138 и другие процессы сохранить.

## Строгая экономия без снижения качества

- Только один coordinator и текущий необходимый worker. Ни polling/watch,
  ни Codex для статуса/ожидания. После dispatch конец хода, ждать Orca wake.
- Не отправлять reviewers весь репозиторий/HISTORY/транскрипт. Bounded packet:
  frozen W1–W11, baseline1689773, actual installer diff + новые assets,
  VP-02-evidence и соответствующие logs/screenshots, прошлый MD-03 verdict.
  Проверять первоисточники, но не перечитывать 48 картинок без основания:
  full manifest, ключевые wizard/native/settled shots по каждому критерию.
- VP-01 уже принят. Final reviewer использует его verdict и relevant diff,
  не повторяет его visual audit автоматически. Отдельное решение stage
  остаётся обязательным; оно не заменяет VP-02 R2 acceptance.
- Не повторять build/install/uninstall/API/static/targeted checks, уже доказанные
  для неизменного source/artifact. Review-policy разрешает повтор лишь при
  конкретном пробеле или изменении; точный reason записать.
- Не создавать новые helpers/тесты/документы ради формальности. Корректируй
  существующий evidence pack ссылкой на five settled shots и exact command/
  CWD/exit. Full suite once, scoped diff, concise report.
- Перед каждым reviewer launch проверить model gpt-6.1-sol/high реально,
  после completion сразу сохранить verdict и закончить его worker.
  Никаких отдельных вызовов дорогой модели для пересказа verdict.
- Actual расход записывать если доступен; неизвестные токены не выдумывать.
  Hard input-token caps не вводить. Не reset counters и не обходить limits.

## Ownership, authority, completion

Сначала минимально: AGENTS, этот brief, STATE, APPROVALS (последнее решение),
VP-02 frozen checklist, существующий evidence pack/последний blocked report;
профильные skills/references как требуется. Старый HISTORY читать только по
нужным ссылкам для counters, не весь архив. Coordinator обновляет STATE/history
и ведёт task ownership. Переиспользуй поддерживаемый runtime recovery того же
Task, не создавай новый logical budget. Не координируй собственный bound Run
как child: прежний контейнерный отказ задокументирован в HISTORY; при
необходимости child Run используй точный установленный guide.

Нет commit до routed PASS; после scoped commit разрешён. Push/merge/deploy/
release/signing не разрешены. Старые artifacts1.0.0/1.1.0/legacy, .venv,
обычная установка/HKCU/ярлыки/сессии сохраняются. Не трогать глобальные configs.
При реальном новом provider limit — стоп без автоматических retry/fallback.
В worker_done: два независимых verdict, suite, artifact/hash, точные пути
preview/screenshots, local revision, ограничения и реальные IDs/model/cost.
COMPLETE только при закрытых критериях и финальном PASS.
