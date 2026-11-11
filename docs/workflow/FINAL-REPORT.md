# FINAL REPORT — этап ГСВ

Статус: **COMPLETE**.

## Итог

Утверждённый этап ГСВ реализован в ветке `feature/gsv` от baseline `2949223`:
добавлены изолированный расчёт ГСВ, API `/calculate/gsv` и `/calculate/combined`,
три режима интерфейса (ГСН, ГСВ, ГСН + ГСВ), серверная и клиентская валидация,
browser evidence desktop/mobile и документация. Прежние 57 тестов ГСН и
контракт `POST /calculate` сохранены. Push, merge и deploy не выполнялись.

## Ревизии

- Stage baseline: `2949223` (`main`).
- Продуктовые коммиты: `501a32b` (модуль ГСВ), `dab59a9` (API),
  `9dc84e0` (UI), `0cd48bc` (response models), `8d2d215` (UI regression).
- Последняя продуктовая ревизия: `8d2d215`; финальный docs/evidence commit
  добавляет этот отчёт, README NIT и HISTOR.
- Утверждение: APPROVALS.md, SHA256 VISION/ARCHITECTURE/ROADMAP/MODEL-ROUTING
  совпали при финальной приёмке.

## TASK, маршруты, вердикты и счётчики

| TASK | Риск | Приёмка | Вердикт | Codex calls |
| --- | --- | --- | --- | ---: |
| GSV-01 модуль ГСВ | R1 | OpenCode Pro `ctx_6f8faa93b48a` | PASS | 0 |
| GSV-02 API | R2 | Codex `ctx_a52e8c040396` C1 | FAIL (административный) | 1 |
| GSV-02 API | R2 | Codex `ctx_ed2dda90c5c1` C2 | PASS | 1 |
| GSV-03 UI | R1 | OpenCode Pro `ctx_d7c8f160505f` | PASS, 1 NIT | 0 |
| GSV-04 docs/evidence | R0 | чек-лист координатора | PASS | 0 |
| FINAL R3 call 1 | R3 | Codex `ctx_a35b269f1f44` | FAIL: 4 MAJOR + 1 NIT | 1 |
| GSV-02 regression | R2 | Codex `ctx_ddd46cfbef19` | PASS | 1 |
| GSV-03 regression | R1 | OpenCode Pro `ctx_faa3f1ff8d22` | PASS | 0 |
| FINAL R3 call 2 | R3 | Codex `ctx_b632e310754a` | PASS, 1 docs NIT | 1 |

Codex: GSV-02 — 3 вызова (1 FAIL + 2 PASS); финальная приёмка — 2 (1 FAIL +
1 PASS), в пределах R2 ≤4 и R3 ≤6. Все routed PASS получены до перехода.

## Фактические проверки

- Полный suite: `.\.venv\Scripts\python.exe -m unittest discover -s tests`,
  CWD `D:/Antigravity/GasProjectCalculator`, exit 0, `Ran 134 tests ... OK`.
  Логи: `evidence/logs/GSV-02R-suite.txt`, `GSV-03-regression.md`.
- API: 29 тестов, exit 0 (`logs/GSV-02R-api.txt`, OpenAPI — `GSV-02R-openapi.txt`).
- GSV unit: 48 тестов, exit 0 (`logs/GSV-01-unit.txt`).
- Browser (Orca built-in): ГСН 105000/5250/110250; ГСВ 100500/5025/105525;
  combined ГСН 75600, ГСВ 70350, 139000/6950/145950; mobile 390×844
  fits=true; ПК при САКЗ 0/1/0; diameter 58 client/422; regression-сценарии
  initial/stale/hidden validation. Артефакты: `evidence/GSV-03-browser.md`,
  `GSV-03-regression.md`, 10 скриншотов `docs/screenshots/gsv-03-*.png`.
- Продуктовый код после проверок не менялся; README/evidence — docs-only.

## Отклонения и исправления

- GSV-02 C1 FAIL был административным (baseline/незакоммиченные evidence),
  не дефект; C2 PASS.
- GSV-03 первая попытка зависла после изменения UI без worker_done; координатор
  остановил её и продолжил логический TASK; browser evidence собрано.
- Финальная приёмка call 1 выявила 4 MAJOR (UI initial mode, stale response,
  hidden validation; отсутствие response models) и 1 NIT. Все исправлены,
  повторно приняты R2/R1, затем этап принят call 2. NIT README (131→134)
  исправлен в этом отчёте.
- Scope соблюдён: нижние примечания фото, строка «Проект», тарифы 16000/20000,
  auth/DB/export/deploy не добавлялись.

## Остаточные риски и ограничения

- `StarletteDeprecationWarning` про httpx2 в тестовой среде; тесты не падают.
- Browser evidence относится к встроенному браузеру Orca (desktop/mobile
  viewport) и не доказывает другие движки.
- Денежная точность целорублёвая и соответствует текущим целым тарифам/метрам.
- Push, merge в main, deploy и важное удаление не выполнялись и не разрешены.

## Ресурсы

Все Orca workers этапа остановлены/освобождены; активных helper workers нет.
Посторонние изменения, `.venv` и пользовательские сессии сохранялись.
