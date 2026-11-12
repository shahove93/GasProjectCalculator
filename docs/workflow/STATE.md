# Состояние проекта

**СС.Расчет 1.1.0 опубликован — COMPLETE** (2026-11-12).

- main и feature/gsv-mixed-diameters содержат принятый mixed-GSV этап и
  README с актуальным скриншотом/кнопкой скачивания.
- Latest release v1.1.0 (id442672288), tag target
  ef057adf76c85f4256e8177d7e93a1be2df51762.
- SS-Raschet-Setup.exe:15 293 993B, SHA256
  3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710.
  HTTP200 публичного скачивания/hash проверены; SHA256SUMS.txt приложен.
- Предыдущий releasev1.0.0 и assets/tag сохранены, не заменялись.
- Отправка ссылки/письма отменена пользователем, письмо не отправлялось.

## Принятый продукт

Три отдельные длины ГСВ доØ25/Ø32–40/Ø57 в отдельном/общем расчёте;
база5м из самых дешёвых первыми, серверный метраж/детализация,
legacy API без breaking changes. Новые header/footer SVG по референсам,
compact800×540/min760×520, русская заставка/installer1.1.0.
Stage product557fe2d, verification0431c0b, finalcb8c87b;219 tests OK,
Codex Astra stage PASS. MD-01 C1FAIL→C2PASS (explicit-null422 исправлен),
MD-02/03 PASS,MD-04/05 R0PASS. Старые counters/история сохранены.
NIT MD02-N1:верх маховика слегка обрезан; unsigned/SmartScreen,
одна Windows/WebView2/DPI96 среда, combined inner scroll при min размере.
User установка/сессия и :8000/:8138 не затрагивались.

[Публикация1.1.0](PUBLICATION-v1.1.0.md),
[смешанные диаметры](FINAL-REPORT-MIXED-GSV.md),
[публикация1.0.0](PUBLICATION-v1.0.0.md),
[разрешения](APPROVALS.md),[история](HISTORY.md).
