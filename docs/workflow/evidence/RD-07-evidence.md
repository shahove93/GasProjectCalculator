# RD-07 — финальная интегрированная проверка (R0, verifier)

- Логический TASK: RD-07, R0 checklist verification (без project PASS).
- Verifier: Orca OpenCode/DeepSeek Flash, dispatch `ctx_e7b35f80b38d`
  (`task_d2acfce2887d`, term_d6f1cdcb). Read-only по продукту.
- Workspace: `D:\Antigravity\GasProjectCalculator`, ветка
  `feature/ss-calculator-redesign`.
- Baseline: `4b0be03` (`4b0be033b0ba5598c82062394d7fb69064c73fde`).
- Final revision: `8ecb0e5` (`8ecb0e505734e0314b7063a01da948af83971dc6`).
  Suite выполнен на `3a3a6b0`; между suite и artifact/runtime-проверками HEAD
  сдвинулся docs-only коммитом `8ecb0e5` (только `HISTORY.md`, `STATE.md`), т.е.
  продуктовое состояние идентично проверенному.
- Отчёт не выставляет project PASS: его фиксирует координатор по R0.

## F1 — diff/status/scope

`git status --short` перед записью evidence-логов пуст (clean). Логи:
`logs/RD-07-scope.txt`.

Продуктовый diff `4b0be03..HEAD` — 4 файла, ровно allowlist:

| Файл | Δ |
| --- | --- |
| `frontend/index.html` | 970 (+/-) |
| `app/desktop_launcher.py` | 75 (+/-) |
| `tests/test_desktop_launcher.py` | 6 (+/-) |
| `tests/test_frontend_redesign.py` | 37 (+) |

Также docs/evidence/screenshots/README: `ARCHITECTURE.md`, `ROADMAP.md`,
`README.md`, `docs/design/*` (2 reference PNG), `docs/screenshots/rd-05-*`
(20) и `rd-06-*` (34), `docs/workflow/*` (APPROVALS, briefs, STATE, HISTORY,
tasks, reviews, evidence/logs).

Проверено отсутствие diff в защищённых путях: `app/main.py`,
`app/calculator.py`, `app/gsv_calculator.py`, `requirements.txt` — пусто.
Installer scripts/lifecycle, чужих и секретных файлов в diff нет.
`git diff --check`: exit 0 (только CRLF-предупреждение рабочей копии
`HISTORY.md`, не ошибка diff).

## F2 — полный suite (ровно один раз)

- CWD: `D:\Antigravity\GasProjectCalculator`
- Команда: `.\.venv\Scripts\python.exe -m unittest discover -s tests`
- Exit code: **0**
- Итог: `Ran 167 tests in 2.126s` — **OK**
- Revision suite: `3a3a6b0d95214d2390d1c92a6a3b884e20634eec`
- Лог: `docs/workflow/evidence/logs/RD-07-suite.txt` (полный stdout).

## F3 — installer/artifact факты

`logs/RD-07-artifacts.txt`.

| Артефакт | Size | SHA256 | Статус |
| --- | --- | --- | --- |
| `installer/Output/GasProjectCalculator-Setup-1.0.0.exe` | 15 286 980 | `71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08` | match |
| `installer/Output/legacy/GasProjectCalculator-Setup-1.0.0-pre-compact.exe` | 15 273 647 | `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A` | match |
| `installer/Output/legacy/GasProjectCalculator-Setup-1.0.0-previous-stage.exe` | 15 256 037 | `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F` | match |
| `dist/GasProjectCalculator/GasProjectCalculator.exe` | 6 836 651 | `5403540C4172779ED6F97381A9618FE423D0915A6BEC1710BAE2B578F6ACDD2C` | match |

Значения совпадают с RD-06 review/evidence и README. Legacy-файлы лежат в
`installer/Output/legacy/` (task-текст сокращал путь); hashes совпадают.

## F4 — evidence/screenshots и выборочная сверка

