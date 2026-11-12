# VP-01 — визуальное продолжение MD-02 / A2 / C1

Дата: 2026-11-12. Автор: исполнитель Orca Codex, **не независимый reviewer**.
Результат: реализация и evidence переданы на routed R2 vision review;
project PASS не выставлен, commit не выполнен.

## Идентичность, разрешения и границы

- Workspace/CWD всех команд: `D:/Antigravity/GasProjectCalculator`.
- Branch: `feature/gsv-mixed-diameters`.
- Baseline/HEAD: `ac59d8c27ed47be07ac9b54acf8285bcab704be0` (HEAD не менялся).
- Task: `task_409018258f8b`; Dispatch: `ctx_0d12c08f442b`;
  worker terminal `term_9f97403b-8f8a-494e-9fe4-dcefc20a7ad5`.
- Requested **и effective**: `agent=codex`, `model=gpt-6-astra`,
  `effort=high`: реальный `orca orchestration worker-show --dispatch
  ctx_0d12c08f442b --json --full`, сохранён **до правки продукта** в
  [VP-01-effective-worker.json](logs/VP-01-effective-worker.json).
  Runtime показывает exactWorker/live; `start_unknown` — старый неполученный
  turn-start hook, не отсутствие worker. Не использовались helper workers.
- Сохранены прежние logical TASK/counters A1/C1 и замечание MD02-N1;
  этот пакет не сбрасывает историю и не присваивает review slot.
- Прочитаны AGENTS, brief, APPROVALS, VISION, ARCHITECTURE, ROADMAP,
  MODEL-ROUTING, MD-02, autonomous-development/orchestration и routing/review
  references; все 3 новых reference и 3 прежних screenshot открыты vision.

Незакоммиченные root/coordinator документы AGENTS, VISION, ARCHITECTURE,
ROADMAP, APPROVALS, HISTORY, MODEL-ROUTING, STATE, TASK/dispatch/preflight и
reference **не редактировались этим worker**. Их изменения видны в общем
git status и отделены от продуктового diff. Не менялись installer, packaging,
requirements, .venv, конфигурация/аккаунты, пользовательская установка.

## Продуктовые изменения

1. `frontend/index.html`: новые inline SVG шапки/подвала, спокойные teal
   оттенки, мягкие тени/границы, selected-gradient и тёплая карточка итога.
   Размеры/порядок формы, режимы, обработчики и render сохранены.
2. `frontend/splash.html`: композиция по новому reference, локальная эмблема,
   «Подготавливаем расчёт…», мягко движущиеся стрелки потока; полноценная
   неподвижная композиция при OS reduced-motion и диагностическом флаге.
3. `app/desktop_launcher.py`: **только** SPLASH_WIDTH=560,
   SPLASH_HEIGHT=450, SPLASH_BACKGROUND="#081e2b".
4. `tests/test_desktop_launcher.py`: единственное изменение — ожидаемая
   русская надпись «Подготавливаем расчёт…» вместо старой. Проверки
   функциональности, безопасности, lifecycle и reduced motion не ослаблены.
5. Локальные воспроизводимые SVG: `frontend/assets/header-pipe.svg`,
   `footer-pipe.svg`, `splash-scene.svg`, `installer-sidebar.svg`,
   `installer-header.svg`; готовые exports `installer-sidebar.png` (328×628)
   и `installer-header.png` (110×110). Company emblem не изменён.

Diff: [VP-01-product.diff](logs/VP-01-product.diff). Полный status, включая
чужие проектные документы: [VP-01-status.txt](logs/VP-01-status.txt).
Хэши продукта и доказательство zero-diff:
[VP-01-static.json](logs/VP-01-static.json).

## Визуальное соответствие

