# MD-04 evidence — README, скриншоты и документация 1.1.0 (R0)

Дата: 2026-11-12. Исполнитель: OpenCode Flash (Orca dispatch MD-04).
Приёмка: R0 coordinator checklist по доказательствам, без Codex.
**Product verdict: NOT_REVIEWED** (исполнитель не выставляет PASS).

## Baseline, workspace, scope

- Workspace/CWD: `D:\Antigravity\GasProjectCalculator`.
- Ветка: `feature/gsv-mixed-diameters` (не переключалась).
- Baseline HEAD: `d08148c014f66193ad5049f4cdfd427ee0076c52` — MD-03 R2 PASS
  (`build(installer): local 1.1.0 with mixed-GSV app`).
- Изменённый tracked-файл: только `README.md`.
- Новые untracked-файлы: `docs/workflow/evidence/MD-04-evidence.md`,
  `docs/workflow/evidence/logs/MD-04-*`.
- Продуктовый код, tests, frontend, installer, packaging, VISION/ARCHITECTURE/
  ROADMAP/APPROVALS/STATE/HISTORY и прежние отчёты не изменялись.
- Commit/push/merge/deploy/release/signing не выполнялись.

Baseline/status/diff: `logs/MD-04-baseline.txt`, `logs/MD-04-git-status.txt`,
`logs/MD-04-diff-stat.txt`, `logs/MD-04-diff-names.txt`,
`logs/MD-04-readme-diff.txt`.

```text
 README.md | 75 +++++++++++++++++++++++++++++++++++++++++++++++----------------
 1 file changed, 56 insertions(+), 19 deletions(-)
```

## Artifact 1.1.0 (перепроверено)

| Параметр | Значение |
| --- | --- |
| Path | `installer\Output\GasProjectCalculator-Setup-1.1.0.exe` |
| Size | 15 293 993 байт |
| SHA256 | `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710` |

Перепроверка совпала с MD-03 evidence (size и hash). Опубликованный
`installer\Output\GasProjectCalculator-Setup-1.0.0.exe` не изменялся:
size 15 286 980, SHA256
`71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08`.
Log: `logs/MD-04-hash-check.txt`.

## Frozen acceptance checklist

| ID | Результат | Evidence |
| --- | --- | --- |
| T1 | README описывает три длины, единую базу 5 м, списание с самых дешёвых, тарифы 2500/3500/4000 | `logs/MD-04-readback.txt` (все факты True), `logs/MD-04-readme-diff.txt` |
| T2 | Эталонные суммы и combined-пример совпадают с MD-01/MD-03 | `logs/MD-04-numbers-check.txt`; источник — `MD-01-evidence.md` D1–D5/D11, `MD-03-evidence.md` mixed-эталоны/combined |
| T3 | Installer 1.1.0: exact path/size/SHA256; release v1.0.0 не заменяется | `logs/MD-04-hash-check.txt`, README раздел «Скачать и установить» |
| T4 | Новые реальные скриншоты MD-02/MD-03 подключены; относительные ссылки существуют | `logs/MD-04-link-check.txt` (TOTAL_LINKS=18, MISSING_COUNT=0) |
| T5 | Сохранены developer-запуск, три режима, RU install/uninstall, user-file preservation; нет claims о signing/publication/telemetry | `logs/MD-04-readme-diff.txt`, `logs/MD-04-claim-scan.txt` |
| T6 | Изменён только allowlist; hash-факты не выдуманы | `logs/MD-04-diff-names.txt`, `logs/MD-04-git-status.txt`, `logs/MD-04-scope.txt`, `logs/MD-04-hash-check.txt` |

## T1 — readback ключевых фактов

README содержит: три поля «до Ø25 / Ø32–40 / Ø57»; общий метраж как сумма
трёх длин; базовую стоимость один раз на раздел ГСВ; списание пяти базовых
метров «с самых дешёвых труб первыми» в порядке до Ø25 → Ø32–40 → Ø57;
тарифы 2 500 / 3 500 / 4 000 ₽; правило нулевой доплаты при сумме ≤5 м и
базовой стоимости при всех нулях. Полный list — `logs/MD-04-readback.txt`,
diff — `logs/MD-04-readme-diff.txt`.

## T2 — сверка чисел

