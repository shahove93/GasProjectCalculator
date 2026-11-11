# RD-FINAL-VERIFY — R0 acceptance (координатор)

- Логический TASK: RD-FINAL-VERIFY (R0). Verifier: OpenCode Flash
  `ctx_1cb546ad517e` (`task_e08ed7f8ac7b`).
- Фактический HEAD при проверке `8c87e44` (dispatch target `c72979a`;
  разница — только координаторский docs-коммит, продуктовое дерево идентично).
- Проверено read-only; верifier изменил только `RD-FINAL-evidence.md`/logs.
- R0: автоматическая проверка frozen checklist координатором; Codex не
  привлекался.

## Вердикт: PASS

| ID | Результат | Проверка |
| --- | --- | --- |
| RF-1 | PASS | `git diff --stat e24d806..HEAD` = 111 files, +8156/−255; scope RD-01..RD-04 + workflow docs; неожиданных файлов нет. |
| RF-2 | PASS | один прогон `.\.venv\Scripts\python.exe -m unittest discover -s tests`, CWD workspace, `Ran 163 tests ... OK`, exit 0. |
| RF-3 | PASS | artifact 15 273 647 bytes, SHA256 `043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`, совпадает с README/RD-03; git-ignored. |
| RF-4 | PASS | 26 `rd-*.png` непустые (`ZERO_SIZE_COUNT=0`), evidence/reviews непустые. |
| RF-5 | PASS | reuse RD-02/RD-03 + spot check: title `СС.Расчет`, 1050×740/min 860×620, subtitle, Inno AppName/Start Menu/optional Desktop. |
| RF-6 | PASS | reuse RD-01 (browser) и RD-03 (installed runtime): 131250/105525/145950. |
| RF-7 | PASS | reuse RD-02: file-only/no network, reduced motion, splash→ready→main. |
| RF-8 | PASS | reuse RD-03: RU wizard/error/uninstaller, reinstall exit 0, user markers сохранены. |
| RF-9 | PASS | diff `app/main.py`/calculators/`requirements.txt`/calculation-тесты пуст; suite 163 OK. |
| RF-10 | PASS | untracked только RD-FINAL logs; добавленные binary — только задекларированные PNG; `SUSPICIOUS_COUNT=0`, `SECRET_HIT_COUNT=0`. |

## Примечания

- Расхождение HEAD `c72979a`→`8c87e44` — docs-only, задокументировано; suite и
  проверки относятся к `8c87e44`, продукт идентичен.
- Повторно выполнен только один полный suite и read-only file/hash/diff
  проверки; runtime/installer/browser переиспользованы по review-policy.
- NOT_RUN: browser/installer/splash runtime, rebuild, signing/push/merge/deploy.
- Счётчики: R0, Codex calls 0.
