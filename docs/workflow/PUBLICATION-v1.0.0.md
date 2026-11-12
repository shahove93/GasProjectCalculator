# Публикация СС.Расчет 1.0.0

2026-11-12 — COMPLETE. Пользователь явно разрешил опубликовать актуальную
версию на главной странице репозитория и скачивание установщика с другого ПК.
Механическая публикация R0, без изменения принятого продукта и его бюджетов.

## Доставка

- Repo: https://github.com/shahove93/GasProjectCalculator, default branch main.
- Принятый код и история: feature/ss-calculator-redesign, HEAD до оформления
  9ccc9c7; product revision 1af13d6.
- Publication source/tag target: e4e4deee6977bd36d0397d643be89b1afef58fea;
  изменения к 9ccc9c7 — только README, download badge, release notes/checksum
  и workflow records. Следующий docs-only commit сохраняет этот отчёт.
- Обычные git push (без force): branch и HEAD:refs/heads/main успешно.
  Main fast-forward с 2949223, сохранена вся история, ветки не удалялись.
- Release v1.0.0, id 442532779, draft=false, prerelease=false, Latest.
  URL: https://github.com/shahove93/GasProjectCalculator/releases/tag/v1.0.0.
- Asset SS-Raschet-Setup.exe, id 738208919, 15 286 980 B,
  SHA256 71232EE4E5A4656D3375EE95758F77038912FABC44F8658396D7E60752BA7E08.
  Имя отличается от локального; байты те же, сборка не повторялась.
- Asset SHA256SUMS.txt, id 738209344, 87 B.
- Repo description и homepage обновлены; homepage ведёт на Latest release.

## Проверено

1. GitHub repository metadata: public, default main, полномочия admin/push.
2. Remote main — предок локального HEAD, divergence отсутствовала.
3. GitHub releases/tags до публикации отсутствовали; ничего не заменялось.
4. Локальный installer hash совпадает с принятой компактной версией.
5. Проверка типовых secret-patterns в tracked text: совпадений нет.
6. Локальные ссылки/изображения README существуют; badge — корректный SVG;
   git diff --check пройден. Старый локальный путь скачивания заменён GitHub URL.
7. Draft release → загрузка exe/checksum → проверка server digest → publish.
8. Публичная загрузка без credentials по кнопке
   https://github.com/shahove93/GasProjectCalculator/releases/latest/download/SS-Raschet-Setup.exe
   — HTTP 200, 15 286 980 B, SHA256 совпал. SHA256SUMS.txt — HTTP 200, 87 B.
9. Product suite не повторялся: продукт не менялся, принятые 167 OK сохранены.

GitHub CLI был не авторизован; GitHub connector использован для repo metadata,
release upload capability отсутствует. REST publication использовала существующий
Git credential helper; credential только в памяти, в файлы/логи не записывался.
Первый create с сокращённым SHA не создал release (inspect подтвердил пустой
список); create с полным SHA выполнен один раз успешно. Нет дублированных releases.

Остаточные ограничения принятых этапов сохраняются: unsigned/SmartScreen,
WebView2, одна Windows/DPI96 среда; отдельное code signing не выполнялось.
