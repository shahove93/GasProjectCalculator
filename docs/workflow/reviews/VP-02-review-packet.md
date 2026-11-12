# VP-02 R2 review packet — installer 1.2.0 (logical MD-03 / A2 / C1)

2026-11-12. Пакет для **независимого** R2 reviewer: отдельный настоящий Orca
Codex **`gpt-6.1-sol`, effort `high`**. Reviewer работает read-only: не меняет
файлы, не пересобирает installer, не делает commit/push, не запускает
дорогие проверки повторно без доказанного пробела. Исполнитель себя не
принимает.

## Идентификация

- Workspace `D:/Antigravity/GasProjectCalculator`, ветка
  `feature/gsv-mixed-diameters`, baseline/HEAD
  `1689773718c818a4ebca400afc2d8a4206b6458e` (принятый VP-01 / MD-02 A2).
- Logical TASK **MD-03**, подход **A2**, цикл **C1**. A1/C1 ранее PASS
  (1 full review, 0 FAIL, 1/4 Codex calls); это зарезервированный второй
  вызов, счётчики не сбрасываются. Оба прежних provider limit — инфраструктура,
  не product FAIL и не verdict.
- Утверждённый scope: `docs/workflow/VISUAL-POLISH-ASTRA-BRIEF.md`,
  `docs/workflow/APPROVALS.md` (раздел Astra/1.2.0 и Lean finish),
  `docs/workflow/tasks/VP-02.md`. Новый local installer **1.2.0**; публикации
  нет. Push/merge/deploy/release/signing запрещены.
- Модель reviewer проверяется координатором по Orca receipt/worker-show:
  `agent=codex`, `model=gpt-6.1-sol`, `effort=high`.

## Замороженный checklist

Чек-лист **W1–W11** из `docs/workflow/tasks/VP-02.md` не меняется. Reviewer
обязан дать verdict по каждому пункту с указанием фактического evidence и
наблюдаемого результата; нельзя расширять checklist во время review.

## Что проверять (bounded packet)

1. **Actual diff и allowlist.** `git diff --stat`/`git diff` относительно
   baseline; product diff сохранён в
   `docs/workflow/evidence/logs/VP-02-resumed-product.diff`. Ожидается только
   `installer/GasProjectCalculator.iss` (version/branding),
   `installer/build-installer.ps1` (version-specific output guard) и новые
   `installer/assets/**`; `app/`, `frontend/`, `packaging/`, `requirements*`,
   `tests/` — zero-diff относительно HEAD. Проверить отсутствие неожиданных
   product files. Координаторские docs/evidence/screenshots — отдельно.
2. **W1–W3, W11 — артефакт.** `installer/Output/GasProjectCalculator-Setup-1.2.0.exe`:
   15 373 267 B, FileVersion `1.2.0.0`, ProductVersion `1.2.0`, SHA256
   `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113`.
   Прежние 1.0.0/1.1.0/legacy bytes и remote releases не изменены; pre/post
   hashes и manifest — `docs/workflow/evidence/logs/VP-02-resumed-manifest.json`,
   `VP-02-old-artifacts-before.json`, `VP-02-resumed-preflight.json`.
   Никаких push/merge/deploy/release операций.
3. **W4 — реальный RU wizard.** Смотреть PNG с vision:
   `docs/screenshots/visual-02-wizard-welcome.png`,
   `-dir`, `-tasks`, `-ready`, `-installing`, `-finish` (598×464). Проверить
   фирменную боковую/верхнюю графику, русские подписи/кнопки, контраст,
   отсутствие перекрытия controls, стандартный Inno Setup 6.4.1, RU-only,
   прежний AppId, Desktop task по умолчанию выключен. Согласованность мотива с
   заставкой (`docs/design/splash-installer-reference.jpg`) — по фактическим
   изображениям, не по тексту. Детали: `VP-02-evidence.md`, W4.
