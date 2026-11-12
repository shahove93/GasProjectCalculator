# Публикация СС.Расчет 1.2.0 — COMPLETE

2026-11-12. Механическая публикация R0 по явному разрешению пользователя
«Но все можно комитить и выкладывать на гитхаб» (записано в APPROVALS).
Публикуются принятые bytes installer 1.2.0 без rebuild; продуктовый код,
suite, installer, UI и screenshots не перезапускались. Новый Codex review
не выполнялся.

## Источник и артефакт

- Принятый этап: `FINAL-REPORT-VISUAL-POLISH.md`; VP-01/VP-02 R2 и отдельная
  финальная Sol/high приёмка PASS.
- Source HEAD до публикации:
  `73ec3acb79cb6e0ba5931afc1fd31688d75d9ea2` (feature/gsv-mixed-diameters,
  ahead 4).
- Publication commit/tag target:
  `2ba4fb032789f8944c355a7731a9ddf14aeb56dc`; к принятому состоянию добавлены
  только README, release notes, checksum, APPROVALS и HISTORY.
- Installer: `installer/Output/GasProjectCalculator-Setup-1.2.0.exe`,
  15 373 267 B, SHA256
  `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113`.
  Локальный artifact сохранён.

## Git

- `git push origin feature/gsv-mixed-diameters`: `ac59d8c..2ba4fb0`,
  exit 0; обычный push, без force.
- `git push origin v1.2.0`: новый тег, exit 0.
- Tag v1.2.0 (annotated `9253c5d1…`) → commit
  `2ba4fb032789f8944c355a7731a9ddf14aeb56dc`.
- `origin/main` был `ac59d8c` — предок HEAD, divergence отсутствовала;
  fast-forward выполнен после финального docs-commit (см. HISTORY), без merge
  commit, force или перезаписи чужих изменений.

## GitHub Release

- Release id **443454221**, tag **v1.2.0**, draft=false, prerelease=false,
  **Latest** (`releases/latest` → v1.2.0), name
  «СС.Расчет 1.2.0 — Windows».
- URL: https://github.com/shahove93/GasProjectCalculator/releases/tag/v1.2.0
- Asset `SS-Raschet-Setup.exe`, id **740919104**, size **15 373 267 B**,
  server digest
  `sha256:4579fb3aa7b2e6220c1204e3aa2a6048648ae5a344b8e2d45dd00cf19f856113`.
- Asset `SHA256SUMS.txt`, id **740924696**, size **87 B**, server digest
  `sha256:8e38fe2b929876daed98e6e5996aa2e4399c42e563dbbaaf0e33def225c76a6c`.
- Прямая ссылка на installer:
  https://github.com/shahove93/GasProjectCalculator/releases/download/v1.2.0/SS-Raschet-Setup.exe
  (`releases/latest/download/SS-Raschet-Setup.exe` также ведёт на v1.2.0).

## Публичная проверка без credentials

- `releases/download/v1.2.0/SS-Raschet-Setup.exe`: HTTP 200,
  15 373 267 B, скачанный SHA256
  `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113` —
  совпал с принятой сборкой.
- `releases/download/v1.2.0/SHA256SUMS.txt`: HTTP 200, 87 B, содержимое
  `4579fb3a…f856113  SS-Raschet-Setup.exe`.
- `releases/latest/download/SS-Raschet-Setup.exe`: HTTP 200,
  Content-Length 15 373 267.

## Сохранение прежних выпусков

Release v1.0.0 (id 442532779) и v1.1.0 (id 442672288), их tag и assets не
изменялись; server digests прежних installer совпадают с ранее
опубликованными. Пользовательская установка/данные/сессии, `.venv`,
посторонние изменения, глобальные конфиги и аккаунты не трогались.

## Ограничения

- Установщик не подписан; Authenticode/SmartScreen остаются как раньше.
- Проверка выполнена в одной Windows/WebView2/DPI96 среде (перенесённое
  ограничение приёмки; suite/build не повторялись).
- Web deployment, signing, force/delete, замена существующих tag/asset и
  изменение v1.0.0/v1.1.0 не выполнялись.

Токен/credentials не выводились и не записывались в файлы; использован
существующий Git credential helper и GitHub REST API. GitHub CLI не был
авторизован.
