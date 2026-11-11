# Итоговый отчёт — этап Windows installer

Дата: 2026-11-11. Статус: **COMPLETE** — все TASK этапа приняты, FINAL
verification пройдена, независимый Codex R3 stage acceptance вернул **PASS**.

## Утверждение и границы

Пользователь утвердил отдельный этап Windows installer: «Да, сделай»
(`docs/workflow/APPROVALS.md`, 2026-11-11). Утверждённые ARCHITECTURE
(SHA256 `259604B4…3375`) и ROADMAP (`78796A2C…FA7F`) не изменялись по смыслу;
VISION.md не менялся.

Ветка: `feature/windows-installer` от `feature/gsv` HEAD `22133a1`, worktree
`D:/Antigravity/GasProjectCalculator`. Коммиты этапа: WI-01 `7fab960`, WI-02
`144a75c`, WI-03 `9eaed0a`, docs/evidence-state `3d291e9`; коммит этого отчёта —
docs-only. R3 принял ревизию `3d291e9`.

В scope: packaging/launcher/native window/installer config, scoped зависимости,
тесты launcher-хелперов, README/docs/evidence. Вне scope и не выполнялись:
кодовая подпись, auto-update, telemetry, cloud, push, merge, deploy, GitHub
Release/публикация, удаление пользовательских данных, глобальные настройки.

## Что поставлено

- `app/desktop_launcher.py` — выбор свободного порта только на `127.0.0.1`,
  in-process uvicorn backend, readiness-probe до показа окна, pywebview
  EdgeChromium окно, остановка backend при закрытии, понятный native error
  dialog, диагностические ключи `--port-file`, `--auto-close-seconds`,
  `--log-file`, `--preferred-port`, `--simulate-startup-failure`.
- `app/resources.py` — разрешение `frontend/index.html` из исходников и из
  PyInstaller bundle; `app/main.py` изменён только в этой точке.
- `desktop_app.py`, `packaging/GasProjectCalculator.spec`,
  `packaging/build.ps1` — PyInstaller onedir, GUI-subsystem, без консоли.
- `installer/GasProjectCalculator.iss` и verify-скрипты — per-user Inno Setup,
  `PrivilegesRequired=lowest`, HKCU, Start Menu всегда, Desktop опционально,
  uninstall без удаления пользовательских файлов.
- `requirements-desktop.txt` — закреплённые PyInstaller 6.22.3, pywebview 6.2.1.
- `tests/test_desktop_launcher.py` — 12 тестов launcher-хелперов.
- README: раздел «Установка на Windows» с точным путём/размером/SHA256
  артефакта, удалением, troubleshooting, localhost/lifecycle; developer-раздел
  с venv/uvicorn/tests сохранён.

## Передаваемый артефакт

- Установщик:
  `D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe`
- Размер: `15 256 037` байт.
- SHA256: `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`.
- Packaged app: `dist\GasProjectCalculator\GasProjectCalculator.exe`, SHA256
  `36A21986EB9A55F1D5309C7AA3E22EDD7EE9F12418B4EC4C27D051B9F77177CC`.
- Артефакт локальный, не подписан, не публиковался и не коммитился
  (`installer/Output/` в `.gitignore`); передаётся пользователю локально.

## Проверки (frozen checklist)

