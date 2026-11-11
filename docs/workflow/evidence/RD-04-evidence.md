# RD-04 evidence — README и пользовательская документация редизайна (R0)

Исполнитель: OpenCode implementer (Orca worker), logical TASK RD-04, dispatch
`ctx_d59e441d9384`, task `task_cb670182c32f`. Это evidence исполнителя; проектный
PASS не заявляется.

## Workspace / baseline

- CWD: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/ss-calculator-redesign`
- Baseline при получении задачи: HEAD `ffe17fb` (RD-03 accepted/committed).
- В ходе работы координатор сделал workflow-коммит `b61205a`
  «docs(workflow): record RD-03 acceptance and RD-04 dispatch», затронувший
  только `docs/workflow/HISTORY.md` и `docs/workflow/STATE.md`. Worker эти
  файлы не менял; его изменение — только `README.md`.
- Push/merge/deploy/signing не выполнялись. Код, тесты, installer, mapping и
  workflow-документы не менялись.

## Что изменено (только allowlist)

Единственный изменённый файл — `README.md`:

- Заголовок продукта `СС.Расчет`, подпись `Калькулятор ГСН и ГСВ`.
- Раздел «Установка на Windows»: exact local artifact path, size
  **15 273 647 bytes**, SHA256
  `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`;
  per-user install без Python/CLI/консоли; Start Menu ярлык всегда, Desktop —
  опционален; ярлык и заголовок окна `СС.Расчет`; издатель
  `ООО «Северное сияние»`; артефакт описан как локальная неподписанная сборка.
  Исправлены прежние устаревшие size/hash (15 256 037 /
  `2973278F…428F`) и прежнее имя ярлыка `GasProjectCalculator`.
- Раздел «Удаление»: русский uninstaller удаляет файлы программы и ярлыки,
  сохраняет пользовательские файлы в `%LOCALAPPDATA%\GasProjectCalculator`.
- Новый раздел «Что изменилось в редизайне»: бренд, компактное окно
  **1050×740** (минимум **860×620**), адаптивность; локальная русская заставка
  520×320 с анимацией потока газа, показывается только во время старта backend;
  `prefers-reduced-motion` уважается.
- Явное указание, что расчёты, бизнес-правила, API, developer-путь (uvicorn и
  тесты) не менялись.
- Раздел «Интерфейс»: реальные ссылки на скриншоты RD-01/RD-02/RD-03.
- Раздел «Доказательства»: добавлены ссылки на RD-01/RD-02/RD-03 evidence и
  review под `docs/workflow/reviews/`.
- Сохранены без изменений разделы: «Что умеет калькулятор», «Технологии»,
  «Бизнес-правила GSN v1.0», «Бизнес-правила ГСВ», «Структура проекта», «Для
  разработчика», «Устранение неполадок», «Пример расчёта», «Пример расчёта
  ГСВ» (developer uvicorn/tests и calculation-документация не переписаны).

Новых заявлений о код-подписи, публикации, телеметрии, cloud или сетевом
доступе нет; указано лишь, что артефакт — локальная неподписанная сборка, а
backend слушает только loopback (подтверждено evidence RD-02/RD-03).

## Проверки артефакта и ссылок

Команды выполнялись из CWD = `D:\Antigravity\GasProjectCalculator`
(PowerShell 5.1). Exit code 0 для всех перечисленных проверок.

### Artifact (сверено с RD-03 evidence)

```text
Get-Item   installer\Output\GasProjectCalculator-Setup-1.0.0.exe
Get-FileHash ... -Algorithm SHA256
```

| Поле | Факт | RD-03 evidence | Совпадение |
| --- | --- | --- | --- |
| path | `installer\Output\GasProjectCalculator-Setup-1.0.0.exe` | тот же | да |
| size | 15 273 647 bytes | 15 273 647 bytes | да |
| SHA256 | `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A` | тот же | да |

### Screenshot / evidence / review existence

Все обязательные файлы существуют; размеры и SHA256 для RD-02/RD-03
скриншотов совпадают с соответствующими evidence.

```text
docs/screenshots/rd-01-1050x740-initial.png         OK  141400
docs/screenshots/rd-01-gsn-result-1050x740.png       OK   74706
docs/screenshots/rd-01-gsv-result-1050x740.png       OK   68587
docs/screenshots/rd-01-combined-result-1050x740.png  OK   72545
docs/screenshots/rd-01-390x844-layout.png            OK   64878
docs/screenshots/rd-02-splash.png                    OK   85195  SHA256 51222A95…10032 (RD-02)
docs/screenshots/rd-02-main-window.png               OK  141421  SHA256 2C6D6751…CDD86 (RD-02)
docs/screenshots/rd-03-wizard-welcome.png            OK   54587  SHA256 ED139A20…05DD4 (RD-03)
docs/screenshots/rd-03-wizard-tasks.png              OK   42151  SHA256 C2B72DEE…1934D (RD-03)
docs/screenshots/rd-03-wizard-finish.png             OK   53895  SHA256 83C10A9D…F1204 (RD-03)
docs/screenshots/rd-03-installed-main.png            OK  144083  SHA256 113D3132…F82E4 (RD-03)
docs/screenshots/rd-03-uninstall-confirm.png         OK   18990  SHA256 94EF0071…2CE48 (RD-03)
docs/screenshots/rd-03-setup-error.png               OK    8953  SHA256 02E78874…267C (RD-03)
docs/workflow/evidence/RD-01-evidence.md             OK   11621
docs/workflow/evidence/RD-02-evidence.md             OK   12827
docs/workflow/evidence/RD-03-evidence.md             OK   21478
docs/workflow/reviews/ (RD-01/02/03-review.md)       OK
```

Дополнительно все относительные markdown-ссылки README разрешены скриптом
(`[regex]` по `](...)`, `Test-Path` для каждого локального пути): **MISSING — 0**.
Внешние ссылки (`https://…`) не проверялись локально; это прежние
developer-инструкции, не новые claims.