4. **W5, W9 — изоляция и сохранение данных.** `VP-02-resumed-cycle.txt`/`.ps1`
   и raw-логи: install 1.1.0 → upgrade 1.2.0 → reinstall → uninstall, numeric
   exits 0; HKCU uninstall key/оба ярлыка exact restore; 106 пользовательских
   files/37 372 847 B unchanged; sentinel user files остались; изолированный
   каталог только в Temp; обычная установка не изменена.
5. **W6–W8 — installed app, размеры, lifecycle.** `VP-02-resumed-native-ui.json`,
   `VP-02-resumed-launch.json`, `VP-02-resumed-close-final.json`,
   `VP-02-resumed-error-*.json`, native screenshots:
   `visual-02-native-splash.png`, `visual-02-resumed-native-target-*`,
   `-minimum-*`, `-native-startup-error.png`, `-splash-os/flag/animated.png`.
   Проверить: запуск без Python/CLI (`pythonResolved=false`), splash 560×450,
   readiness 0.78 s без hold, target 800×540 / min 760×520 (WebView client
   784×501 / 744×481, DPR=1), `scrollY=0`, action/total видимы, loopback
   127.0.0.1, занятый test-порт, закрытие завершает backend/launcher без
   детей, русский error path/exit 1, reduced motion.
6. **W7 — расчёты и пять settled кадров.** Таблица значений в
   `VP-02-evidence.md`; новые кадры
   `docs/screenshots/visual-02-resumed-desktop-gsv-D1..D5-settled.png` сняты
   после `document.getAnimations()`, `opacity=1`, 800×540, `scrollY=0`;
   итоги 75600/79275/71400/63000/70875; JSON
   `docs/workflow/evidence/logs/VP-02-resumed-settled-shots.json`; старые
   не-settled D1–D5 сохранены. Проверить combined 151000/7550/158550,
   legacy/422, ГСН-регрессию, САКЗ/ПК/район/НДС 5%, переключение режимов.
7. **W10 — проверки и scope.** Targeted:
   `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_launcher tests.test_frontend_redesign`
   — 36 OK/exit 0 (`VP-02-resumed-targeted-tests.txt`). Full integrated suite
   один раз по конечной ревизии: `.\.venv\Scripts\python.exe -m unittest discover -s tests`
   — exit 0, **219 tests OK** (`VP-02-final-full-suite.txt`/`.exit.txt`).
   Static/manifest: 137 assertions/exit 0 (`VP-02-resumed-static.json`),
   manifest 48 PNG/5 artifacts/106 user files
   (`VP-02-resumed-manifest.json`); `git diff --check` exit 0.
8. **Визуальная согласованность установщика.** Оценить welcome/finish sidebar
   и header внутренних страниц: труба/дом/тёплое окно/тёмно-синий/бирюза,
   отсутствие clipping/чрезмерного неона, читаемость и штатное поведение
   кнопок. Сравнить с `docs/design/splash-installer-reference.jpg` и уже
   принятым VP-01 splash. Это установщик, а не веб-макет.

## Правила review

- Использовать **фактический diff и первоисточники**, не только summary.
- Не перечитывать все 48 изображений без основания: обязательны wizard,
  native splash/main target/min, пять settled D1–D5, reduced-motion и
  side-by-side мотива установщика; остальные — по конкретному критерию.
- Повторно запускать команду можно только при недостающем/неоднозначном
  артефакте; записать причину, exact command/CWD/exit. Уже доказанные
  build/install/lifecycle/tests не дублировать.
- Не изменять файлы, не делать commit, не запускать installer build, не
  обращаться к сети. Read-only shell допустим только для проверки diff/hash.
- Вернуть: **PASS/FAIL**, severity (BLOCKER/MAJOR/MINOR/NIT), stable finding
  IDs, verdict по каждому W1–W11, фактические значения/пути evidence,
  перечень просмотренных изображений, остаточные риски и явные NOT_RUN.
- PASS возможен только если все критерии выполнены; MINOR/NIT не требуют
  нового цикла. При BLOCKER/MAJOR — FAIL с точной локализацией и evidence,
  без исправлений reviewer-ом.
- Завершить `worker_done` с вердиктом и краткими evidence; не ждать и не
  координировать других workers.
