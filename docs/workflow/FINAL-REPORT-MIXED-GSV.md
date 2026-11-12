# FINAL REPORT — смешанные диаметры ГСВ и новое оформление (1.1.0)

Дата: 2026-11-12. Этап: три длины ГСВ (`up_to_25` / `from_32_to_40` /
`diameter_57`), серверная детализация, верхнее/нижнее artwork по двум
пользовательским образцам, локальный Windows installer 1.1.0.

- **Статус: COMPLETE.** Все TASK и независимая финальная Codex R3 acceptance —
  **PASS**.
- Ветка: `feature/gsv-mixed-diameters` (создана от baseline `9dea625`).
- Продуктовый revision: `557fe2d`; verification/accounting commit `0431c0b`;
  финальный docs-only commit — HEAD ветки при передаче.
- Утверждение: `docs/workflow/APPROVALS.md` (раздел «Этап трёх диаметров…»),
  `GSV-MIXED-DIAMETERS-PLAN.md`, дополнения VISION/ARCHITECTURE/ROADMAP.

## Итог по scope

1. **Формула и API (MD-01, R2).** Добавлены три длины `pipe_lengths` с
   строгими integer ≥ 0 без bool; сервер вычисляет общий метраж, включённые и
   оплачиваемые метры, одну базу 5 м с вычитанием из самых дешёвых труб
   (`up_to_25 → from_32_to_40 → diameter_57`). Тот же модуль используется в
   `/calculate/gsv` и nested `gsv` `/calculate/combined`. Legacy
   `length`/`diameter` request+response сохранены без breaking changes;
   смешение форм, неполная пара и explicit `null` дают 422.
   `POST /calculate` (ГСН) не изменён.
2. **UI, детализация и artwork (MD-02, R2).** В ГСВ и combined добавлены три
   поля длин, общий метраж и таблица `length/included/billable/rate/surcharge`
   из серверного `pipe_breakdown`; суммы клиентом не пересчитываются. Верх и
   низ оформлены inline-SVG по `header-detail-reference.jpg` и
   `footer-detail-reference.jpg` (объёмная труба/муфты/золотой вентиль;
   труба/пламя/дом с тёплым окном). Сохранены `СС.Расчет`, круглая эмблема и
   окно 800×540 / min 760×520.
3. **Installer 1.1.0 (MD-03, R2).** Собран локальный x64 installer с
   FileVersion `1.1.0.0`/ProductVersion `1.1.0` и сохранённым AppId.
   Установленная программа проверена без Python/CLI: mixed-эталоны,
   combined, legacy/422, ГСН/САКЗ/ПК/район/НДС, splash/readiness,
   loopback/занятый порт, закрытие без дочерних процессов, русский wizard,
   reinstall/uninstall с сохранением пользовательских файлов. Пользовательская
   установка и её PID не затрагивались.
4. **Документация (MD-04, R0) и интегрированная проверка (MD-05, R0).**
   README обновлён под 1.1.0 с формулой, тарифами, эталонами, installer
   path/size/SHA256 и реальными скриншотами. Полный suite прогнан один раз на
   интегрированном состоянии: **219 tests OK, exit 0**.

## Эталоны (подтверждены API и установленной версией)

| до Ø25 / Ø32–40 / Ø57, м | Длина | Доплата | Подытог | Итог с НДС 5% |
| --- | ---: | ---: | ---: | ---: |
| 4 / 0 / 4 | 8 | 12 000 | 72 000 | **75 600** |
| 2 / 4 / 3 | 9 | 15 500 | 75 500 | **79 275** |
| 0 / 5 / 2 | 7 | 8 000 | 68 000 | **71 400** |
| 3 / 1 / 1 | 5 | 0 | 60 000 | **63 000** |
| 8 / 0 / 0 | 8 | 7 500 | 67 500 | **70 875** |

Общая смета (частник, район): ГСН 10 м — 75 600 ₽ с НДС; ГСВ 4/0/4 —
82 950 ₽ с НДС; подытог **151 000 ₽**, НДС **7 550 ₽**, итог **158 550 ₽**.

## Артефакт

- **Installer 1.1.0 (локально, git-ignored):**
  `installer/Output/GasProjectCalculator-Setup-1.1.0.exe`
- Размер: **15 293 993 байт**
- SHA256: `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710`
- Authenticode: NotSigned (локальная сборка; SmartScreen может предупредить).
- Packaged/installed exe: `F374EEED2535BBDDD024AEBFA8B562642A010F28804C7BEB4A0755C53F459690`.
- **Не изменены:** опубликованный v1.0.0 (15 286 980 B, SHA256
  `71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08`) и
  legacy artifacts `04388410…949A` / `2973278F…2428F`. Release v1.0.0 не
  заменялся; новая публикация в этот execution packet не входила.

## Приёмка и счётчики

| TASK | Risk | Вердикт | Reviews / Codex calls |
| --- | --- | --- | --- |
| MD-01 | R2 | PASS (C2; MD01-R1 CLOSED) | 2 full / 1 FAIL / 2 calls |
| MD-02 | R2 | PASS (vision) | 1 full / 0 FAIL / 1 call; NIT MD02-N1 |
| MD-03 | R2 | PASS | 1 full / 0 FAIL / 1 call |
| MD-04 | R0 | PASS | coordinator; 0 Codex |
| MD-05 | R0 | PASS | coordinator; 0 Codex |
| FINAL-MIXED | R3 | **PASS** | Codex `gpt-6-astra` high; 1 call |

Прежние счётчики сохранены: GSV-01..04, WI-01..03, RD-01 1/0/0,
RD-02 1/0/1, RD-03 2/1/2, RD-05 1/0/1, RD-06 2/1/2, RD-07 R0, прежний
stage R3 1. Rename/new session не сбрасывали бюджеты.

## Findings и остаточные ограничения

- **MD02-N1 (NIT, backlog):** верх золотистого маховика вентиля слегка обрезан
  SVG viewBox; обязательные элементы artwork различимы, на расчёт/приёмку не
  влияет.
- **FINALMD-N1 (MINOR, editorial):** устаревшие формулировки STATE и счётчики
  скриншотов в review packet (36/35 вместо 33+33=66). Исправлено при
  финализации; новый цикл ревью не требовался.
- Installer неподписан; SmartScreen может предупредить. Проверка выполнена в
  одной среде Windows x64 / WebView2 / DPI 96. Remote Release asset v1.0.0 в
  MD-05 повторно не скачивался; локальные bytes не изменены.
- В combined детализация может прокручиваться внутри карточки на минимальном
  размере; итог и кнопка остаются видимыми, page-level overflow отсутствует.

## Границы

Push, merge в main, deployment, GitHub Release, signing и замена release
v1.0.0 не выполнялись. Пользовательская установка, её сессия, `:8000` и
root-owned `:8138` не затрагивались. Локальный installer 1.1.0 передан как
проверенный артефакт; решение о публикации — за пользователем.

## Evidence

- `docs/workflow/evidence/MD-01-evidence.md` … `MD-05-evidence.md` + logs.
- `docs/workflow/reviews/MD-01..05-review.md`,
  `FINAL-MIXED-STAGE-review.md` + packets.
- 66 реальных PNG: `docs/screenshots/md-02-*`, `docs/screenshots/md-03-*`.
- Suite log: `docs/workflow/evidence/logs/MD-05-suite.txt` (`219 tests`, OK).
- `docs/workflow/HISTORY.md`, `docs/workflow/STATE.md`.
