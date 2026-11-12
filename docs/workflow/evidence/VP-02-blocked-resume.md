# VP-02 resume — BLOCKED: повторный Codex provider usage limit

Дата: 2026-11-12. Статус: **BLOCKED**, не product PASS и не FAIL продукта.
Logical TASK: **MD-03 A2/C1** (тот же подход после первого BLOCKED). Координатор:
OpenCode/DeepSeek Flash. Исполнитель: настоящий Orca Codex **`gpt-6-astra`**,
effort **`high`**.

## Точная причина остановки

Во время финальной досъёмки пяти browser-кадров Codex вернул реальный отказ
провайдера:

```text
You've hit your usage limit. Upgrade to Pro
(https://chatgpt.com/explore/pro), visit
https://chatgpt.com/settings/usage to purchase more credits or try again at
9:31 PM.
Approaching rate limits
Switch to gpt-6-luna for lower credit usage?
```

Локальное время: 2026-11-12 около 16:54 (Windows, +03:00). Это фактический
provider usage limit, не ошибка продукта и не review verdict.

Согласно `routing-and-budget.md` и прямому заданию:

- зависимая цепочка остановлена;
- **не** выполнялись reset-credit, покупка кредитов, смена аккаунта/тарифа,
  пересоздание сессии ради обхода, молчаливая замена модели; предложенный
  `gpt-6-luna` отклонён, поскольку visual scope пользователь закрепил только за
  `gpt-6-astra`/high;
- автоматическое продолжение после reset не запускалось; решение за root.

## Идентификация

- Координатор: `ctx_ed7166e32fdc` / `task_d75e7fdcd753`, terminal
  `term_f61ee838-7bfb-44e4-a660-994e91dc82e4` (Run `run_8e5d92ad57c7`).
- Контейнер возобновления: Run `run_51b48d1d96cc`, task `task_150bb380db2c`.
- Исполнитель: `ctx_988a8c02d5c3`, terminal
  `term_879889ea-ac9e-48ad-bc89-978a67a20e10`.
- Requested/effective до работы и после: `agent=codex`,
  `model=gpt-6-astra`, `effort=high`; receipts
  [launch](logs/VP-02-resume-receipt.json),
  [effective](logs/VP-02-resume-effective.json),
  [final state](logs/VP-02-resume-effective-final.json).
- Worker остановлен/fenced: `worker-stop` →
  `state=stopped`, `processAction=closed_agent_terminal`,
  `ptyKilled=true`; [receipt](logs/VP-02-resumed-worker-stop.json).

## Что реально сделано до остановки

Исполнитель завершил основной evidence pack
[VP-02-evidence.md](VP-02-evidence.md) и добавил только evidence-файлы
`VP-02-resumed-*` / `visual-02-resumed-*`; продуктовых правок, пересборки и
коммитов в этом dispatch нет.

Подтверждено в pack:

- W1–W3/W11: artifact 1.2.0 — 15 373 267 B, FileVersion `1.2.0.0`,
  ProductVersion `1.2.0`, SHA256
  `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113`;
  прежние 1.0.0/1.1.0/legacy bytes и remote releases не изменены; push/merge/
  deploy/release отсутствуют.
- W4: реальные RU wizard welcome/dir/tasks/ready/installing/finish screenshots
  598×464; штатный Inno Setup 6.4.1, Russian-only, прежний AppId, фирменные
  sidebar/header.
- W6–W7: installed EXE без CLI/Python (`pythonResolved=false`), native target
  800×540 / min 760×520, WebView client 784×501 / 744×481, DPR=1,
  `scrollY=0`, action/total видимы; browser desktop/min/mobile390×844; все три
  режима; mixed 75600/79275/71400/63000/70875; combined 151000/7550/158550;
  legacy/422; ГСН-регрессия; САКЗ/ПК/район/НДС 5%; exact requests/responses.
