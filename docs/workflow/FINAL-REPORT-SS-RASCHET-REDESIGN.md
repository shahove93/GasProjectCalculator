# Финальный отчёт — редизайн СС.Расчет и локальный installer

Дата: 2026-11-12. Статус: **COMPLETE** — все TASK приняты, FINAL verification
выполнен, независимая Codex R3 stage acceptance вернула **PASS**.

## Основание и scope

Пользователь запросил современный компактный дизайн и одобрил вариант 1
(APPROVALS, 2026-11-11, SHA256 ARCHITECTURE `98ACB1F2…B7DA`, ROADMAP
`1B1CBD0B…D631`). VISION.md и калькуляционные правила не изменялись.
Scope: компактный интерфейс `СС.Расчет` с оригинальной круглой эмблемой,
native window 1050×740 (min 860×620), локальная русская startup-заставка,
полностью русский Inno Setup, новый локальный x64 installer, README/evidence.
Push/merge/deploy/release/signing не выполнялись.

## Ревизия и ветка

- Ветка `feature/ss-calculator-redesign` от `e24d806`.
- Продуктовая ревизия доставки: `a14f032`. Финальный docs-only коммит
  (этот отчёт, review, STATE/HISTORY) идёт после неё и не меняет продукт.

## Принятые TASK

| TASK | Риск/маршрут | Вердикт | Ревизия |
| --- | --- | --- | --- |
| RD-01 frontend + emblem | R1, OpenCode Pro | PASS (1 full review, 0 FAIL) | `041b13d` |
| RD-02 window + splash | R2, Codex sol high | PASS (1 call) | `32e77b1` |
| RD-03 RU Inno + rebuild | R2, Codex sol high | C1 FAIL RD03-F01 → C2 PASS, finding CLOSED (2 calls) | `ffe17fb` |
| RD-04 README | R0, coordinator | PASS | `c72979a` |
| RD-FINAL-VERIFY | R0, coordinator | PASS | `8c87e44` |
| Stage acceptance | R3, Codex astra high | **PASS** | diff `e24d806..a14f032` |

## Доставленный артефакт (локально)

- Путь: `D:\Antigravity\GasProjectCalculator\installer\Output\GasProjectCalculator-Setup-1.0.0.exe`
- Размер: **15 273 647 байт**
- SHA256: **`043884107E087CCA6269EC67AF7555A3EB7E5EEF851CF14774534AE35A15949A`**
- Прежний installer этапа сохранён:
  `installer/Output/legacy/GasProjectCalculator-Setup-1.0.0-previous-stage.exe`
  (15 256 037 байт, SHA256 `2973278F…428F`).
- Артефакт локальный, неподписанный, git-ignored; не публиковался.

## Что проверено (факты)

- Точные title/ярлыки `СС.Расчет` и подпись `Калькулятор ГСН и ГСВ`;
  продуктовый ассет — только круглый знак 146×146 в исходном фиолетовом, без
  wordmark; светлый диск через CSS; остаточный риск прав зафиксирован.
- Тёмно-синяя шапка, pipe motif, teal-акценты; responsive 1050×740, 860×620,
  390×844 без horizontal scroll; реальные скриншоты RD-01.
- Локальная русская заставка 520×320 с газовым потоком к дому: показывается
  только во время старта backend, исчезает при readiness, main появляется
  после readiness (~107 мс), нет сети/искусственной задержки, reduced motion
  уважается, ошибка старта закрывает splash и останавливает backend.
- Русский Inno Setup: страницы/кнопки/ошибки/финиш/uninstaller; Start Menu
  всегда, Desktop опционален (unchecked); per-user HKCU без UAC; x64; чистая
  установка, reinstall и uninstall сохраняют пользовательские файлы
  (`%LOCALAPPDATA%\GasProjectCalculator` и markers).
- Установленное приложение без Python/консоли (GUI subsystem), окно
  `СС.Расчет`, три режима 131250/105525/145950, только `127.0.0.1`, занятый
  порт пропускается, закрытие окна освобождает порт.
- Полный suite: `Ran 163 tests ... OK`, exit 0; `app/main.py`, calculators,
  requirements и calculation-тесты без diff; developer uvicorn не затронут.
- Пользовательский сервер `:8000` (PID 12888) не останавливался и не менялся.

## Evidence

- `docs/workflow/evidence/RD-01-evidence.md` … `RD-04-evidence.md`,
  `RD-FINAL-evidence.md`; raw logs `docs/workflow/evidence/logs/RD-*`.
- Reviews: `docs/workflow/reviews/RD-01..04-review.md`,
  `RD-FINAL-VERIFY-review.md`, `FINAL-STAGE-REDESIGN-review.md`.
- Реальные скриншоты: 26 файлов `docs/screenshots/rd-*.png` (app, splash,
  installer wizard/error, uninstaller).

## Остаточные риски и backlog

- Формальные корпоративные права на эмблему репозиторием не подтверждены.
- Installer неподписан → возможен SmartScreen; публикация/подпись не входили в
  разрешение.
- Проверена одна Windows/WebView2-среда, 96 DPI; reduced motion — эмуляция;
  failure path — ранний диагностический; мобильные снимки используют
  screenshot-only overflowX workaround без изменения продукта.
- NIT backlog RD-01 F1–F3 (stale listing/mojibake/duplicate note); RD-FINAL
  N01/N02 исправлены в STATE.

## Ресурсы

Все Orca workers по стадии завершены и released; активных workflow-терминалов,
кроме координатора, нет. `:8000` PID12888 и `:8138` не тронуты. Push/merge/
deploy/release/signing не выполнялись. Installer передан локально.
