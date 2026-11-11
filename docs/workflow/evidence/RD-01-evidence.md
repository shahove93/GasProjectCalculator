# RD-01 evidence — компактный редизайн и круглая эмблема

Исполнитель: OpenCode worker (DeepSeek Flash), Dispatch ctx_6bc08bbe6a19,
TASK task_527858dbf289. Это evidence исполнителя, не проектный PASS.

## Baseline / workspace

- CWD: `D:\Antigravity\GasProjectCalculator`
- Branch: `feature/ss-calculator-redesign`
- HEAD на момент проверки: `bd91c77b285fd3dcd99e179534a21a9fe0bd4fb8`
- Продуктовый baseline: `e24d806`
- Worktree сохранил незакоммиченные workflow-документы и продуктовую работу
  предыдущих попыток RD-01; ничего из этого не отброшено.
- :8000 (PID 12888) не останавливался и не изменялся.
- Browser checks выполнены на coordinator-provided диагностическом backend
  `http://127.0.0.1:8138` (PID 23152). Собственный backend не запускался.
  Ранее случайно поднятый диагностический :8137 (PID 7804) остановлен; :8000
  не затронут.

## Что изменено (сохранено из предыдущих попыток RD-01)

- `frontend/index.html` — только presentation: тёмно-синяя компактная шапка,
  SVG pipe motif, teal-акценты, круглый emblem на светлом диске, `<title>` и
  заголовок `СС.Расчет`, подпись `Калькулятор ГСН и ГСВ`, responsive CSS,
  reduced-motion CSS, presentation-only JS. Функциональные id/поля/режимы/
  payload не менялись.
- `frontend/assets/company-emblem.png` — новый продуктовый ассет, только
  круглая эмблема, 146×146, исходный фиолетовый цвет.
- `tests/test_frontend_redesign.py` — статические проверки title/шапки/ассета/
  локальности/сохранения id.
- `tests/test_main.py` — одна строка: проверка title `СС.Расчет` вместо
  `GasProjectCalculator`.
- `assets/company-logo-source.png` — одобренный пользователем исходник.

## Commands / exit codes

| Команда | CWD | Exit |
| --- | --- | --- |
| `orca tab create --url http://127.0.0.1:8138/` | workspace | 0 |
| `orca exec --command "set viewport 1050 740"` | workspace | 0 |
| `orca exec --command "set viewport 860 620"` | workspace | 0 |
| `orca exec --command "set viewport 390 844"` | workspace | 0 |
| browser fills/clicks/evals (см. `logs/RD-01-browser.txt`) | workspace | 0 |
| `orca screenshot` / agent-browser `screenshot` (см. лог) | workspace | 0 |
| `curl ... -X POST http://127.0.0.1:8138/calculate` с невалидным payload | workspace | HTTP 422 (ожидаемо) |
| suite (reuse, см. ниже) | workspace | 0 |

Полный suite **не перезапускался**: этот worker не менял продуктовый/тестовый
код. Переиспользован `docs/workflow/evidence/logs/RD-01-suite.txt`:
`Ran 152 tests ... OK`, `EXIT=0`.

## Final diff / status

`git diff --stat e24d806 -- app tests frontend/index.html`:

```
 frontend/index.html | 230 ++++++++++++++++++++++++++++++++++++++--------------
 tests/test_main.py  |   2 +-
 2 files changed, 171 insertions(+), 61 deletions(-)
```

`app/` не изменён. Полный `git status --short` и HEAD — в
`logs/RD-01-git.txt`. Изменены/добавлены также только разрешённые evidence,
screenshots, `frontend/assets/`, `assets/`.

## Frozen acceptance checklist

| ID | Результат | Evidence |
| --- | --- | --- |
| R1-1 | PASS-кандидат: DOM `title="СС.Расчет"`, `h1="СС.Расчет"`, подпись `Калькулятор ГСН и ГСВ`; видны в шапке | `logs/RD-01-browser.txt` (R1-1), `docs/screenshots/rd-01-1050x740-initial.png` |
| R1-2 | PASS-кандидат: продуктовый ассет 146×146 существует и содержит только круглую эмблему без wordmark; в UI — фиолетовый знак на светлом диске; исходный цвет не перекрашен | `frontend/assets/company-emblem.png`, provenance ниже, `rd-01-1050x740-initial.png` |
| R1-3 | PASS-кандидат: тёмно-синий gradient `rgb(10,23,37)→rgb(11,31,51)→rgb(18,58,82)`, pipe SVG, teal `rgb(94,234,212)` / `#5eead4`, active `rgb(15,118,110)` | `logs/RD-01-browser.txt` (R1-3), desktop screenshots |
| R1-4 | PASS-кандидат: 1050×740, 860×620, 390×844 — `hScroll=false`, кнопка расчёта и итог полностью внутри ширины; на 860/390 одна колонка | метрики в `logs/RD-01-browser.txt`; `rd-01-860x620-header.png`, `rd-01-860x620-layout.png`, `rd-01-860x620-result.png`, `rd-01-390x844-header.png`, `rd-01-390x844-layout.png`, `rd-01-390x844-result.png` |
| R1-5 | PASS-кандидат: ГСН 14 м / 2 угла / 4 ч / район / юрлицо → **125 000 / 6 250 / 131 250** | `logs/RD-01-browser.txt` (R1-5), `rd-01-gsn-result-1050x740.png` |
| R1-6 | PASS-кандидат: ГСВ 8 м Ø25 / 2 отверстия / САКЗ 1 + ПК / район / частник → **100 500 / 5 025 / 105 525** | `logs/RD-01-browser.txt` (R1-6), `rd-01-gsv-result-1050x740.png` |
| R1-7 | PASS-кандидат: Combined ГСН 10 м без опций + ГСВ 5 м Ø25 без опций / район → **139 000 / 6 950 / 145 950** | `logs/RD-01-browser.txt` (R1-7), `rd-01-combined-result-1050x740.png` |
| R1-8 | PASS-кандидат: все три переключения очищают result-контейнеры (`none`) и показывают только `calc-info`; реальный 422 от сервера отображается текстом ошибки | `logs/RD-01-browser.txt` (R1-8), `rd-01-422-error-1050x740.png`, `logs/RD-01-422-response.json` |
| R1-9 | PASS-кандидат: `performance` resources — только same-origin `/calculate*`; эмблема — inline `data:image/png` 146×146; grep по `https?://`, `@import`, CDN — нет совпадений | `logs/RD-01-browser.txt` (R1-9) |
| R1-10 | PASS-кандидат: `app/` без diff; suite reuse 152 OK / EXIT=0 | `logs/RD-01-git.txt`, `logs/RD-01-suite.txt` |
| R1-11 | PASS-кандидат: при `prefers-reduced-motion: reduce` pipe animation `none`, duration `0s`, transition `1e-06s`; CSS также содержит глобальный reduce-блок | `logs/RD-01-browser.txt` (R1-11), `rd-01-reduced-motion-1050x740.png` |

