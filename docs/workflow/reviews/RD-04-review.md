# RD-04 — R0 acceptance (координатор)

- Логический TASK: RD-04 (R0, документация). Исполнитель: OpenCode Flash
  `ctx_d59e441d9384` (`task_cb670182c32f`).
- Baseline `ffe17fb`; единственное изменение исполнителя — `README.md`
  (+85/−30) и `docs/workflow/evidence/RD-04-evidence.md`. Код/тесты/installer/
  mapping/frontend/workflow-документы не менялись.
- R0: автоматическая проверка frozen checklist координатором; Codex не
  привлекался.

## Вердикт: PASS

| ID | Результат | Проверка |
| --- | --- | --- |
| R4-1 | PASS | H1 `СС.Расчет`, подпись `Калькулятор ГСН и ГСВ` (чтение README). |
| R4-2 | PASS | exact path `installer\Output\GasProjectCalculator-Setup-1.0.0.exe`, size 15 273 647, SHA256 `043884…949A`; совпало с RD-03 evidence и фактическим файлом. |
| R4-3 | PASS | разделы «Установка на Windows»/«Удаление»: RU installer, Start Menu всегда, Desktop опционален, uninstall сохраняет `%LOCALAPPDATA%\GasProjectCalculator`. |
| R4-4 | PASS | окно 1050×740 (min 860×620), заставка 520×320, `prefers-reduced-motion`. |
| R4-5 | PASS | явно указано, что расчёты/бизнес-правила/API/developer-путь (uvicorn/тесты) не менялись. |
| R4-6 | PASS | все относительные ссылки README разрешены; `MISSING_TOTAL=0` для 23+ ссылок, включая RD-01/RD-02/RD-03 screenshots/evidence/reviews. |
| R4-7 | PASS | нет заявлений о signing/publication/telemetry/cloud; артефакт назван локальной неподписанной сборкой. |

## Примечания

- Проверка ссылок и artifact hash выполнена координатором read-only командами
  (CWD `D:/Antigravity/GasProjectCalculator`), exit 0; MISSING — 0.
- NOT_RUN: повторный suite/browser/install — не требуется: изменён только
  README, продуктовый код не затронут; предыдущие доказательства
  переиспользуются по review-policy.
- Счётчики: R0, Codex calls 0; новый подход не требуется.