| Пример | README | MD-01/MD-03 |
| --- | ---: | ---: |
| 4 / 0 / 4 | 12 000 → 72 000 → **75 600** | 75 600 (D1) |
| 2 / 4 / 3 | 15 500 → 75 500 → **79 275** | 79 275 (D2) |
| 0 / 5 / 2 | 8 000 → 68 000 → **71 400** | 71 400 (D3) |
| 3 / 1 / 1 | 0 → 60 000 → **63 000** | 63 000 (D4) |
| 8 / 0 / 0 | 7 500 → 67 500 → **70 875** | 70 875 (D5) |
| Combined | 151 000 + 7 550 → **158 550** | 158 550 (MD-01 D11/MD-03) |

Дополнительно README содержит ГСВ 4/0/4 с районом = **82 950** и ГСН 10 м =
**75 600**, что даёт combined 151 000 / 7 550 / 158 550. Все проверки True:
`logs/MD-04-numbers-check.txt`.

## T3 — installer и release v1.0.0

README указывает точный локальный path, размер 15 293 993 байт и SHA256
`3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710`,
отмечает, что сборка 1.1.0 локальная и не опубликована, а публичный выпуск
v1.0.0 не заменяется. SHA256 и size перевычислены из файла; совпадают с
MD-03. `logs/MD-04-hash-check.txt`.

## T4 — ссылки и скриншоты

Ссылки из README проверены на существование файлов (локальные) и помечены
EXTERNAL (http/https). Итог: 18 ссылок, **0 missing**.
`logs/MD-04-link-check.txt`.

Новые реальные скриншоты MD-03 (установленная 1.1.0, native):

- `docs/screenshots/md-03-native-target-gsv-D1.png` — EXISTS
- `docs/screenshots/md-03-native-target-combined.png` — EXISTS
- `docs/screenshots/md-03-native-target-combined-detail.png` — EXISTS
- `docs/screenshots/md-03-native-target-gsn.png` — EXISTS
- `docs/screenshots/md-03-native-splash.png` — EXISTS
- `docs/screenshots/md-03-wizard-welcome.png` — EXISTS

Новые реальные скриншоты MD-02 (browser mobile 390×844):

- `docs/screenshots/md-02-browser-mobile-390x844-gsv.png` — EXISTS
- `docs/screenshots/md-02-browser-mobile-390x844-combined.png` — EXISTS

Также README сохраняет существующие `frontend/assets/company-emblem.png`,
`docs/images/download-windows.svg`, `packaging/README.md`,
`installer/build-installer.ps1` — все EXISTS.

## T5 — сохранённое поведение и отсутствие claims

README сохраняет: три режима (ГСН, ГСВ, общая смета); developer-запуск
(`venv`, `pip install`, `uvicorn`, unittest); русский мастер установки;
удаление через Параметры Windows; сохранение пользовательских файлов в
Documents, на рабочем столе и журналов в `%LOCALAPPDATA%\GasProjectCalculator`.
Нет заявлений о наличии цифровой подписи, публикации 1.1.0 или телеметрии;
явно указано, что локальный установщик не подписан, а release v1.0.0 не
заменяется. Scan: `logs/MD-04-claim-scan.txt`.

## T6 — scope

`git diff --stat` — только `README.md` (56 вставок, 19 удалений).
`git diff --name-only` — `README.md`. Остальные новые файлы — разрешённые
`docs/workflow/evidence/MD-04-*`. Logs: `logs/MD-04-diff-stat.txt`,
`logs/MD-04-diff-names.txt`, `logs/MD-04-scope.txt`,
`logs/MD-04-git-status.txt`.

## NOT_RUN

- Повторная browser/native/installer-верификация не выполнялась: MD-02/MD-03
  evidence переиспользуется по review-policy; README только цитирует
  существующие факты и подключает уже созданные скриншоты.
- Suite не перезапускался (219 OK зафиксирован в MD-02); изменения только
  документация.
- Commit/push/merge/deploy/release/signing не выполнялись (запрещены TASK).

## Риски / заметки

- README описывает 1.1.0, но публичный download-блок ведёт на прежний
  опубликованный v1.0.0; это явно оговорено, чтобы не создавать ложного
  впечатления о публикации 1.1.0.
- Combined-пример использует район в обоих разделах (ГСН и ГСВ), как в
  утверждённом PLAN и MD-03 evidence.
- Продуктовый PASS не выставляется: требуется R0 coordinator checklist.
