# MD-03 R2 review packet (Codex gpt-6.1-sol high)

## Task

- Project TASK: **MD-03** — пересборка локального installer 1.1.0 и проверка
  реальной установленной программы.
- Risk **R2**; approach/cycle **A1/C1**; reviewer — independent Codex
  `gpt-6.1-sol` high.
- Baseline: `fb080aa9dfcb7420fa83ff32cdc52e223ac96dd5`;
  branch `feature/gsv-mixed-diameters`. Submission — uncommitted working tree;
  reviewer files не меняет и не коммитит.
- Perimeter: `installer/GasProjectCalculator.iss` (tracked diff),
  `installer/Output/GasProjectCalculator-Setup-1.1.0.exe` (git-ignored local
  artifact), `docs/screenshots/md-03-*`, `docs/workflow/evidence/MD-03-*`,
  `docs/workflow/evidence/logs/MD-03-*`.
  Product code `app/`, `frontend/`, `tests/` must have zero diff.

## Frozen checklist (verbatim `docs/workflow/tasks/MD-03.md`)

| ID | Criterion |
| --- | --- |
| B1 | Packaged app и installer 1.1.0 собраны из MD-02; exit 0 |
| B2 | VersionInfo/installer metadata = 1.1.0; AppId сохранён |
| B3 | 1.0.0, legacy bytes и опубликованный release не изменены |
| B4 | Изолированная установка; пользовательская установка/HKCU/ярлыки восстановлены |
| B5 | Установленная программа без Python/CLI; splash/readiness |
| B6 | Mixed 75600/79275/71400/63000/70875 и combined 158550 в установленной версии |
| B7 | Три длины, метраж, детализация видимы; legacy/422 проверены |
| B8 | ГСН-регрессия, САКЗ/ПК/район/НДС корректны |
| B9 | Loopback-only, занятый test-порт, закрытие завершает backend |
| B10 | Русский wizard, Start Menu/optional Desktop, reinstall/uninstall с сохранением user files |
| B11 | Нет diff в app/frontend/tests/requirements; suite отложен в MD-05 |
| B12 | Артефакт локально; signing/push/merge/deploy/release отсутствуют |

## Key facts to verify

- Installer 1.1.0: `installer/Output/GasProjectCalculator-Setup-1.1.0.exe`,
  15 293 993 B, SHA256
  `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710`.
- Unchanged: 1.0.0 15 286 980 B / `71232EE4…A7E08`; legacy
  `04388410…949A` (15 273 647 B) and `2973278F…2428F` (15 256 037 B).
- Version: FileVersion `1.1.0.0`, ProductVersion `1.1.0`, AppId preserved.
- Isolated install dir under `C:\Users\user\AppData\Local\Temp\opencode\md-03`;
  user install `%LOCALAPPDATA%\Programs\GasProjectCalculator` /
  PID 13248 unchanged (106 files, 37 372 847 B, same exe SHA256).
- Installed app: splash 520×320, target 800×540, min 760×520, DPI 96; close
  releases backend and leaves no children.

## Evidence supplied

- `docs/workflow/evidence/MD-03-evidence.md` — baseline/scope, build/artifact
  chain, pre/post hashes, isolated install/backup/restore, wizard/reinstall/
  uninstall, runtime/lifecycle, native metrics, B1–B12, NOT_RUN.
- `docs/workflow/evidence/logs/MD-03-*` — build exits, toolchain, versioninfo,
  hashes, install/restore, wizard, runtime, native JSON/summary, API, scope.
- Screenshots: `docs/screenshots/md-03-*` (wizard RU, splash, native
  target/min all modes + D1–D5, combined detail, 422).
- Tracked diff: `git diff fb080aa -- installer/GasProjectCalculator.iss`.

## Review instructions

1. Inspect the actual diff and evidence; confirm only
   `installer/GasProjectCalculator.iss` changed in tracked product scope and no
   unexpected files. Confirm 1.0.0/legacy/release bytes are unchanged (recorded
   pre/post hashes; one bounded hash check allowed if considered ambiguous).
2. Verify B1–B12 against logs/screenshots and the actual installer metadata.
   With complete, unambiguous evidence do not rerun build/install/runtime
   checks (reuse rule). The full suite is intentionally deferred to MD-05.
3. Confirm the installed app's mixed/legacy/GSN/САКЗ/ПК/НДС values, compact
   native viewport with visible action+total, loopback/port/close lifecycle,
   RU wizard/reinstall/uninstall user-file preservation, and that the normal
   user install/session was untouched.
4. Report findings with ID/criterion/location/observed/expected/severity/
   closure evidence. MINOR/NIT do not fail. Do not modify files or commit.
5. Return exactly one verdict: **PASS**, **FAIL** (BLOCKER/MAJOR) or
   **BLOCKED**; end your turn after the verdict.
