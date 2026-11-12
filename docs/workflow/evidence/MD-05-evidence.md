# MD-05 evidence — интегрированная полная проверка финального состояния (R0)

Дата: 2026-11-12. Исполнитель: OpenCode Flash verifier (Orca dispatch MD-05).
Приёмка: R0 coordinator checklist по доказательствам. Codex stage acceptance —
отдельный FINAL-MIXED-STAGE.
**Project verdict: NOT_REVIEWED** — исполнитель не выставляет PASS.

## Workspace, revision, precondition

- CWD: `D:\Antigravity\GasProjectCalculator`.
- Ветка: `feature/gsv-mixed-diameters` (не переключалась).
- HEAD (baseline MD-05, он же MD-04 commit):
  `557fe2d1ed994c3c635ebfb8cfa849d5fd8a4dae`
  (`docs(readme): mixed GSV 1.1.0 usage, benchmarks and local installer (MD-04 R0 PASS)`).
- Stage baseline (последний опубликованный compact HEAD): `9dea625`.
- Precondition MD-01..MD-04 выполнены и закоммичены последовательно:
  `1d77194` MD-01, `fb080aa` MD-02, `d08148c` MD-03, `557fe2d` MD-04.
- Рабочий diff HEAD до начала проверки отсутствовал (clean worktree);
  итоговый `git status` содержит только разрешённые `MD-05-*` evidence/logs.
- Logs: `logs/MD-05-revision.txt`, `logs/MD-05-status.txt`,
  `logs/MD-05-worktree-diff-stat.txt`.

## F1 — baseline/HEAD и интегрированный diff

Команды и CWD: `git rev-parse`, `git log --oneline 9dea625..HEAD`,
`git diff --stat 9dea625..HEAD`, CWD = workspace, exit 0.
Логи: `logs/MD-05-revision.txt`, `logs/MD-05-diff-stat.txt`,
`logs/MD-05-diff-names.txt`.

```text
557fe2d docs(readme): mixed GSV 1.1.0 usage, benchmarks and local installer (MD-04 R0 PASS)
d08148c build(installer): local 1.1.0 with mixed-GSV app (MD-03 R2 PASS)
fb080aa feat(ui): mixed GSV lengths, server billing detail, reference artwork (MD-02 R2 PASS)
1d77194 feat(gsv): mixed three-diameter lengths with legacy-compatible API (MD-01 R2 PASS)
32709a4 docs(workflow): bind mixed-GSV run and MD-01 task
2474243 docs(workflow): record mixed task-pack baseline
118afa6 docs(workflow): freeze mixed-GSV task pack and branch record
```

Интегрированный diff `9dea625..HEAD`: 203 файла, `10980 insertions(+),
153 deletions(-)`. Вся разница распределяется на: stage-планирование
(AGENTS/VISION/ARCHITECTURE/ROADMAP/APPROVALS/STATE/HISTORY, plan/brief,
tasks, references, evidence/reviews) и продуктовый scope MD-01..MD-04 (ниже,
F8). Неожиданных tracked-файлов вне этого состава нет.

## F2 — полный suite ровно один раз

| Параметр | Значение |
| --- | --- |
| Команда | `.\.venv\Scripts\python.exe -m unittest discover -s tests` |
| CWD | `D:\Antigravity\GasProjectCalculator` |
| Exit code | **0** |
| Результат | `Ran 219 tests in 2.159s` — `OK` |
| Время оболочки | 2.808 s |
| Файлы | `logs/MD-05-suite.txt`, `logs/MD-05-suite-exit.txt` |

Полный log: `logs/MD-05-suite.txt`. Suite запускался **один раз** в этой
TASK; перечисление тестов (`logs/MD-05-test-list.txt`) выполнено loader'ом
без запуска тестов. Предупреждение `StarletteDeprecationWarning` о
`httpx`/`testclient` не является ошибкой теста.

## F3 — mixed-тесты и legacy/ГСН регрессия

Test loader без запуска: 219 тестов (`logs/MD-05-test-list.txt`).
Разбивка по модулям: `test_gsv_api` 63, `test_gsv_calculator` 63,
`test_main` 10, `test_calculator` 47, `test_frontend_redesign` 13,
`test_desktop_launcher` 23.

Новые mixed-тесты присутствуют и зелёные:

- `GsvMixedApiTests.test_d1_four_zero_four` … `test_d5_eight_zero_zero`,
  `test_d6_pipe_breakdown_structure`, `test_d7_client_total_is_not_accepted`;
- mixed-валидация: `test_d9_*` (4), `test_d10_*` (7), `test_d14_*` (3),
  `test_c2_*` (7), `test_combined_mixed_and_legacy_mix_in_gsv_is_422`,
  `test_d11_combined_mixed_four_zero_four`;