| Reference | Реализация и осознанное сохранение компактности | Evidence |
| --- | --- | --- |
| header-detail-reference.jpg | Navy фон; одна полупрозрачная труба: вход снизу слева, подъём к вентилю, второй изгиб вверх справа; 3 металлические муфты. Горизонтальный золотой маховик около 63×14 SVG units, отдельные ножка и корпус. Нет второй ветки, точек, пунктира или glow-filter. Весь маховик внутри viewBox с верхним запасом. Бренд/эмблема/режимы остаются слева. Шапка компактнее фото по высоте, в пределах прежнего окна. | [compare-header](../../screenshots/visual-01-compare-header.png), [native target](../../screenshots/visual-01-native-target-gsv.png) |
| footer-detail-reference.jpg | Светлый фон, двойной тонкий контур трубы; слева голубое пламя и маленькая горелка, 3 муфты; справа контурный дом/дымоход, тёплое окно, кусты и дерево. Центральный прямой участок удлинён до ширины полосы, пропорции дома/пламени не растянуты. ViewBox -5…91 обеспечивает запас над крышей/пламенем и под землёй. Нет массивной тёмной трубы или неоновой линии. | [compare-footer](../../screenshots/visual-01-compare-footer.png), [native min](../../screenshots/visual-01-native-min-combined.png) |
| splash-installer-reference.jpg | 560×450, navy gradient без серой фото-рамки; название и узкая teal-черта в верхней трети, статус ниже. Слева большая непрерывная труба с овальным вентилем, изгиб вниз, светлый поток вправо к контурному дому, 4 отдельные тёплые оконные панели, плавные холмы. Короткое настоящее имя оставляет больше воздуха, чем длинный title фото; эмблема в верхнем правом углу. | [compare-splash](../../screenshots/visual-01-compare-splash.png), [native splash](../../screenshots/visual-01-native-splash.png) |

Сравнения состоят из **исходного reference и реального native capture** рядом;
пропорции каждого изображения сохранены. Header/footer — документированные
кропы native 800×540: (8,31,792,114) и (8,469,792,532); ничего не дорисовано.
Сборка: [VP-01-compare.py](logs/VP-01-compare.py), exit 0;
[размеры](logs/VP-01-compare.txt). Открыты vision итоговые сравнения, native
target/min, splash/error, mobile combined и оба installer exports.

## Artwork для VP-02

- [installer-sidebar.svg](../../../frontend/assets/installer-sidebar.svg),
  [PNG](../../../frontend/assets/installer-sidebar.png): вертикальная
  welcome/finish-панель 328×628 (2× стандартного 164×314), бренд, pipe/house,
  тёплое окно, navy/teal, мягкий переход к нижней сцене.
- [installer-header.svg](../../../frontend/assets/installer-header.svg),
  [PNG](../../../frontend/assets/installer-header.png): малая верхняя
  иллюстрация 110×110 (2×55×55), тот же вентиль, поток и дом.
- SVG самостоятельные, без внешних изображений/fonts/сетевых загрузок.
  В sidebar включена геометрия `splash-scene.svg`; PNG получены локальным
  Chromium renderer из SVG, не изображением installer-макета.
- Воспроизведение: `node docs/workflow/evidence/logs/VP-01-render.cjs`,
  exit 0, [render log](logs/VP-01-render.txt). Используется уже установленный
  Playwright и Edge, новые зависимости не установлены. Для самого wizard
  при необходимости BMP конвертируется в VP-02, installer здесь не менялся.

## Реальные browser / native проверки

| Проверка | Команда/артефакт | Итог |
| --- | --- | --- |
| Targeted tests | `.\.venv\Scripts\python.exe -m unittest tests.test_frontend_redesign tests.test_desktop_launcher -v` | **36 OK, exit 0**, [log](logs/VP-01-targeted-tests.txt), [exit](logs/VP-01-targeted-tests.exit.txt) |
| Browser desktop 800×540 / mobile 390×844 | `node docs/workflow/evidence/logs/VP-01-browser.cjs` | exit 0; реальный Edge Chromium 157.0.4341.46, 3 режима до/после, D1–D5, options, 422, switch-clear, reduced motion; [JSON](logs/VP-01-browser.json), [summary](logs/VP-01-browser-run.txt) |
| Literal mobile viewport | `node docs/workflow/evidence/logs/VP-01-mobile-viewport.cjs` | exit 0; [метрики](logs/VP-01-mobile-viewport.json), отдельные 390×844 screenshot каждого режима до/после |
| Native 800×540 и min760×520 | `$env:MD02_BRIDGE='C:/Users/user/AppData/Local/Temp/opencode/vp-01-native/normal-bridge.json'; .\.venv\Scripts\python.exe C:/Users/user/AppData/Local/Temp/opencode/vp-01-native/drive_native.py 14840 8174 D:/Antigravity/GasProjectCalculator/docs/workflow/evidence/logs/VP-01-native.json` | exit 0; [JSON](logs/VP-01-native.json), [summary](logs/VP-01-native-run.txt) |
| Static / contract diff | `.\.venv\Scripts\python.exe docs/workflow/evidence/logs/VP-01-static.py` | exit 0; JS byte-equivalent as text, form nodes/attributes/order identical, launcher AST identical excluding 3 constants, API/calculators zero-diff, no external asset URLs |
| Product whitespace | `git diff --check -- frontend app/desktop_launcher.py tests/test_desktop_launcher.py` | exit 0 |

