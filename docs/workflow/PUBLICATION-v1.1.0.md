# Публикация СС.Расчет 1.1.0 — COMPLETE

2026-11-12. Пользователь подтвердил публикацию новой версии; последующей фразой
«Можешь ссылку мне не присылать, найду» отменил отправку ссылки/письма.
Письмо не отправлялось, контакты в этом отчёте не публикуются.

- Принятый этап: FINAL-REPORT-MIXED-GSV.md, baseline9dea625, product557fe2d,
  stage final cb8c87b, 219 tests OK и Codex stage acceptance PASS.
- Publication commit/tag target: ef057adf76c85f4256e8177d7e93a1be2df51762.
  К принятому cb8c87b добавлены только README/release notes/checksum/records.
- Ветка feature/gsv-mixed-diameters и default main опубликованы обычным push,
  main обновлён fast-forward9dea625→ef057ad, force/delete не применялись.
- Release id442672288, tagv1.1.0, draft=false, prerelease=false, Latest.
- Installer SS-Raschet-Setup.exe asset738698226, 15 293 993 B, SHA256
  3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710.
- SHA256SUMS.txt asset738698772,87B. Server digest совпал до публикации.
- Публичное скачивание через releases/latest/download/SS-Raschet-Setup.exe
  без credentials: HTTP200,15293993B, hash совпал с принятой сборкой.
  SHA256SUMS.txt также HTTP200. Rebuild/нового suite не было.
- v1.0.0 и его asset/tag не изменялись. Неподписанность/SmartScreen и
  recorded NIT с обрезанием вентиля сохраняются, продукт не менялся.

GitHub CLI не авторизован, release-upload capability connector отсутствует;
использован GitHub REST через существующий Git credential helper без записи
credential в файл/вывод. Механическая публикация R0, counters без reset.
Финальный docs-only commit сохраняет этот отчёт и обновляет STATE/HISTORY;
установщик и tag target неизменны.
