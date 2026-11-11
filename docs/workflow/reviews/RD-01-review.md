# RD-01 — независимое R1-ревью (OpenCode Pro)

- Логический TASK: RD-01, подход A1, цикл C1.
- Ревьюер: отдельный Orca OpenCode worker `ctx_edd1a2ae92e9`
  (`task_696412840fc3`), requested/effective model `deepseek/deepseek-v4-pro`,
  terminal term_863f5dff.
- Ревизия: ветка `feature/ss-calculator-redesign`, HEAD `bd91c77`,
  продуктовый baseline `e24d806`, рабочее дерево с uncommitted RD-01.
- Пакет: `docs/workflow/evidence/RD-01-evidence.md`, логи
  `docs/workflow/evidence/logs/RD-01-*`, 12 скриншотов
  `docs/screenshots/rd-01-*`, frozen checklist `docs/workflow/tasks/RD-01.md`.
- Ревьюер файлов не менял и не коммитил; выполнена только read-only проверка и
  сверка фактического diff/артефактов. Повторных прогонов не было: evidence
  полный и однозначный.

## Вердикт: PASS

BLOCKER/MAJOR нет; FAIL нет. Все критерии R1-1..R1-11 подтверждены:

| ID | Вердикт | Подтверждение |
| --- | --- | --- |
| R1-1 | PASS | `<title>`/h1 `СС.Расчет`, подпись `Калькулятор ГСН и ГСВ` в DOM/браузере; тесты title. |
| R1-2 | PASS | `frontend/assets/company-emblem.png` 146×146, SHA256 `C3DCBA6D…52F4DC`; фиолетовый RGB(63,45,146) совпадает с исходником, без перекраски; прозрачные углы, только круглый знак без wordmark; светлый диск через CSS. |
| R1-3 | PASS | Тёмно-синий gradient, pipe SVG, teal `#5eead4/#2dd4bf`, active `#0f766e` (computed + скриншоты). |
| R1-4 | PASS | 1050×740, 860×620, 390×844: hScroll=false, кнопка и итог внутри viewport; скриншоты размеров сверены. |
| R1-5 | PASS | ГСН 14 м/2 угла/4 ч/район/юрлицо → 125000/6250/131250. |
| R1-6 | PASS | ГСВ 8 м Ø25/2 отверстия/САКЗ 1+ПК/район/частник → 100500/5025/105525. |
| R1-7 | PASS | Combined ГСН 10 м + ГСВ 5 м Ø25 без опций/район → 139000/6950/145950. |
| R1-8 | PASS | Переключение режимов очищает прежний результат; 422 виден в браузере и подтверждён HTTP 422 + скриншот. |
| R1-9 | PASS | Нет `https?://`, `@import`, CDN/webfonts; эмблема inline `data:image/png`; resources только same-origin `/calculate*`. |
| R1-10 | PASS | `app/` — нулевой diff; suite log 152 OK / EXIT=0; 146 baseline + 6 новых frontend-тестов согласованы. |
| R1-11 | PASS | `prefers-reduced-motion: reduce`, pipe animation `none`, duration 0.001ms; emulated media подтверждён. |

## Findings (NIT, backlog; не влияют на PASS)

- F1: `RD-01-git.txt` не перечисляет `rd-01-390x844-layout.png` и
  `rd-01-860x620-layout.png` (stale listing; файлы существуют).
- F2: `RD-01-422-response.json` содержит mojibake для русского текста
  (кодировка терминала); семантика `loc=body/customer_type` ясна, браузер
  показывает корректный текст.
- F3: `RD-01-browser.txt` содержит дублирующиеся секции примечаний о снимках.

## Наблюдения по scope

Продуктовый diff ограничен `frontend/index.html` (только presentation; form
markup, все функциональные id/поля и весь `<script>` байт-идентичны baseline),
`tests/test_main.py` (только title-assertion), новыми
`frontend/assets/company-emblem.png`, `tests/test_frontend_redesign.py`,
`assets/company-logo-source.png` (одобренный исходник). Recovery/STATE/HISTORY
и evidence — координаторские workflow-записи, не продуктовый scope.
Неожиданных файлов вне scope нет.

## Остаточный риск / NOT_RUN

- Репозиторий не устанавливает формальные корпоративные права на логотип;
  зафиксировано как остаточный риск, лицензия не выдумана.
- NOT_RUN: installer/splash/ярлыки (следующие RD-шаги), push/merge/deploy.

## Счётчики

- R1 full reviews: 1 (PASS); failed reviews: 0; Codex calls: 0 (R1).
- A1, C1; следующий шаг — scoped commit RD-01 и переход к RD-02.