Native screenshot получен настоящим Win32 `PrintWindow(PW_RENDERFULLCONTENT)`
для окна **с проверенным PID**, размеры через GetWindowRect/GetClientRect,
DPI через GetDpiForWindow. Никаких CSS/JS/zoom screenshot workaround.
Eval bridge менял только тестовые inputs/режимы, обычную прокрутку внутренних
областей и отправлял реальные запросы; product JS не подменён.
Harness заархивирован: [VP-01-native-harness.zip](logs/VP-01-native-harness.zip).

| Native размер | Фактический client / DPI | Все 3 режима после расчёта |
| --- | --- | --- |
| 800×540 | 784×501 / 96 | scrollX=0, scrollY=0, h/v page scroll=false, action+total in viewport=true |
| 760×520 | 744×481 / 96 | те же значения; формы/детали имеют прежнюю внутреннюю прокрутку |

Browser desktop: document=800×540, scrollY=0, action+total видимы.
Mobile: documentWidth=390, horizontal overflow отсутствует; ГСН/ГСВ action+total
видимы при scrollY=0, combined — при обычной прокрутке scrollY=269
(action y719.55–750.55, total y392.38–419.38 в viewport844). Full-page capture
дополнен отдельным literal viewport, чтобы не выдавать высокий PNG за экран844.

Изображения:
- `visual-01-native-{target,min}-{gsn,gsv,combined}{,-before}.png`;
- `visual-01-native-{target,min}-window.png`, `visual-01-native-422.png`;
- `visual-01-desktop-{gsn,gsv,combined}-{before,after}.png`;
- `visual-01-desktop-gsv-D1.png` … `D5.png`;
- `visual-01-mobile-{gsn,gsv,combined}-{before,after}.png` (full page);
- `visual-01-mobile-{gsn,gsv,combined}-viewport-{before,after}.png` (390×844);
- `visual-01-{desktop,mobile}-{422,switch-clear}.png`;
- `visual-01-native-splash.png`, `visual-01-native-error.png`;
- `visual-01-splash-{animated,os,flag}.png`;
- `visual-01-compare-{header,footer,splash}.png`.

## Запросы и суммы

Все payload/response сохранены в browser JSON: настоящие POST, статус и тело.
Режимы desktop и mobile до/после: ГСН 10 м/город/без опций **68 250 ₽**;
ГСВ [4,0,4]/город **75 600 ₽**; combined с районом **158 550 ₽**.
Native подтверждает те же три значения на обоих размерах.

| Mixed длины [до25,32–40,57] | Итог с НДС5% | Оплачиваемые метры |
| --- | ---: | --- |
| D1 [4,0,4] | 75 600 | [0,0,3] |
| D2 [2,4,3] | 79 275 | [0,1,3] |
| D3 [0,5,2] | 71 400 | [0,0,2] |
| D4 [3,1,1] | 63 000 | [0,0,0] |
| D5 [8,0,0] | 70 875 | [3,0,0] |

D5 + САКЗ2 + ПК + район: **111 825 ₽**. При САКЗ0 ПК disabled и снят;
при САКЗ2 доступен. В combined район +7000 каждому разделу до НДС:
65 000+7 000 и 72 000+7 000 → 151 000 + 7 550 = 158 550.
Дополнительный viewport combined без района: **143 850 ₽** (другой payload,
не расхождение с предыдущим примером). Реальный 422 при ПК/САКЗ0 показывает
русское сообщение; переключение режима очищает прежний результат/ошибку.

## Процессы, splash lifecycle, cleanup

