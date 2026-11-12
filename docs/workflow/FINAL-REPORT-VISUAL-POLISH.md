# FINAL REPORT — визуальная доработка 1.2.0 (local)

2026-11-12. Статус этапа: **COMPLETE по независимым приёмкам**. Это локальный
результат 1.2.0; публикация/push/merge/release/deploy не выполнялись.

## Итог

- Шапка и нижняя полоса переделаны по `header-detail-reference.jpg` и
  `footer-detail-reference.jpg`; заставка — по
  `splash-installer-reference.jpg`; установщик получил фирменную графику в том
  же стиле; добавлены ограниченные дизайнерские улучшения в рамках brief.
- VP-01 (MD-02 A2) принят независимым R2 Codex `gpt-6.1-sol`/high;
  MD02-N1 закрыт.
- VP-02 (MD-03 A2/C1) принят независимым R2 Codex `gpt-6.1-sol`/high:
  W1–W11 PASS, 0 BLOCKER/MAJOR/MINOR; NIT VP02-R2-N1 (формулировка manifest)
  исправлен.
- Отдельная финальная stage-приёмка Codex `gpt-6.1-sol`/high: **PASS**.

## Локальный артефакт

| Параметр | Значение |
| --- | --- |
| Путь | `installer/Output/GasProjectCalculator-Setup-1.2.0.exe` |
| Размер | 15 373 267 байт |
| FileVersion | 1.2.0.0 |
| ProductVersion | 1.2.0 |
| SHA256 | `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113` |

Прежние 1.0.0/1.1.0/legacy bytes не изменены; remote releases не трогались.
Local scoped commit: `bbd0f606b23ce2620676ea92bce9bcc6f256422d`.

## Проверки (первичные доказательства)

- Полный suite один раз по HEAD `1689773718`:
  `.\.venv\Scripts\python.exe -m unittest discover -s tests` — exit 0,
  **219 tests OK** (`evidence/logs/VP-02-final-full-suite.txt/.exit.txt`).
- Targeted: 36 OK/exit 0; static: 137 assertions/exit 0; `git diff --check` 0.
- RU wizard welcome/dir/tasks/ready/installing/finish (598×464), фирменная
  графика, читаемые кнопки, RU-only, Desktop task выключен.
- Изолированный Temp install 1.1.0 → upgrade 1.2.0 → reinstall → uninstall:
  4×exit 0; HKCU/ярлыки восстановлены; 106 user files unchanged; sentinels
  сохранены.
- Установленное приложение без Python/CLI (`pythonResolved=false`), native
  splash 560×450, main 800×540 / min 760×520, DPR=1, `scrollY=0`,
  action+total видимы; browser desktop/min/mobile390×844.
- D1–D5 settled: 75600/79275/71400/63000/70875 при `opacity=1`;
  combined 151000/7550/158550; САКЗ/ПК/район/НДС 5%; legacy/mixed 422;
  ГСН-регрессия.
- Lifecycle: loopback-only, занятый тестовый порт, закрытие без дочерних
  процессов, русский error path/exit 1, reduced motion.

## Приёмки и модели

| Роль | Реальный worker | Модель | Вердикт |
| --- | --- | --- | --- |
| Реализация | Codex implementer `ctx_988a8c02d5c3` | `gpt-6-astra`, high | evidence |
| VP-01 R2 | Codex reviewer `ctx_fd6edd091391` | `gpt-6.1-sol`, high | PASS |
| VP-02 R2 | Codex reviewer `ctx_df0f7573e041` | `gpt-6.1-sol`, high | PASS |
| Final stage | Codex reviewer `ctx_059202c6763a` | `gpt-6.1-sol`, high | PASS |

Evidence/logs: `docs/workflow/evidence/VP-02-evidence.md`,
`docs/workflow/evidence/logs/VP-02-*`; screenshots:
`docs/screenshots/visual-02-*`; review verdicts:
`docs/workflow/reviews/VP-01-review.md`, `VP-02-review.md`,
`VP-02-final-stage-review.md`.

## Ограничения и NOT_RUN

- Публикация/push/merge/deploy/release/signing не выполнялись; 1.2.0 — local.
- Не доказаны: чистая VM без Python/WebView2, иные DPI, полный OS packet
  capture, независимый повторный запрос remote releases.
- Исходный GUI wrapper numeric exit отсутствует; компенсирован finish/raw log
  и четырьмя cycle exit 0.
- Пользовательская установка/HKCU/ярлыки/сессии, `.venv`, `:8000`/`:8138`
  сохранены.