## Responsive viewport measurements (real browser)

| Viewport | scrollWidth / clientWidth | hScroll | Submit btn left..right | Total left..right | Grid |
| --- | --- | --- | --- | --- | --- |
| 1050×740 | 1035 / 1035 | false | 45..505 | 840..971 | `509.766px 461.219px` |
| 860×620 | 845 / 845 | false | 45..800 | 650..781 | `805px` |
| 390×844 | 375 / 375 | false | 26..349 | 41..146 | `355px` |

## Emblem provenance и права

- Источник: `assets/company-logo-source.png`, предоставлен пользователем
  (в REDESIGN-BRIEF указан исходный путь на рабочей машине пользователя).
  SHA256: `86B79EFDB1FCCA038B7D73BAAF51DC634AD60F731551CB692EA323FBD7D698AB`.
  Размер: 1200×146 (круглый знак + wordmark «СЕВЕРНОЕ СИЯНИЕ»).
- Продуктовый ассет: `frontend/assets/company-emblem.png`.
  SHA256: `C3DCBA6DC868B8C9F39C004C6FB23C21D31CD58B9FEEC209CAF8697BBD52F4DC`.
  Размер: 146×146.
- Crop provenance: из исходника взят только левый квадратный круглый знак;
  текстовая часть/wordmark не включены. Знак не перекрашивался, не
  генерировался новый растр; фон прозрачный, светлый диск создаётся CSS
  (`.brand-emblem`), не пикселями ассета.
- Одобрение: пользователь одобрил вариант 1 и эмблему 2026-11-11
  (APPROVALS.md, REDESIGN-BRIEF.md; цитата: «Ну давай, окей, вот этот первый
  вариант мне тоже нравится.»). Дата в APPROVALS: 2026-11-11.
- Остаточный риск: репозиторий не устанавливает формальные корпоративные
  права на логотип. Это риск для последующего публичного распространения, а не
  основание менять scope RD-01. Лицензия не выдумывается.

## Screenshots

- `docs/screenshots/rd-01-1050x740-initial.png`
- `docs/screenshots/rd-01-gsn-result-1050x740.png`
- `docs/screenshots/rd-01-gsv-result-1050x740.png`
- `docs/screenshots/rd-01-combined-result-1050x740.png`
- `docs/screenshots/rd-01-422-error-1050x740.png`
- `docs/screenshots/rd-01-860x620-header.png`
- `docs/screenshots/rd-01-860x620-layout.png` (весь layout: кнопка + результат)
- `docs/screenshots/rd-01-860x620-result.png`
- `docs/screenshots/rd-01-390x844-header.png`
- `docs/screenshots/rd-01-390x844-layout.png` (весь layout: кнопка + результат)
- `docs/screenshots/rd-01-390x844-result.png`
- `docs/screenshots/rd-01-reduced-motion-1050x740.png`

Примечание по 860/390: изначально viewport-скриншот Orca agent-browser после
прокрутки длинной страницы отрисовывал верхние «плитки» пустыми (артефакт
компоновки браузера), хотя DOM-метрики были корректны. Артефакт снят
runtime-настройкой `document.body.style.overflowX='visible'` только на время
снимка (продуктовый CSS не менялся). Итоговые `rd-01-390x844-result.png` и
`rd-01-860x620-result.png` — реальные viewport-снимки, где одновременно видны
кнопка расчёта и итог; дополнительные element-снимки `.layout` приложены.

## Logs

- `docs/workflow/evidence/logs/RD-01-browser.txt` — реальные browser steps и
  DOM/computed/network замеры.
- `docs/workflow/evidence/logs/RD-01-git.txt` — branch/HEAD/status/diff.
- `docs/workflow/evidence/logs/RD-01-422-payload.json` /
  `RD-01-422-response.json` — 422 request/response.
- `docs/workflow/evidence/logs/RD-01-suite.txt` — reuse, 152 OK, EXIT=0.
- `docs/workflow/evidence/logs/RD-01-uvicorn-8137.*` — след случайного
  диагностического backend (остановлен); `RD-01-uvicorn.*` — прежняя попытка.

## NOT_RUN / вне scope

- Установщик, splash, ярлыки, RU wizard — следующие RD-шаги, здесь не
  выполнялись.
- Push/merge/deploy/release не выполнялись.
- Независимый R1 review — за координатором/ревьюером; здесь проектный PASS не
  заявляется.
- Полный suite повторно не запускался: код не менялся, использован
  существующий лог 152 OK.