- W8: loopback 127.0.0.1, собственный занятый порт 65531→65532; readiness
  0.76 s без искусственной задержки; закрытие завершает backend/launcher,
  без дочерних процессов; error path с русским сообщением и ожидаемым exit1;
  reduced motion.
- W5/W9: изолированный cycle install 1.1.0 → upgrade 1.2.0 → reinstall →
  uninstall, numeric exits 0; user sentinel files сохранены; HKCU exact
  export/restore, оба ярлыка exact SHA256, все 106 user files unchanged,
  исходные PID/start times сохранены.
- W10: targeted tests `.venv/Scripts/python.exe -m unittest
  tests.test_desktop_launcher tests.test_frontend_redesign` — 36 OK/exit0;
  static/manifest checks 137 assertions/exit0; `git diff --check` exit0;
  product diff только installer version/branding/build-output; `app/`,
  `frontend/`, `packaging/`, `requirements.txt`, `tests/` zero-diff.
- Manifest: 5 artifacts unchanged, 48 real PNG, 106 user files unchanged,
  registry/shortcuts exact.

## Известный незакрытый gap (не скрыт)

Пять browser-снимков смешанных эталонов
`visual-02-resumed-desktop-gsv-D1.png` … `D5.png` были сняты во время
0,3-секундной анимации появления итоговой суммы (`fadeUp`). Числа в API/DOM
ответах корректны, но кадры не являются «settled». Исполнитель явно
зафиксировал это и начал переснимать только эти пять кадров; попытка упала с
`ERR_UNSAFE_PORT` (`http://127.0.0.1:0/`) и не была доведена — на этом шаге
сработал provider limit. Исходные пять PNG и причина повторения сохранены;
новые settled-кадры **NOT_RUN**. Это визуальный evidence-дефект, не изменение
расчётов.

## Сохранение пользовательской среды и артефактов

После остановки проверено:

- пользовательский процесс PID 13248
  `%LOCALAPPDATA%\Programs\GasProjectCalculator\GasProjectCalculator.exe`
  работает; :8000 PID 12888 и :8138 PID 23152 сохранены;
- HKCU uninstall key `DisplayVersion=1.0.0`, `InstallLocation` пользовательский;
  Start Menu и Desktop ярлыки указывают на пользовательский EXE;
- пользовательская установка: 106 файлов, 37 372 847 B — не изменены;
- изолированных процессов `vp-02-isolated`/`vp-02-resume` не осталось;
- artifact 1.2.0 SHA256 прежний; 1.0.0/1.1.0/legacy hashes прежние;
- `.venv`, чужие процессы/сессии, глобальные конфиги не менялись;
- незакоммиченные installer/assets/evidence/screenshots сохранены; commit не
  выполнялся.

## Counters и следующий шаг

- MD-03: A1/C1 — 1 full review, 0 FAIL, 1/4 Codex calls. A2/C1 — тот же
  незавершённый первый цикл; повторный запуск после первого BLOCKED не добавил
  цикл, а второй provider limit снова прервал C1 без verdict. Счётчик review
  не увеличивается; резерв call 2/4 остаётся.
- Финальная stage-приёмка Codex/Astra high отдельно; full suite — координатор
  один раз по конечной ревизии. Оба шага зависимы от восстановления доступа
  Codex и решения root.
- Next после явного восстановления лимитов: сначала только досъёмка пяти
  settled browser-кадров, затем независимый R2 `gpt-6.1-sol` high review
  actual diff/evidence, full suite, отдельная финальная Astra-приёмка,
  FINAL-REPORT/README/STATE и local scoped commit. До этого PASS/COMPLETE не
  объявляется.

## Явно НЕ выполнялось

- reset-credit/покупка кредитов/смена аккаунта/тарифа/модели/обход лимита;
- checkout/clean/reset/stash; потеря чужих/незакоммиченных изменений;
- изменения пользовательской установки/HKCU/ярлыков, `.venv`, :8000/:8138;
- commit/push/merge/deploy/release/signing.
