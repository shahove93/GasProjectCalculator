# Состояние проекта

**Корректирующий этап компактности — COMPLETE** (2026-11-12). RD-05, RD-06,
RD-07 и Codex R3 stage acceptance **PASS**. Отчёт:
[FINAL-REPORT-COMPACT-CORRECTION](FINAL-REPORT-COMPACT-CORRECTION.md).

- Ветка `feature/ss-calculator-redesign`; продуктовая ревизия `1af13d6`;
  baseline этапа `4b0be03`. Рабочее дерево после docs-commit чистое.
- Итог: окно 800×540/min 760×520 (client 784×501/744×481, DPI96; 55,6%
  прежней площади), плотная композиция по
  `original-window-splash-reference.png`, отдельный блок опций, result справа,
  нижняя труба. Действие/итог при scrollY=0, mobile 390 без h-overflow.
- Поведение сохранено: 131250/105525/145950, САКЗ/ПК, switch/422, API/
  calculators/requirements без diff; полный suite 167 OK exit 0.
- Артефакт: `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`,
  15 286 980 B, SHA256
  `71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08`.
  Legacy pre-compact — 15 273 647 B `04388410…949A`; previous-stage
  `2973278F…428F` не тронут.
- Счётчики: RD-01 1/0/0; RD-02 1/0/1; RD-03 2/1/2; RD-05 1/0/1 (R1 Pro
  capability-BLOCKED, не failed); RD-06 2/1/2 (RD06-F01 CLOSED); RD-07 R0;
  stage R3 1. Прежние FAIL/история сохранены, бюджет не обнулялся.
- Backlog/риски: RD-05 F1 (подписи 10,5–11,5 px), F2 (`--eval-bridge` opt-in),
  RD-06 F02 (вспомогательный mobile result-PNG), неподписанный installer/
  SmartScreen, одна Windows/WebView2/DPI96 среда, reduced motion эмуляцией,
  права на эмблему не подтверждены. RD-COMPACT-N01 закрыт этим STATE.
- `:8000` PID12888, `:8138` PID23152 и пользовательская установка/PID13248
  не изменены; test-портов/окон не осталось. Push/merge/deploy/release/
  signing не выполнялись.
- Предыдущие этапы: [ГСВ](FINAL-REPORT.md),
  [Windows installer](FINAL-REPORT-WINDOWS-INSTALLER.md),
  [редизайн](FINAL-REPORT-SS-RASCHET-REDESIGN.md).
- Разрешения [APPROVALS](APPROVALS.md), инструкции [AGENTS](../../AGENTS.md).
