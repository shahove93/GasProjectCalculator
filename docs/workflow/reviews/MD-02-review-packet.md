# MD-02 R2 review packet (Codex gpt-6.1-sol high, vision)

## Task

- Project TASK: **MD-02** — три длины в UI, серверная детализация и artwork по
  двум образцам.
- Risk **R2**; approach/cycle **A1/C1**; reviewer — independent Codex
  `gpt-6.1-sol` high with vision (OpenCode Pro has no image input).
- Baseline: `1d77194d777963214e83bb2ad63bcf0b431b5485`;
  branch `feature/gsv-mixed-diameters`. Submission — uncommitted working tree;
  reviewer files не меняет и не коммитит.
- Perimeter: `frontend/index.html`, `tests/test_frontend_redesign.py`,
  `docs/screenshots/md-02-*`, `docs/workflow/evidence/MD-02-*`,
  `docs/workflow/evidence/logs/MD-02-*`. Coordinator-owned documents не
  считать продуктовым diff.

## Frozen checklist (verbatim `docs/workflow/tasks/MD-02.md`)

| ID | Criterion |
| --- | --- |
| U1 | В ГСВ и combined три поля `до Ø25`, `Ø32–40`, `Ø57`; старые length/diameter в UI отсутствуют |
| U2 | Payload содержит `pipe_lengths` с тремя ключами; старые поля не отправляются |
| U3 | Показан общий метраж и по каждой позиции length/included/billable/rate/surcharge из серверного ответа |
| U4 | Суммы D1–D5: 75600, 79275, 71400, 63000, 70875 |
| U5 | САКЗ/ПК, район, НДС корректны; ПК disabled/сброшен при 0 САКЗ |
| U6 | 422 видима, смена режима очищает устаревший результат |
| U7 | Верх по header-reference: объёмная труба, муфты, золотой вентиль, свечение, тёмно-синий фон |
| U8 | Низ по footer-reference: труба, голубое пламя, дом с тёплым окном, пейзаж |
| U9 | `СС.Расчет` и круглая эмблема сохранены; внешних ресурсов нет |
| U10 | Native 800×540 / min 760×520; action+итог видимы при scrollY=0; нет page h/v scroll/workaround |
| U11 | Mobile 390×844 без horizontal overflow; действие/итог доступны |
| U12 | Все три режима, ГСН без регрессии; full suite зелёный; diff в allowlist |

## Evidence supplied

- `docs/workflow/evidence/MD-02-evidence.md` — baseline/diff, commands/CWD/exit,
  process/port ownership, browser+native measurements, U1–U12, NOT_RUN.
- `docs/workflow/evidence/logs/MD-02-*` — browser/native JSON+summary, suite,
  scope, uvicorn/launcher logs, port ownership.
- Screenshots: `docs/screenshots/md-02-*` (36 real PNG:
  desktop browser D1–D5/combined/422/switch, native target/min all modes,
  mobile 390 all modes, header/footer side-by-side comparisons).
- References: `docs/design/header-detail-reference.jpg` (1021×194),
  `docs/design/footer-detail-reference.jpg` (1021×177).
- Product diff: `git diff 1d77194 -- frontend/index.html
  tests/test_frontend_redesign.py`.

## Review instructions

1. Inspect the actual final diff and evidence; confirm no unexpected files and
   that only allowlist product files changed.
2. **Vision is mandatory:** open the two reference JPEGs and the comparison
   PNGs `md-02-compare-header.png` / `md-02-compare-footer.png`, plus native
   target/min and mobile screenshots. Judge whether the implementation visibly
   matches the requested volumetric glowing pipe + gold valve (top) and
   pipe/flame/house/warm window (bottom), while keeping `СС.Расчет`, emblem and
   compact layout.
3. Verify U1–U12 against code/measurements; with complete, unambiguous evidence
   do not rerun commands (reuse rule). One bounded read-only probe is allowed
   only if evidence is missing/ambiguous.
4. Confirm no screenshot-only overflow masking (`zoom`/`scale`/hidden page
   overflow workaround) and that action+total are genuinely visible in the
   native viewport at `scrollY=0`.
5. Report findings with ID/criterion/location/observed/expected/severity/
   closure evidence. MINOR/NIT do not fail. Do not modify files or commit.
6. Return exactly one verdict: **PASS**, **FAIL** (BLOCKER/MAJOR) or
   **BLOCKED**; end your turn after the verdict.