- `GsvMixedFormulaTests` D1–D6, base/zero-position/bool/negative/unknown-key;
- frontend: `test_gsv_has_three_pipe_length_fields_and_no_legacy_fields`,
  `test_payload_sends_pipe_lengths_instead_of_legacy_fields`,
  `test_breakdown_reads_total_and_pipe_breakdown_from_response`.

Legacy/ГСН регрессия присутствует и зелёная:

- `GsvLegacyCompatTests.test_legacy_breakdown_keys_unchanged`,
  `test_legacy_eight_meters_25_is_70875`, `test_legacy_five_meters_57_is_63000`;
- `test_d12_legacy_combined_still_works`, `test_d14_legacy_*`, `test_d9_*`;
- `test_main.CalculateApiTests.*` (10, включая `POST /calculate` и валидацию);
- `test_calculator.*` (47, ГСН-расчёт без изменений).

Логи: `logs/MD-05-test-categories.txt`, `logs/MD-05-key-tests.txt`,
`logs/MD-05-legacy-tests.txt`, полный suite — `logs/MD-05-suite.txt`.

## F4 — artifact chain installer 1.1.0 и прежние артефакты

Перевычислено `Get-FileHash -Algorithm SHA256` и `Length` по фактическим
файлам; CWD = workspace, exit 0. Log: `logs/MD-05-artifact-hashes.txt`.

| Артефакт | Path | Size | SHA256 | Сверка с MD-03 |
| --- | --- | ---: | --- | --- |
| Installer 1.1.0 | `installer\Output\GasProjectCalculator-Setup-1.1.0.exe` | 15 293 993 | `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710` | совпадает |
| Опубликованный 1.0.0 | `installer\Output\GasProjectCalculator-Setup-1.0.0.exe` | 15 286 980 | `71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08` | не изменён |
| Legacy pre-compact | `installer\Output\legacy\...pre-compact.exe` | 15 273 647 | `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A` | не изменён |
| Legacy previous-stage | `installer\Output\legacy\...previous-stage.exe` | 15 256 037 | `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F` | не изменён |

Size/SHA256 1.1.0 точно совпадают с MD-03 evidence и STATE. Локальный
`1.0.0` — тот же бинарник, что опубликованный release asset v1.0.0
(`PUBLICATION-v1.0.0.md`); удалённый GitHub Release asset в этой TASK не
перекачивался (см. NOT_RUN), bytes локального файла не изменены.

## F5 — screenshots и README-ссылки

- MD-02/MD-03 PNG в `docs/screenshots`: **66 файлов**, все непустые и с
  валидной PNG-сигнатурой `89504E470D0A1A0A` (0 bad):
  `logs/MD-05-png-signatures.txt`. Проверенный список ключевых MD-02/MD-03
  файлов (37) — `logs/MD-05-screenshots.txt`, `MISSING_COUNT=0`.
- README link check: 16 локальных ссылок, **0 missing**; плюс внешние
  `http(s)`-ссылки (GitHub release, сайт) не проверялись сетью.
  Log: `logs/MD-05-readme-links.txt` (включая дубликат gsv-D1 из двух
  вхождений; итог совпадает с MD-04 — 18 извлечённых ссылок, 0 missing).

## F6 — review records и сохранение прежних счётчиков

Файлы записей присутствуют (`logs/MD-05-review-files.txt`):
`MD-01-review.md`, `MD-02-review.md`, `MD-03-review.md`, `MD-04-review.md`
и review packets MD-01/C2/MD-02/MD-03.

| TASK | Verdict / review route | Counters | Evidence |
| --- | --- | --- | --- |
| MD-01 | R2 Codex `gpt-6.1-sol` high; C1 FAIL (MD01-R1 MAJOR) → C2 **PASS**, finding CLOSED | 2 full / 1 FAIL / 2 calls | `reviews/MD-01-review.md`, `MD-01-evidence.md` |
| MD-02 | R2 Codex vision **PASS**, NIT MD02-N1 backlog | 1 full / 0 FAIL / 1 call | `reviews/MD-02-review.md`, `MD-02-evidence.md` |
| MD-03 | R2 Codex **PASS**, no findings | 1 full / 0 FAIL / 1 call | `reviews/MD-03-review.md`, `MD-03-evidence.md` |
| MD-04 | R0 coordinator **PASS** T1–T6, Codex 0 | 0 | `reviews/MD-04-review.md`, `MD-04-evidence.md` |

Readback STATE/HISTORY (`logs/MD-05-review-accounting.txt`): прежние
счётчики сохранены — GSV-01..04, WI-01..03, RD-01 1/0/0, RD-02 1/0/1,
RD-03 2/1/2, RD-05 1/0/1, RD-06 2/1/2, RD-07 R0, прежний stage R3 1;
сброса истории/подходов нет. STATE по-прежнему фиксирует MD-05 как NEXT
(coordinator-owned update после этой проверки). HISTORY содержит записи
MD-01..MD-04 и stage accounting.

## F7 — cleanliness, процессы, порты

