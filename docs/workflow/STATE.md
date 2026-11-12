# Состояние проекта

2026-11-12 — этап «три диаметра ГСВ + artwork»: IN_PROGRESS.
Baseline `9dea625`; ветка `feature/gsv-mixed-diameters`; task-pack commit
`118afa6`. Плановые документы и два пользовательских reference закоммичены
координатором; продуктовый код не менялся. Product verdict NOT_REVIEWED.

Authority: [GSV-MIXED-DIAMETERS-PLAN](GSV-MIXED-DIAMETERS-PLAN.md), VISION/
ARCHITECTURE/ROADMAP, [APPROVALS](APPROVALS.md), MODEL-ROUTING.
Frozen checklists: `docs/workflow/tasks/MD-01..05.md`,
`FINAL-MIXED-STAGE.md`.

| TASK | Risk | Содержание | Исполнитель | Review | Reserve | Статус |
| --- | --- | --- | --- | --- | --- | --- |
| MD-01 | R2 | mixed-формула, API, legacy | OpenCode Flash | Codex sol/high | 1 (≤4/3M) | **PASS** (2 full/1 FAIL/2 calls) |
| MD-02 | R2 | три длины в UI, детализация, artwork | OpenCode Flash | Codex sol/high (vision) | 1 (≤4/3M) | NEXT |
| MD-03 | R2 | installer 1.1.0, installed checks | OpenCode Flash | Codex sol/high | 1 (≤4/3M) | PENDING |
| MD-04 | R0 | README/screenshots/docs | OpenCode Flash | coordinator R0 | 0 | PENDING |
| MD-05 | R0 | интегрированный full suite | OpenCode Flash | coordinator R0 | 0 | PENDING |
| FINAL-MIXED | R3 | stage acceptance | Codex astra/high | — | 1 (≤6/5M) | PENDING |

MD-01: Run `run_8f265b57fb70`; implementer `ctx_f23a43bf4e82`; C1 review
`ctx_1ce9629cc368` FAIL MD01-R1 MAJOR; C2 `ctx_ca7386182b3a`; C2 review
`ctx_b5a2191479fe` **PASS**, finding CLOSED. Review record:
`docs/workflow/reviews/MD-01-review.md`; evidence
`docs/workflow/evidence/MD-01-evidence.md`; suite 216 OK.
Next owner — координатор: scoped commit MD-01, затем dispatch MD-02.

Старые счётчики сохранены: GSV-01..04, WI-01..03, RD-01 1/0/0, RD-02 1/0/1,
RD-03 2/1/2, RD-05 1/0/1, RD-06 2/1/2, RD-07 R0, прежний stage R3 1. Новый
scope не сбрасывает историю/подходы.

Ограничения: `:8000` и root-owned `:8138` сохранять; пользовательскую
установку/сессии не менять; backend — в управляемой Orca service session
(не блокирующий background tool); свои порт/PID/handle документировать.
release v1.0.0 (15 286 980 B, SHA256
`71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08`) не
заменять. Новый installer 1.1.0 — локально. Push/merge/deploy/release/
signing запрещены.

## Ранее принято и опубликовано

main/feature/ss-calculator-redesign `9dea625`; compact 800×540/min 760×520,
3 режима, русский installer/splash, 167 OK. Release v1.0.0 target `e4e4dee`,
SS-Raschet-Setup.exe 15 286 980 B, SHA256 `71232EE4…7E08`.
[Публикация](PUBLICATION-v1.0.0.md),
[компактная версия](FINAL-REPORT-COMPACT-CORRECTION.md),
[разрешения](APPROVALS.md), [история](HISTORY.md),
[инструкции](../../AGENTS.md), [маршруты](MODEL-ROUTING.md).