- `docs/screenshots/rd-05-*` — **20** файлов; `rd-06-*` — **34** файла
  (фактический подсчёт).
- `logs/RD-05-native.json` (31 393 B) и `logs/RD-06-installed-native.json`
  (34 013 B) присутствуют.
- Mobile B7: `docs/screenshots/rd-06-installed-mobile-390x844.png` — 82 172 B,
  SHA256 `FFB848567864F2C5E5A9ABD977189E4F4564CCFA06BF30A509E3CB8E2A3243A5`;
  `RD-06-mobile-390.txt`: viewport 390×844, `scrollWidth/clientWidth=375/375`,
  `scrollHeight/clientHeight=889/844`, `scrollX/Y=0/0`, `hScroll=false`, max
  right edge 375; PNG ровно 390×844. Соответствует C2 PASS.
- Значения `131 250`, `105 525`, `145 950` найдены в
  `RD-06-installed-native.json` (формат с разделителем разрядов и ₽).
- Review records сохранены: RD-05 PASS (F1/F2 MINOR); RD-06 C1 FAIL
  (`RD06-F01` MAJOR, old SHA `BA0D…455C` SUPERSEDED), C2 PASS,
  `RD06-F01` CLOSED, `RD06-F02` MINOR backlog. FAIL/история не подменены.

## F5 — вычисления/API/requirements

`app/main.py`, `app/calculator.py`, `app/gsv_calculator.py`,
`requirements.txt` — вне diff. Значения 131250/105525/145950 подтверждены
reuse-артефактами RD-05/RD-06 (см. F4). Новых вычислений не проверялось и не
требовалось.

## F6 — документы/счётчики/route

- README: окно **800×540**, min **760×520**, размер/Hash нового installer
  (`15 286 980` / `71232EE4…7E08`), ссылки на новые `rd-06-*` screenshots —
  все 7 целей существуют.
- STATE и HISTORY согласованы: RD-05 1 full/0 FAIL/1 Codex; RD-06
  2 full/1 FAIL/2 Codex, RD06-F01 CLOSED; RD-07 R0 dispatch записан.
  Прежние счётчики RD-01..RD-04/stage1 сохранены; review route не подменён
  (RD-05 R2 Codex, RD-06 Codex R2 C1/C2).

## Runtime / отсутствие утечек

`logs/RD-07-runtime.txt`.

- `:8000` — PID 12888 (не тронут); `:8138` — PID 23152 (не тронут).
- Пользовательская установка `%LOCALAPPDATA%\Programs\GasProjectCalculator`:
  PID 13248 работает; exe 6 834 942 B `5E25FA92A530E104AA69BC7153C068FA34C477659F375142EA7D047257A0FBA3`
  — совпадает с RD-06 (unchanged user install), не переустановлена.
- Лишних test backend/портов/окон не обнаружено: единственные слушатели
  проекта — 8000/8138 (и 8001 у пользовательского приложения). Venv-процессы
  12424/20204 — родители тех же uvicorn, не новые test instances.

## Evidence reuse / NOT_RUN

Переиспользовано без rerun: build/package/installer, изолированная
install/uninstall, native screenshots, lifecycle, mobile C2 capture, значения
расчётов. **NOT_RUN**: повторная сборка/установка, повторный native/UI capture,
повторный Codex review, повторная проверка API-поведения сверх suite.

## Расхождения

1. HEAD сдвинулся `3a3a6b0 → 8ecb0e5` во время проверки — docs-only
   (`HISTORY.md`, `STATE.md`), продукт не изменён; suite остаётся валиден для
   финального состояния.
2. Legacy/previous-stage installer находятся в `installer/Output/legacy/`, а
   не в корне `installer/Output/`; размеры/SHA256 совпадают с ожидаемыми.
3. Прочих расхождений scope/artifact/evidence не найдено.

Итог R0: все обязательные проверки выполнены, product FAIL-признаков нет.
Project PASS не выставляется — фиксирует координатор.