| Владение / PID / session | Команда и назначение | Завершение |
| --- | --- | --- |
| worker backend 22540 / 85743 | `.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8172` | после browser checks собственный process остановлен Stop-Process; terminal exit1 от остановки, **не ошибка проверки** |
| worker native 9504 / 65541 | `.\.venv\Scripts\python.exe -m app.desktop_launcher --preferred-port 8173 --port-file C:/Users/user/AppData/Local/Temp/opencode/vp-01-native/port.json --log-file D:/Antigravity/GasProjectCalculator/docs/workflow/evidence/logs/VP-01-native-launch.log --splash-hold-seconds 30 --eval-bridge C:/Users/user/AppData/Local/Temp/opencode/vp-01-native/bridge.json --auto-close-seconds 240` | только диагностический hold для splash screenshot; main закрыт CloseMainWindow, exit0 |
| worker normal native 14840 / 98396 | `.\.venv\Scripts\python.exe -m app.desktop_launcher --preferred-port 8174 --port-file C:/Users/user/AppData/Local/Temp/opencode/vp-01-native/normal-port.json --log-file D:/Antigravity/GasProjectCalculator/docs/workflow/evidence/logs/VP-01-normal-launch.log --eval-bridge C:/Users/user/AppData/Local/Temp/opencode/vp-01-native/normal-bridge.json --auto-close-seconds 240` | **нет splash-hold**; readiness0.78s → close splash → main shown; CloseMainWindow → backend stopped → exit0 |
| worker error native 11568 / 49243 | `.\.venv\Scripts\python.exe -m app.desktop_launcher --preferred-port 8175 --port-file C:/Users/user/AppData/Local/Temp/opencode/vp-01-native/error-port.json --log-file D:/Antigravity/GasProjectCalculator/docs/workflow/evidence/logs/VP-01-error-launch.log --simulate-startup-failure` | splash closed after failure, реальный русский диалог, ожидаемый exit1, no listener |
| supplemental mobile backend 11960 / 47565 | та же uvicorn command /8172 | только недостающие literal viewport captures; затем Stop-Process собственного PID |

Логи: [normal lifecycle](logs/VP-01-normal-launch.log),
[diagnostic splash](logs/VP-01-native-launch.log),
[error lifecycle](logs/VP-01-error-launch.log),
[session exit codes](logs/VP-01-sessions.json).
Native splash outer/client560×450, DPI96:
[geometry](logs/VP-01-native-splash.json). Error dialog outer426×283:
[geometry](logs/VP-01-native-error.json).

Reduced motion: browser computed animation `gas-flow` в normal;
`none`, opacity0.8 в OS reduce и `?reduced-motion=1`. Геометрия и весь
светящийся трубный путь статичны всегда; animation двигает только стрелки.
Lifecycle/readiness/error/loopback/timing код доказан zero-diff AST.

После cleanup собственных PID и дочерних процессов **0**:
[processes-after-close](logs/VP-01-processes-after-close.json).
На 8172–8175 listeners нет. Чужие :8000 PID12888 и :8138 PID23152 сохранены:
[ports-after-close](logs/VP-01-ports-after-close.json). Никаких user sessions
или чужих процессов не закрывали.

## Честные ограничения / история verification

- Первоначальная локальная попытка импортировать Playwright в node_repl дала
  `The requested module './index.js' does not provide an export named 'default'`.
  Прямой Node использовал уже установленный пакет. Default bundled Chromium
  headless shell отсутствовал (`Executable doesn't exist at ...chromium_headless_shell-1234...`);
  выбран **уже установленный Edge** через `channel:'msedge'`, без download.
  Это устранённые environment gaps, результаты не имитировались.
- После первого visual capture только прямой центральный участок footer был
  удлинён до ширины полосы. Final browser/native/targeted evidence повторены
  на окончательном продукте по причине изменения artwork. Первоначальные
  native JSON/summary сохранены с суффиксом `-initial`; окончательные без него.
- Supplemental mobile run заполнил gap literal390×844 screenshots, основной
  mobile набор изначально был full-page. Математический suite заново не гонялся.
- Full integrated unittest suite — **NOT_RUN этим worker**: его единожды
  выполняет coordinator после VP-02 по согласованному workflow. Здесь целевые36.
- Native DPI отличные от96, installer/build/install/version1.2.0 — **NOT_RUN**
  в VP-01, входят в следующий packaging scope. Main geometry не изменена.
- Общий `git diff --check` указывает существующий extra blank line в
  root-owned VISION.md:94; файл не исправлялся. **Product-only check exit0**.
- R2 независимое review и приёмка сходства — **NOT_REVIEWED**; executor
  предоставляет реальные изображения и mapping, не подменяет reviewer.

## Frozen checklist coverage (не verdict)

V1–V4: три comparisons + native + SVG geometry; V5: brand/emblem screenshots
и static scan; V6: native target/min + browser/mobile metrics/screens;
V7: presentation-only diff; V8: payload/response/DOM values и backend zero-diff;
V9: normal/error lifecycle logs, native splash/error и reduced-motion captures;
V10: 2 standalone SVG+PNG и renderer; V11: 36 targeted tests/static/scope;
V12: этот pack, реальные PNG, команды/logs и явно перечисленные NOT_RUN.

Следующий владелец: coordinator → независимый Codex Sol/high R2 vision review.
После routed PASS coordinator может сделать разрешённый scoped local commit;
никаких push/merge/deploy/release здесь не выполнялось.