| Критерий | Результат | Доказательство |
| --- | --- | --- |
| Clean x64 build | PASS | WI-01 W1: `packaging/build.ps1` exit 0, PyInstaller 6.22.3; GUI subsystem; `logs/WI-01-build.txt` |
| Installer + Start Menu + optional Desktop | PASS | WI-02 I1–I4: Inno build exit 0; silent HKCU install; ярлыки проверены; `logs/WI-02-install-a/b.txt` |
| Без Python/терминала | PASS | WI-01 W2, WI-02 I5: PATH без Python, `python` not found, без консоли |
| Первый запуск ждёт backend | PASS | WI-01 W5, WI-02 I6: readiness → port file → создание окна |
| ГСН, ГСВ, общая смета | PASS | WI-01 W6, WI-02 I7: итоги 131250 / 105525 / 145950 |
| Только localhost, конфликт портов | PASS | WI-01 W3–W4, WI-02 I8: только 127.0.0.1; занятые 8000/8123 пропущены |
| Закрытие окна завершает backend | PASS | WI-01 W7, WI-02 I9: exit 0, порт свободен, дочерних процессов нет |
| Понятная ошибка запуска | PASS | WI-01 W8, WI-02 I10: native диалог, exit 1, `status=failed` |
| Uninstall сохраняет файлы пользователя | PASS | WI-02 I11: два цикла uninstall; три маркера вне `{app}` сохранены |
| Developer uvicorn работает | PASS | WI-01 W9: `GET /` 200 на 127.0.0.1:8010; user :8000 не тронут; 146 OK |
| README ведёт к установщику | PASS | WI-03 D1–D5; точный путь/размер/SHA256 |

Интегрированная FINAL verification: docs-only diff после принятого артефакта,
artifact hash совпал, `146 tests OK` exit 0, user uvicorn :8000 PID 12888 не
тронут — `docs/workflow/evidence/FINAL-WINDOWS-INSTALLER-EVIDENCE.md`.

## TASK и приёмка

| TASK | Риск | Вердикт | Codex calls | Коммит |
| --- | --- | --- | ---: | --- |
| WI-01 packaging/window | R2 | PASS `gpt-6.1-sol` high, C1 | 1 | `7fab960` |
| WI-02 installer | R2 | PASS `gpt-6.1-sol` high, C1 (1 MINOR backlog) | 1 | `144a75c` |
| WI-03 docs | R0 | PASS координатора по D1–D5 | 0 | `9eaed0a` |
| FINAL verification | R0 | PASS координатора | 0 | `3d291e9` |
| FINAL stage acceptance | R3 | PASS `gpt-6-astra` high, call 1 | 1 | `3d291e9` |

Всего Codex calls этапа: 3. Точный input-token расход в records не
представлен; потолки R2 (4 calls / 3M на TASK) и R3 (6 / 5M) не превышены.
Вердикты и evidence: `docs/workflow/reviews/WI-0*-review.md`,
`docs/workflow/reviews/FINAL-STAGE-review.md`.

## Отклонения и остаточные ограничения

- Toolchain: указанный portable ISCC неполон (нет `ISCmplr.dll`); build script
  проверил кандидатов и использовал локальный полный Inno Setup 6.4.1 без
  системной установки. R3 признал допустимым.
- `WI02-R1-F1` **MINOR** backlog: `installer/verify-runtime.ps1` рекурсивно
  удаляет caller-supplied `WorkDir` после `GetFullPath`; нужен bounded scratch
  ownership/path validation. Это helper, не runtime-дефект; не исправлялся.
- Чистая вторая Windows x64 машина/VM недоступна: build/install/runtime
  проверены только на этой машине.
- Установщик не подписан; SmartScreen может показать предупреждение.
- Первый запуск требует Microsoft Edge WebView2 Runtime; фактическое отсутствие
  WebView2 не воспроизводилось — проверен общий симулированный отказ с понятным
  диалогом.
- Uninstall через GUI «Параметры → Приложения» не прокликан; тот же Inno
  uninstaller выполнен беззвучно в WI-02.
- Push/merge/deploy/публикация не выполнялись и не разрешены.
- Тестовые маркеры пользовательских файлов, созданные в WI-02 для проверки
  сохранности, намеренно оставлены вне каталога установки; их можно удалить
  вручную.

## Передача

Пользователь запускает `GasProjectCalculator-Setup-1.0.0.exe`, устанавливает для
текущего пользователя без прав администратора и запускает приложение из
**Пуск → GasProjectCalculator** (ярлык Desktop — по желанию в мастере). Python и
терминал не требуются. Удаление — через «Параметры → Приложения»; журнал и файлы
пользователя в `%LOCALAPPDATA%\GasProjectCalculator` сохраняются.
