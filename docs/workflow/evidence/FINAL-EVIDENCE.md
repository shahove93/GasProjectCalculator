# Final evidence — этап ГСВ

## Идентификация

- Утверждённый этап: VISION, ARCHITECTURE, ROADMAP; APPROVALS.md (SHA256).
- Stage baseline: `2949223` (`main`). Ветка: `feature/gsv`.
- Последний продуктовый commit: `8d2d215` (UI regression). API regression —
  `0cd48bc`; API — `dab59a9`, модуль ГСВ — `501a32b`, UI — `9dc84e0`,
  workflow — `1b533ac`. README/evidence — docs-only коммиты, продуктовый код
  не меняют.
- Workspace: `D:/Antigravity/GasProjectCalculator`.
- Модели: координатор/исполнители `deepseek/deepseek-flash`; R1
  `deepseek/deepseek-v4-pro`; R2 `gpt-6.1-sol` high; финал `gpt-6-astra` high.

## TASK, маршруты и вердикты

| TASK | Риск | Приёмка | Вердикт | Доказательство |
| --- | --- | --- | --- | --- |
| GSV-01 модуль ГСВ | R1 | OpenCode Pro `ctx_6f8faa93b48a` | PASS, 0 findings | `GSV-01-evidence.md`, 48 unit / 105 suite OK |
| GSV-02 API | R2 | Codex `ctx_a52e8c040396` C1 | FAIL (MAJOR evidence/baseline) | `GSV-02-evidence.md` |
| GSV-02 API | R2 | Codex `ctx_ed2dda90c5c1` C2 | PASS, B1–B11 | 26 API / 131 suite OK |
| GSV-03 UI | R1 | OpenCode Pro `ctx_d7c8f160505f` | PASS, 1 NIT backlog | `GSV-03-browser.md`, 6 screenshots |
| GSV-02 regression | R2 | Codex `ctx_ddd46cfbef19` | PASS, D1–D6 | `GSV-02-regression-evidence.md` |
| GSV-03 regression | R1 | OpenCode Pro `ctx_faa3f1ff8d22` | PASS, 0 findings | `GSV-03-regression.md` |
| FINAL R3 call 1 | R3 | Codex `ctx_a35b269f1f44` | FAIL: 4 MAJOR + NIT | findings исправлены |
| FINAL R3 call 2 | R3 | Codex gpt-6-astra high | ожидается | этот пакет |

Codex calls: GSV-02 — 3 (1 FAIL + 2 PASS); финальная приёмка — 1 FAIL + 1
повторная (в пределах R2 ≤4 и R3 ≤6).

## Фактические проверки (reuse, без повторного прогона)

- Полный suite (актуальное состояние): `.\.venv\Scripts\python.exe -m unittest
  discover -s tests`, CWD `D:/Antigravity/GasProjectCalculator`, exit 0,
  `Ran 134 tests ... OK` (`GSV-02-regression-evidence.md`,
  `GSV-03-regression.md`). Прежний прогон 131 OK сохранён в
  `logs/GSV-02-suite.txt`.
- API: 29 тестов `/calculate/gsv` и `/calculate/combined` (включая response
  models/OpenAPI), exit 0. Лог: `logs/GSV-02R-api.txt`; прежний 26 OK —
  `logs/GSV-02-api.txt`.
- GSV unit: 48 тестов, exit 0. Лог: `logs/GSV-01-unit.txt`.
- Browser (Orca built-in): desktop ГСН 105000/5250/110250; ГСВ
  100500/5025/105525; combined ГСН 75600, ГСВ 70350, 139000/6950/145950;
  mobile 390×844, `scrollWidth <= innerWidth`; ПК при САКЗ 0/1/0; ошибка
  diameter 58. Скриншоты: `docs/screenshots/gsv-03-*.png`.
- Browser regression: начальная загрузка только ГСН; отложенный ответ ГСН после
  переключения в ГСВ игнорируется; скрытый diameter=58 не блокирует ГСН submit;
  mobile fits=true. `docs/screenshots/gsv-03-initial-gsn.png`,
  `gsv-03-race-guard.png`, `gsv-03-hidden-validation.png`, `gsv-03-mobile.png`.
- Продуктовый код после проверок не менялся (README/evidence — docs-only).

## Отклонения и риски

- GSV-02 C1 FAIL был административным (неверный baseline и незакоммиченные
  координаторские evidence-файлы), не дефект продукта; C2 PASS.
- GSV-03 первая попытка зависла после изменения UI; координатор остановил её,
  продолжил логический TASK (`ctx_513a316e9b89`), код проверен и принят R1.
- Финальная приёмка call 1 вернула FAIL с 4 MAJOR: UI initial mode, stale
  response, hidden validation; отсутствие утверждённых response models. Все
  исправлены и повторно приняты R2/R1; NIT по суффиксу «ГСВ» также исправлен.
  Повторная финальная приёмка — call 2.
- Вне scope: нижние примечания фото, строка «Проект», auth/DB/export/deploy.

## Ресурсы

Все Orca workers этого этапа остановлены/освобождены; активных helper workers
нет. Push/merge/deploy не выполнялись.
