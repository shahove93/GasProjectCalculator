# RD-02 — независимое R2-ревью (Codex)

- Логический TASK: RD-02, подход A1, цикл C1.
- Ревьюер: отдельный Orca Codex worker `ctx_66502b51d130`
  (`task_f3daf8be58f6`), model `gpt-6.1-sol`, effort high, terminal
  term_55b493f1.
- Ревизия: ветка `feature/ss-calculator-redesign`, HEAD `2703e83`,
  продуктовый baseline RD-02 `041b13d`, рабочее дерево с uncommitted RD-02.
- Ревьюер файлов не менял и не коммитил; повторных прогонов не было
  (`rerun=0`) по evidence-reuse rule. Сверены фактический diff, исходные логи,
  четыре реальных native-снимка и SHA256 launcher/splash/снимков.

## Вердикт: PASS

BLOCKER/MAJOR/MINOR/NIT отсутствуют; открытых/закрытых finding IDs нет.

| ID | Вердикт | Подтверждение |
| --- | --- | --- |
| R2-1 | PASS | `RD-02-title-size.json`, `rd-02-main-window.png`: title ровно `СС.Расчет`. |
| R2-2 | PASS | `RD-02-main-window.json`/`.txt`: 1050×740, clamp 300×200→860×620. |
| R2-3 | PASS | `RD-02-splash-hold-launcher.txt` (shown до backend ready), `RD-02-splash-window.json`, `rd-02-splash.png`: реальная локальная русская заставка; hold — разрешённый диагностический хук. |
| R2-4 | PASS | normal log: ready → hidden main → splash closed → main shown; `rd-02-main-window.png`. |
| R2-5 | PASS | readiness 0,75 s, main через 107 мс; sleep только в диагностических ветках. |
| R2-6 | PASS | `frontend/splash.html`, `RD-02-browser.txt`: emulated media=true, gas/glow animation none, duration 0 s, статичные transform. |
| R2-7 | PASS | file URI, только локальная эмблема; protocol=file, resourceEntries=[]. |
| R2-8 | PASS | failure logs: splash closed → русская ошибка → Backend stopped → exit 1; реальный диалог на снимке. |
| R2-9 | PASS | busy 8000→127.0.0.1:8001, после close listener исчез; :8000 PID12888 и :8138 PID23152 сохранены. |
| R2-10 | PASS | suite 163 OK exit 0; diff `app/main.py`/calculators/`frontend/index.html` пуст. |
| R2-11 | PASS | новые/изменённые тесты title/geometry/splash local URI/asset/no-network/reduced-motion/gas-flow; module 23 OK, suite 163 OK. |

## Scope

Изменены только allowlisted `app/desktop_launcher.py`, `app/resources.py`,
`packaging/GasProjectCalculator.spec`, `tests/test_desktop_launcher.py` и новый
`frontend/splash.html`; spec включает splash/assets. Evidence/screenshots
допустимы; STATE/HISTORY — координаторские workflow-записи. Неожиданных
продуктовых файлов, изменений installer/user data/privacy storage нет.

## Остаточное / NOT_RUN

- NOT_RUN: самостоятельные suite/browser/runtime повторы, packaged
  splash/PyInstaller/installer build (RD-03), реальная смена Windows animation
  effects, commit/push/merge/deploy.
- Ограничения: native-снимки 96 DPI; reduced motion подтверждён эмуляцией;
  failure evidence покрывает ранний диагностический сбой; WebView2
  инициализируется ~0,57 s до backend без искусственной задержки; упакованный
  вариант требует RD-03; права на эмблему — ранее зафиксированный риск RD-01.

## Счётчики

- R2 full reviews: 1 (PASS); failed 0; Codex calls: 1 из резерва ≤4;
  input-токены по факту вызова не раскрыты средой.
- Rerun=0; файловых изменений ревьюером нет.
- Следующий шаг — scoped commit RD-02 и переход к RD-03.
