# FINAL-MIXED-STAGE — итоговая приёмка этапа смешанных диаметров (R3)

## Authority

Утверждённый этап 2026-11-12: `AGENTS.md`, `VISION.md` (дополнение
«смешанные диаметры»), `ARCHITECTURE.md` (соответствующие дополнения),
`ROADMAP.md` (раздел «Этап 2026-11-12 — три диаметра…»),
`docs/workflow/APPROVALS.md` (раздел «Этап трёх диаметров…»),
`docs/workflow/GSV-MIXED-DIAMETERS-PLAN.md`. Reviewer — независимый Codex
`gpt-6-astra` high; coordinator не выставляет PASS за reviewer.

## Precondition

MD-01..MD-05 приняты routed PASS; их review records и evidence pack
существуют; интегрированное состояние финально закоммичено координатором.
Reviewer файлов не меняет, команд не перезапускает при полном evidence
(review-policy reuse rule); только читает diff/evidence/артефакты.

## Scope

Проверить delivered behavior против утверждённых VISION/ARCHITECTURE/ROADMAP/
APPROVALS:

1. Три длины `up_to_25`/`from_32_to_40`/`diameter_57`, строгие integer ≥ 0 без
   bool, серверная сумма, одна база 5 м с вычитанием из самых дешёвых первыми.
2. Единый модуль в `/calculate/gsv` и `combined.gsv`; legacy length/diameter
   request+response без breaking changes; смешение/неполнота → 422.
3. UI в ГСВ и combined: три поля, общий метраж, детализация, тарифы
   2500/3500/4000; artwork по двум refs; `СС.Расчет`/эмблема/компактность;
   реальные screenshots/визуальное сравнение; отсутствие overflow-workaround.
4. Installer 1.1.0 собран/проверен; release v1.0.0 и старые artifact bytes
   сохранены; mixed/ГСН/САКЗ/ПК/НДС/lifecycle/RU wizard/reinstall/uninstall.
5. README/docs/скриншоты соответствуют фактам; полный suite один раз зелёный.

## Frozen acceptance criteria (evidence-based)

| ID | Criterion |
| --- | --- |
| A1 | Все эталоны PLAN (75600/79275/71400/63000/70875; combined 151000/7550/158550) подтверждены в коде/API/установленной версии |
| A2 | Формула cheapest-first и единственная база 5 м реализованы без клиентского total |
| A3 | Legacy API/response и ГСН не сломаны; конфликт форм 422; strict validation |
| A4 | UI трёх режимов, три длины и детализация работают; artwork соответствует обоим refs |
| A5 | Native 800×540/min 760×520 и mobile 390 без скрытого overflow; action+итог видимы |
| A6 | Installer 1.1.0 и установленная программа проверены; release/legacy bytes сохранены |
| A7 | README/evidence/review records согласованы; suite зелёный |
| A8 | Счётчики: старые RD/GSV/WI не сброшены; новые MD-01..MD-05 в пределах резервов |
| A9 | Нет несанкционированных push/merge/deploy/release/signing; scope соблюдён |

## Accounting to verify

Старые логические TASK сохраняют историю: GSV-01..04, WI-01..03, RD-01
(1 full/0 FAIL/0 Codex), RD-02 (1/0/1), RD-03 (2/1/2), RD-05 (1/0/1),
RD-06 (2/1/2), RD-07 R0, прежние stage R3. Новые резервы: MD-01 R2 ≤4/3M,
MD-02 R2 ≤4/3M, MD-03 R2 ≤4/3M, MD-04/MD-05 R0, FINAL-MIXED R3 ≤1 вызов из
≤6/5M. Rename/new session не сбрасывает бюджеты.

## Verdict

Вернуть ровно один из: **PASS** (все criteria доказаны), **FAIL**
(BLOCKER/MAJOR с finding IDs), **BLOCKED** (недоступный prerequisite/
непроверяемое evidence). Findings вне frozen checklist — backlog, не
расширяют review. Файлов не менять; после вердикта завершить turn.
