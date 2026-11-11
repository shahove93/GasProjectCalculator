# Evidence — TASK GSV-01 (R1, A1/C1)

- Baseline: `1b533ac` (ветка `feature/gsv`); workspace `D:/Antigravity/GasProjectCalculator`.
- Implementer: Orca dispatch `ctx_d1f4b5534011`, task `task_4e374c18335e`,
  agent opencode, requested model `deepseek/deepseek-flash`.
- State on submission: `app/gsv_calculator.py` и `tests/test_gsv_calculator.py`
  untracked; других изменений нет (`git status --short` содержит только эти два
  файла; `git diff --stat` пуст, т.к. файлы новые).
- Реализация: 9 публичных функций, точная целочисленная арифметика, ValueError
  на невалидных входах. Тестов: 48.

## Выполненные проверки

Причина однократного повторного запуска координатором по review-policy: в
отчёте исполнителя не было сохранённого лог-артефакта, только inline-вывод.

1. Команда: `.\.venv\Scripts\python.exe -m unittest tests.test_gsv_calculator -v`
   CWD: `D:/Antigravity/GasProjectCalculator`
   Exit code: `0`
   Результат: `Ran 48 tests in 0.001s` — `OK`.
   Log: `docs/workflow/evidence/logs/GSV-01-unit.log`.
2. Команда: `.\.venv\Scripts\python.exe -m unittest discover -s tests`
   CWD: `D:/Antigravity/GasProjectCalculator`
   Exit code: `0`
   Результат: `Ran 105 tests in 0.074s` — `OK` (57 старых + 48 новых).
   Log: `docs/workflow/evidence/logs/GSV-01-suite.log`.

## Отчёт исполнителя (inline)

Создан `app/gsv_calculator.py` по замороженному контракту; тесты покрывают
примеры VISION (63000/105525/105525/67200/96600), границы и ошибки; изменения
вне allowlist отсутствуют; коммит не выполнялся.

## Frozen checklist GSV-01

A1 модуль без HTTP/UI импортов; A2 база 60000/80000 до 5 м; A3 тарифы длины
2500/3500/4000 по диаметрам ≤25/26–40/41–57; A4 диаметр 1..57, >57 и 0 —
ValueError; A5 бурение 0/8000/10000; A6 САКЗ ×14000; A7 ПК 4000 только при
САКЗ≥1, иначе ValueError; A8 район 7000; A9 НДС 5% и total; A10 пять примеров
VISION точно; A11 ошибки отрицательных/дробных/неверных значений; A12 полный
suite 105 OK, diff только в allowlist.
