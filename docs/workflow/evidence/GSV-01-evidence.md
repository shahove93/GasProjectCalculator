# Evidence вЂ” TASK GSV-01 (R1, A1/C1)

- Baseline: `1b533ac` (РІРµС‚РєР° `feature/gsv`); workspace `D:/Antigravity/GasProjectCalculator`.
- Implementer: Orca dispatch `ctx_d1f4b5534011`, task `task_4e374c18335e`,
  agent opencode, requested model `deepseek/deepseek-flash`.
- State on submission: `app/gsv_calculator.py` Рё `tests/test_gsv_calculator.py`
  untracked; РґСЂСѓРіРёС… РёР·РјРµРЅРµРЅРёР№ РЅРµС‚ (`git status --short` СЃРѕРґРµСЂР¶РёС‚ С‚РѕР»СЊРєРѕ СЌС‚Рё РґРІР°
  С„Р°Р№Р»Р°; `git diff --stat` РїСѓСЃС‚, С‚.Рє. С„Р°Р№Р»С‹ РЅРѕРІС‹Рµ).
- Р РµР°Р»РёР·Р°С†РёСЏ: 9 РїСѓР±Р»РёС‡РЅС‹С… С„СѓРЅРєС†РёР№, С‚РѕС‡РЅР°СЏ С†РµР»РѕС‡РёСЃР»РµРЅРЅР°СЏ Р°СЂРёС„РјРµС‚РёРєР°, ValueError
  РЅР° РЅРµРІР°Р»РёРґРЅС‹С… РІС…РѕРґР°С…. РўРµСЃС‚РѕРІ: 48.

## Р’С‹РїРѕР»РЅРµРЅРЅС‹Рµ РїСЂРѕРІРµСЂРєРё

РџСЂРёС‡РёРЅР° РѕРґРЅРѕРєСЂР°С‚РЅРѕРіРѕ РїРѕРІС‚РѕСЂРЅРѕРіРѕ Р·Р°РїСѓСЃРєР° РєРѕРѕСЂРґРёРЅР°С‚РѕСЂРѕРј РїРѕ review-policy: РІ
РѕС‚С‡С‘С‚Рµ РёСЃРїРѕР»РЅРёС‚РµР»СЏ РЅРµ Р±С‹Р»Рѕ СЃРѕС…СЂР°РЅС‘РЅРЅРѕРіРѕ Р»РѕРі-Р°СЂС‚РµС„Р°РєС‚Р°, С‚РѕР»СЊРєРѕ inline-РІС‹РІРѕРґ.

1. РљРѕРјР°РЅРґР°: `.\.venv\Scripts\python.exe -m unittest tests.test_gsv_calculator -v`
   CWD: `D:/Antigravity/GasProjectCalculator`
   Exit code: `0`
   Р РµР·СѓР»СЊС‚Р°С‚: `Ran 48 tests in 0.001s` вЂ” `OK`.
   Log: `docs/workflow/evidence/logs/GSV-01-unit.txt`.
2. РљРѕРјР°РЅРґР°: `.\.venv\Scripts\python.exe -m unittest discover -s tests`
   CWD: `D:/Antigravity/GasProjectCalculator`
   Exit code: `0`
   Р РµР·СѓР»СЊС‚Р°С‚: `Ran 105 tests in 0.074s` вЂ” `OK` (57 СЃС‚Р°СЂС‹С… + 48 РЅРѕРІС‹С…).
   Log: `docs/workflow/evidence/logs/GSV-01-suite.txt`.

## РћС‚С‡С‘С‚ РёСЃРїРѕР»РЅРёС‚РµР»СЏ (inline)

РЎРѕР·РґР°РЅ `app/gsv_calculator.py` РїРѕ Р·Р°РјРѕСЂРѕР¶РµРЅРЅРѕРјСѓ РєРѕРЅС‚СЂР°РєС‚Сѓ; С‚РµСЃС‚С‹ РїРѕРєСЂС‹РІР°СЋС‚
РїСЂРёРјРµСЂС‹ VISION (63000/105525/105525/67200/96600), РіСЂР°РЅРёС†С‹ Рё РѕС€РёР±РєРё; РёР·РјРµРЅРµРЅРёСЏ
РІРЅРµ allowlist РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‚; РєРѕРјРјРёС‚ РЅРµ РІС‹РїРѕР»РЅСЏР»СЃСЏ.

## Frozen checklist GSV-01

A1 РјРѕРґСѓР»СЊ Р±РµР· HTTP/UI РёРјРїРѕСЂС‚РѕРІ; A2 Р±Р°Р·Р° 60000/80000 РґРѕ 5 Рј; A3 С‚Р°СЂРёС„С‹ РґР»РёРЅС‹
2500/3500/4000 РїРѕ РґРёР°РјРµС‚СЂР°Рј в‰¤25/26вЂ“40/41вЂ“57; A4 РґРёР°РјРµС‚СЂ 1..57, >57 Рё 0 вЂ”
ValueError; A5 Р±СѓСЂРµРЅРёРµ 0/8000/10000; A6 РЎРђРљР— Г—14000; A7 РџРљ 4000 С‚РѕР»СЊРєРѕ РїСЂРё
РЎРђРљР—в‰Ґ1, РёРЅР°С‡Рµ ValueError; A8 СЂР°Р№РѕРЅ 7000; A9 РќР”РЎ 5% Рё total; A10 РїСЏС‚СЊ РїСЂРёРјРµСЂРѕРІ
VISION С‚РѕС‡РЅРѕ; A11 РѕС€РёР±РєРё РѕС‚СЂРёС†Р°С‚РµР»СЊРЅС‹С…/РґСЂРѕР±РЅС‹С…/РЅРµРІРµСЂРЅС‹С… Р·РЅР°С‡РµРЅРёР№; A12 РїРѕР»РЅС‹Р№
suite 105 OK, diff С‚РѕР»СЊРєРѕ РІ allowlist.

