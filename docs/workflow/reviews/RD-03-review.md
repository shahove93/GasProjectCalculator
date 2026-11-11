# RD-03 — независимое R2-ревью C1 (Codex): FAIL

- Логический TASK: RD-03, подход A1, цикл C1.
- Ревьюер: отдельный Orca Codex worker `ctx_0f37bf720947`
  (`task_70cf5390b9b4`), model `gpt-6.1-sol`, effort high, terminal
  term_96fdf92a.
- Ревизия: ветка `feature/ss-calculator-redesign`, HEAD `6d91036`,
  продуктовый baseline `32e77b1`, рабочее дерево с uncommitted RD-03.
- Ревьюер файлов не менял, повторных прогонов не было (`rerun=0`); проверены
  фактический diff, исходные логи, 9 native-снимков и локальные бинарники.

## Вердикт: FAIL

Единственный finding:

- **RD03-F01 — MAJOR, OPEN** (R3-2,
  `docs/workflow/tasks/RD-03.md:68`, `RD-03-evidence.md:219`,
  `logs/RD-03-wizard-error.txt`): нет реального скриншота ошибки самого Setup.
  Попытка с `/DIR=C:\Windows\System32\RD03-Forbidden` не наблюдала error-dialog;
  frozen checklist R3-2 требует real screenshots страниц/кнопок/**ошибок**/
  финиша. Компиляция `Russian.isl` и русский uninstaller подтверждают
  настройку языка, но не заменяют обязательное наблюдение setup-error; runtime
  failure относится к другому компоненту (приложение, не мастер установки).

## Матрица C1

| ID | Результат | Evidence |
| --- | --- | --- |
| R3-1 | PASS | build logs: Build complete, Successful compile, exit 0; hash совпал. |
| R3-2 | **FAIL / MAJOR** | wizard welcome/dir/tasks/ready/finish русские; setup-error screenshot — NOT_RUN (RD03-F01). |
| R3-3 | PASS | точные имя/target/WorkingDir ярлыков; runtime title `СС.Расчет`. |
| R3-4 | PASS | clean install desktop False; reinstall desktop True; tasks unchecked. |
| R3-5 | PASS | Inno: User privileges None, Administrative install mode No, HKEY_CURRENT_USER; HKCU True/HKLM False. |
| R3-6 | PASS | PE x64 GUI subsystem 2; PATH-stripped python not found; app starts. |
| R3-7 | PASS | splash → ready → main; installed-app log и снимки. |
| R3-8 | PASS | реальные HTTP 200: 131250/105525/145950. |
| R3-9 | PASS | busy 8123→127.0.0.1:8124, close освобождает; :8000/:8138 сохранены. |
| R3-10 | PASS | reinstall exit 0; marker hashes не изменились. |
| R3-11 | PASS | русский uninstaller; program/shortcuts/HKCU удалены, markers сохранены. |
| R3-12 | PASS | suite 163 OK exit 0; diff API/frontend/packaging/VISION/ARCH/ROADMAP пуст. |
| R3-13 | PASS | все 9 реальных `rd-03-*.png` проверены. |

## Артефакт (независимо)

`installer/Output/GasProjectCalculator-Setup-1.0.0.exe` = 15 273 647 bytes,
SHA256 `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`;
Setup stub Machine 014C / subsystem 2, x64compatible, AMD64 payload; payload
SHA256 `5E25FA92FBA3`; legacy artifact 15 256 037 bytes / SHA256
`2973278F…428F`; Authenticode NotSigned. Других findings/BLOCKER нет.

## Счётчики и решение

- R2 full reviews: C1 = 1 (FAIL); failed reviews 1; Codex calls RD-03: 1/4.
- Допустим C2: одна bounded коррекция и одно повторное полное R2-ревью того же
  TASK (не новый подход). Требуется реальный русский setup-error screenshot
  именно этого артефакта с командой/CWD/revision/результатом и cleanup proof,
  сохранив остальные доказательства. Проектный PASS не присвоен.

## C2 — повторное полное R2-ревью: PASS, RD03-F01 CLOSED

- Ревьюер C2: отдельный Codex worker `ctx_a92d1fc9a28c`
  (`task_c20c237aec63`), `gpt-6.1-sol` high, term_6d8c9eb6. Файлов не менял,
  rerun=0 (evidence reuse).
- RD03-F01 **CLOSED**: C2 запустил ровно тот артефакт
  (`043884…949A`) с `/DIR=C:\Windows\System32\RD03-Forbidden`, реальные
  Далее/Установить, native dialog title «Установка», текст «Невозможно создать
  папку … Ошибка 5: Отказано в доступе.», второй русский диалог, exit 4;
  `rd-03-setup-error.png` (322×179, 8 953 bytes, SHA256
  `02E788748F23C5E3B6AC1FB5991AF93FF415509F5E1162208890130F2867267C`)
  и raw log подтверждают capture. Cleanup: 0 installer processes/HKCU/
  shortcuts, нет install/forbidden dirs, blocker/log, :8000 PID12888 и
  :8138 PID23152 сохранены, artifact hash неизменен.
- **Вердикт C2: PASS**; новых BLOCKER/MAJOR/MINOR/NIT нет.
- Все критерии R3-1..R3-13 повторно подтверждены: RU wizard/error/uninstaller,
  точные ярлыки/имя, Start Menu + optional Desktop, per-user HKCU/no-admin,
  Python-free GUI x64, splash/readiness, три режима 131250/105525/145950,
  loopback/port-skip/close-free, reinstall/uninstall с сохранением markers,
  suite 163 OK, 10 снимков с проверенными hash.
- Артефакт независимо: 15 273 647 bytes, SHA256
  `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`;
  legacy 15 256 037 / `2973278F…428F`; NotSigned; payload hash `5E25…FBA3`.
- Счётчики RD-03: full reviews 2/2, failed 1, Codex calls 2/4; input-токены
  средой не раскрыты. Scope: только 4 installer-файла + evidence/screenshots
  + coordinator workflow; неожиданных product-файлов нет.
- NOT_RUN: reviewer rebuild/install/runtime/suite/browser повторы, commit/push/
  merge/deploy/signing. Остаточные ограничения: текущая Windows/WebView2-среда,
  splash capture через диагностический hold и auto-close, риск прав на эмблему
  RD-01. Итоговая приёмка этапа не назначена.