- `git status --porcelain --untracked-files=all`: только разрешённые
  `docs/workflow/evidence/logs/MD-05-*` (и этот evidence). Посторонних,
  временных файлов, `.env`, ключей нет — `logs/MD-05-cleanliness.txt`.
- Сканирование tracked-исходников на типичные secret-паттерны:
  `NO_SECRET_PATTERN_HITS` (`logs/MD-05-cleanliness.txt`).
- Запущенных test-процессов (`unittest`/`pytest`) нет. Найденные python —
  только два защищённых uvicorn-сервера:
  `:8000` (listener PID 12888, parent 12424) и `:8138` (listener PID 23152,
  parent 20204); оба живы и не трогались —
  `logs/MD-05-processes-ports.txt`, `logs/MD-05-python-processes.txt`.
- Пользовательские установка/сессии не изменялись; серверы не
  перезапускались, порты не освобождались.

## F8 — diff map продуктового scope

Интегрированный продуктовый diff `9dea625..HEAD` — 7 файлов,
`1266 insertions(+), 105 deletions(-)` (`logs/MD-05-product-diff.txt`):

| TASK | Files | Ожидание |
| --- | --- | --- |
| MD-01 | `app/gsv_calculator.py` (+106), `app/main.py` (+90/−24), `tests/test_gsv_api.py` (+349), `tests/test_gsv_calculator.py` (+169) | mixed-формула/API/legacy |
| MD-02 | `frontend/index.html` (+570/−…), `tests/test_frontend_redesign.py` (+59/−…) | три длины UI, детализация, artwork |
| MD-03 | `installer/GasProjectCalculator.iss` (+2/−2) | AppVersion 1.1.0 / VersionInfo 1.1.0.0 |
| MD-04 | `README.md` | документация/скриншоты/installer facts |

Per-commit карта: `logs/MD-05-diff-map.txt`. `app/calculator.py` —
zero-diff; `requirements.txt`/`requirements-dev.txt` — zero-diff;
`app/`, `frontend/`, `tests/`, `installer`, `packaging` не содержат
изменений вне перечисленного. Stage-документация
(VISION/ARCHITECTURE/ROADMAP/AGENTS/APPROVALS/STATE/HISTORY, plan/brief,
tasks, design references) входит в утверждённый этап 2026-11-12.

## Frozen acceptance checklist (наблюдения, не project PASS)

| ID | Наблюдение | Evidence |
| --- | --- | --- |
| F1 | Baseline/HEAD зафиксированы; diff соответствует ожидаемому составу | `MD-05-revision.txt`, `MD-05-diff-stat.txt`, `MD-05-diff-names.txt` |
| F2 | Full suite ровно один раз, exit 0, `Ran 219 tests`, `OK` | `MD-05-suite.txt`, `MD-05-suite-exit.txt` |
| F3 | Mixed D1–D14/C2 и legacy/ГСН тесты присутствуют и зелёные | `MD-05-test-list.txt`, `MD-05-test-categories.txt`, suite log |
| F4 | Installer 1.1.0 size/SHA256 совпадают с MD-03; 1.0.0/legacy не изменены | `MD-05-artifact-hashes.txt` |
| F5 | MD-02/MD-03 screenshots существуют/непустые; README 0 missing | `MD-05-screenshots.txt`, `MD-05-png-signatures.txt`, `MD-05-readme-links.txt` |
| F6 | Review records MD-01..MD-04 и счётчики сохранены | `MD-05-review-files.txt`, `MD-05-review-accounting.txt` |
| F7 | Нет посторонних/секретов/test-процессов; `:8000`/`:8138` целы | `MD-05-cleanliness.txt`, `MD-05-processes-ports.txt` |
| F8 | Продуктовый diff соответствует MD-01/02/03; requirements/calculator zero-diff | `MD-05-product-diff.txt`, `MD-05-diff-map.txt` |

## NOT_RUN

- Полный suite повторно не запускался (ровно один прогон по TASK).
- Remote GitHub Release v1.0.0 asset/SHA256SUMS не перекачивались и не
  сверялись по сети; локальный published-бинарник 1.0.0 не изменён.
- Browser/native/installer build/install/runtime проверки не повторялись:
  MD-02/MD-03 evidence переиспользуется по review-policy.
- Commit/push/merge/deploy/release/signing и продуктовые/документационные
  правки не выполнялись (кроме разрешённого MD-05 evidence/logs).

## Риски / заметки

- Открытый NIT MD02-N1 (верх золотистого вентиля слегка обрезан viewBox)
  остаётся backlog по решению MD-02 review; на расчёт/приёмку не влияет.
- Installer 1.1.0 не подписан, SmartScreen может предупредить; это
  ожидаемое локальное состояние 1.1.0, release v1.0.0 не заменялся.
- Проверка remote Release asset и будущий FINAL-MIXED-STAGE Codex review —
  вне scope MD-05.
