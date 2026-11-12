# Итоговый отчёт: компактность UI и пересобранный installer

Дата: 2026-11-12. Ветка: `feature/ss-calculator-redesign`.
Статус: **COMPLETE** (RD-05, RD-06, RD-07 и Codex R3 stage acceptance PASS).

## Запрос и scope

Пользователь указал, что установленное приложение непохоже на выбранный макет,
расстояние между строками большое, и попросил сделать калькулятор примерно
вдвое компактнее. Утверждение запроса и SHA256 — `APPROVALS.md`; архитектурное
уточнение — `ARCHITECTURE.md`; последовательность — `ROADMAP.md`; brief —
`COMPACT-CORRECTION-BRIEF.md`. Уточнение основного макета 2026-11-12:
основной образец — `docs/design/original-window-splash-reference.png`;
`approved-variant-1-reference.png` — вспомогательный только для эмблемы/
названия. Название `СС.Расчет`, НДС 5%, все реальные поля и расчёты сохранены.

Scope: presentation `frontend/index.html`, native geometry
`app/desktop_launcher.py`, presentation tests, пересборка package/installer,
новый локальный installer, evidence/screenshots/README. Вычисления, API,
requirements и пользовательские данные не менялись.

## Что доставлено

- Компактное native-окно **800×540** (client 784×501), min **760×520**
  (client 744×481), DPI 96. Площадь окна уменьшена с 1050×740 (777 000 px²)
  до 800×540 (432 000 px²) — **55,6% прежней площади** (~на 44% меньше);
  min — с 860×620 (533 200 px²) до 760×520 (395 200 px²), **74,1%**.
- Плотная композиция по основному макету: тёмная шапка с эмблемой, названием,
  трубой/вентилем и режимами; строка заказчика; слева пары полей и отдельный
  блок опций; справа тёплая светлая карточка «Итого с НДС» и кнопка; снизу
  труба к дому. Текст читается без масштабирования; CSS zoom/scale не
  используется.
- В target/min и всех трёх режимах при `scrollY=0` действие и итог видимы,
  page h/v scroll отсутствует; combined использует только внутреннюю
  прокрутку детализации. Mobile 390×844 без horizontal overflow.
- Сохранены: три режима, все поля/payload, значения **131250 / 105525 / 145950**,
  САКЗ/ПК (ПК только при САКЗ), switch и видимый HTTP 422, loopback/close
  lifecycle, русская заставка, reduced motion, отсутствие внешних ресурсов.

## Фактические проверки

| TASK | Маршрут | Результат | Ключевое evidence |
| --- | --- | --- | --- |
| RD-05 | R1 Pro → R2 Codex (vision) | **PASS**, F1/F2 MINOR | 20 native screenshots, targeted 33 OK, diff только 4 product/test файла |
| RD-06 | R2 Codex C1/C2 | C1 FAIL (RD06-F01 evidence) → **C2 PASS**, F01 CLOSED, F02 MINOR | новый installer, 34 screenshots, изолированная установка с backup/restore |
| RD-07 | R0 verifier | **PASS** | полный suite ровно один раз: `Ran 167 tests in 2.126s`, **OK**, exit 0 |
| Stage | Codex R3 `gpt-6-astra` high | **PASS** | mapping scope→evidence, artifact/review accounting, без budget reset |

R1 Pro вернул capability-BLOCKED (у модели нет image input), поэтому визуальная
приёмка RD-05 явно передана vision-capable Codex R2; это не failed review и не
дополнительный цикл. Раскладка ревью сохранена: RD-01 1 full/0 FAIL/0 Codex;
RD-02 1/0/1; RD-03 2/1/2 (третьего RD-03/A1 нет); RD-05 1/0/1; RD-06
2/1/2; RD-07 R0; stage R3 1. Бюджеты не обнулялись.

## Артефакт (локальный, неподписанный)

- **Новый installer:** `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`
  — **15 286 980 байт**, SHA256
  `71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08`.
- Packaged exe: `dist/GasProjectCalculator/GasProjectCalculator.exe` —
  6 836 651 байт, SHA256
  `5403540C4172779ED6F97381A9618FE423D0915A6BEC1710BAE2B578F6ACDD2C`;
  совпадает с installed exe в evidence.
- Прежний проверенный installer сохранён:
  `installer/Output/legacy/GasProjectCalculator-Setup-1.0.0-pre-compact.exe` —
  15 273 647 байт, SHA256 `04388410…949A`. Более ранний
  `…-previous-stage.exe` (15 256 037 байт, `2973278F…428F`) не тронут.
- Installer пересобран из нового dist; установка проверена изолированно
  (`/DIR` temp, backup/restore HKCU-ключа и ярлыка). Пользовательская
  установка по умолчанию и её запущенный PID 13248 не изменялись. После
  проверки test instance удалён, test-портов/окон не осталось.

Чтобы получить новую версию, запустите новый installer: per-user установка
обновит существующее приложение. Push/merge/deploy/release/signing не
выполнялись.

## Отклонения и остаточные риски

- Основной визуальный образец был уточнён пользователем уже во время RD-05;
  работа была доведена до `original-window-splash-reference.png` до первого
  полного review, с записью в APPROVALS/ARCHITECTURE/ROADMAP.
- RD-05 F1 (MINOR): подписи 10,5–11,5 px ниже ориентира 13–14 px при
  body/input 13 px; читаемость подтверждена 1:1 PNG — backlog.
- RD-05 F2 (MINOR): `--eval-bridge` — opt-in локальная диагностика, default
  `None`, без listener и без активации обычным запуском — backlog.
- RD-06 F02 (MINOR): вспомогательный mobile result-PNG не использовать как
  доказательство scrollY=45; основной mobile proof достаточен.
- RD-COMPACT-N01 (MINOR) исправлен финальным STATE — актуальный next-owner.
- Известные ограничения: installer неподписан (возможен SmartScreen); проверка
  выполнена в одной Windows/WebView2/DPI96 среде; reduced motion проверен
  эмуляцией; формальные права на эмблему не подтверждены.

## Итог

Все согласованные TASK корректирующего этапа приняты routed review, полный
suite прошёл на финальном интегрированном состоянии, Codex R3 принял этап.
Проверенный локальный installer и отчёт переданы; продуктовые вычисления/API
не изменены.
