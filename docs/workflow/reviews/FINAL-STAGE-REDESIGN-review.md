# Final stage acceptance — СС.Расчет redesign (Codex R3)

- Стадия: утверждённый редизайн и фирменный вид `СС.Расчет` (APPROVALS
  2026-11-11, ARCHITECTURE `98ACB1F2…B7DA`, ROADMAP `1B1CBD0B…D631`).
- Ревьюер: отдельный Orca Codex worker `ctx_3b5e848dc8a6`
  (`task_eca7c45d6240`), model `gpt-6-astra`, effort high, terminal
  term_6def3abc.
- Интегрированный diff: `e24d806..a14f032`; фактический HEAD на момент
  приёмки `a14f032` (после него — только docs/workflow).
- Ревьюер файлов не менял, приложение не запускал, повторных испытаний не
  выполнял (`rerun=0`), процессы `:8000`/`:8138` не затронуты.

## Вердикт: STAGE ACCEPTANCE PASS

Открытых BLOCKER/MAJOR нет.

| Область | Вердикт | Подтверждение |
| --- | --- | --- |
| Бренд и оформление | PASS | title/ярлыки `СС.Расчет`, подпись `Калькулятор ГСН и ГСВ`, оригинальный круглый знак без wordmark, исходный фиолетовый на светлом диске, navy/teal/pipe — frontend diff, RD-01 browser/provenance, rd-03-installed-main. |
| Геометрия/responsive | PASS | 1050×740, clamp до 860×620, 1050/860/390 без горизонтального обрезания действий/итогов. |
| Splash | PASS | локальная русская сцена газа к дому, file URI, без сети, reduced-motion `none`, ready→main 107 мс без искусственной выдержки, русский failure с закрытием splash. |
| Установка | PASS | Russian-only wizard/error/uninstaller, точные ярлыки, Start Menu всегда + optional Desktop, per-user HKCU/no admin, x64 payload, Python-free GUI subsystem 2. |
| Расчёты | PASS | 125000/6250/131250, 100500/5025/105525, 139000/6950/145950; ставки/НДС сохранены. |
| Lifecycle/data | PASS | только `127.0.0.1`, busy 8123→8124, close освобождает порт, developer uvicorn не изменён, reinstall/uninstall сохраняют markers с теми же SHA256. |
| Документация/delivery | PASS | README описывает установку/запуск/удаление/окно/splash/локальную неподписанную сборку; artifact 15 273 647 bytes, SHA256 `04388410…949A`, git-ignored, NotSigned; legacy installer сохранён. |
| Интеграция | PASS | suite 163 OK/exit 0; `app/main.py`, calculators, requirements, calculation tests без diff; `test_main.py` — только title assertion; неожиданных файлов/секретов нет. |
| Маршрутизация/учёт | PASS | RD-01 R1 1 PASS/0 FAIL/0 Codex; RD-02 R2 1 PASS/1 call; RD-03 R2 1 FAIL→1 PASS/2 calls, RD03-F01 CLOSED; RD-04 + RD-FINAL R0; скрытых failed reviews нет. |
| Утверждения | PASS | SHA256 ARCHITECTURE/ROADMAP/VISION совпали с APPROVALS. |

## Findings

- RD-01 F1–F3 (NIT) — backlog: stale listing двух layout-PNG, mojibake в 422
  JSON, дублирующиеся примечания в browser log.
- RD-FINAL-N01 (MINOR) — STATE содержал устаревший HEAD `6d91036`/C2 dirty;
  исправлено координатором в финальном STATE на `a14f032`/clean.
- RD-FINAL-N02 (NIT) — неверный относительный путь ссылки RD-FINAL в STATE;
  исправлено на `evidence/RD-FINAL-evidence.md`.
Оба новых замечания не затрагивают продуктовые критерии и закрыты
документально.

## Остаточные риски / NOT_RUN

- Формальные корпоративные права на эмблему репозиторием не установлены —
  остаточный риск; лицензия не выдумывалась.
- Installer неподписан → возможен Windows SmartScreen; публикация/подпись не
  выполнялись.
- Проверена только текущая Windows/WebView2-среда и 96 DPI; reduced motion
  подтверждён эмуляцией; failure path — ранний диагностический; мобильные
  снимки используют screenshot-only overflowX workaround без изменения
  продуктового CSS.
- NOT_RUN: push/merge/deploy/release/deploy/signing; удалённый аудит
  публикации не требовался (её не было).
- Итог: этап редизайна принимается; FINAL-REPORT и COMPLETE — за координатором.