## Final diff / status

```text
git status --short
 M README.md

git diff --stat HEAD
 README.md | 115 +++++++++++++++++++++++++++++++++++++++-------------
 1 file changed, 85 insertions(+), 30 deletions(-)
```

`git diff HEAD -- app tests installer packaging frontend` пуст (код/тесты/
installer/mapping не менялись). Workflow-документы worker не менял.

## Frozen acceptance checklist (R4-1..R4-7)

| ID | Результат (кандидат) | Evidence |
| --- | --- | --- |
| R4-1 | README называет продукт `СС.Расчет` с подписью `Калькулятор ГСН и ГСВ` | `README.md` H1 и подзаголовок |
| R4-2 | Exact artifact path, size, SHA256 совпадают с RD-03 | таблица «Artifact» выше; `Get-FileHash` = `043884…949A` |
| R4-3 | Описаны RU installer, ярлыки, uninstall и сохранение user files | `README.md` разделы «Установка на Windows», «Удаление» |
| R4-4 | Описаны компактное окно, заставка, reduced motion | `README.md` раздел «Что изменилось в редизайне» |
| R4-5 | Указано, что расчёты/API/developer path не менялись | `README.md` раздел «Что изменилось в редизайне»; developer-разделы сохранены |
| R4-6 | Ссылки на реальные скриншоты/evidence существуют | проверка existence выше, MISSING — 0 |
| R4-7 | Нет неподтверждённых claims/signing/publication | README: указано «локальная неподписанная сборка»; нет заявлений о публикации/телеметрии/cloud |

## NOT_RUN

- Полный test suite и browser verification не перезапускались: изменён только
  `README.md`, продуктовый код/тесты не затрагивались. Suite и UI уже
  подтверждены в RD-01/RD-02/RD-03 evidence (`Ran 163 tests ... OK`).
- Повторная проверка installer install/uninstall NOT_RUN: артефакт не
  пересобирался, использованы фактический size/SHA256 и скриншоты из
  RD-03 evidence.
- Независимое ревью и проектный PASS — за ревьюером/координатором; здесь PASS
  не заявляется.
