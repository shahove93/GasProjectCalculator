# VP-02 — independent R2 review (logical MD-03 / A2 / C1)

2026-11-12. Verdict: **PASS** (W1–W11), one **NIT** (VP02-R2-N1). No
BLOCKER/MAJOR/MINOR. Reviewer: real Orca Codex **`gpt-6.1-sol`**, effort
**`high`**; task `task_65c331479b7e`, dispatch `ctx_df0f7573e041`, terminal
`term_abc2c4e8-a62e-482e-9554-f0cf903681ef`, run `run_8e5d92ad57c7`.
Requested/effective confirmed in
`evidence/logs/VP-02-r2-effective.json` →
`result.worker.startOptions.launch.requested/effective`: `agent=codex`,
`model=gpt-6.1-sol`, `effort=high`.

Baseline/HEAD `1689773718c818a4ebca400afc2d8a4206b6458e`; branch
`feature/gsv-mixed-diameters`. Reviewer was read-only: no file changes, no
build/install/tests/API/network re-run; only live `git diff`/`git status` was
used to reconcile the saved diff with the current tree.

## Verdict by frozen criterion

| ID | Verdict | Key observed evidence |
| --- | --- | --- |
| W1 | PASS | PyInstaller/ISCC logs exit 0; dist EXE SHA256 `DD9AF548…E6888`; static check maps 111 installed payload files to dist; HEAD confirmed |
| W2 | PASS | `AppVersion`/`AppVerName` 1.2.0, `VersionInfoVersion` 1.2.0.0, prior AppId; artifact 15 373 267 B, FileVersion 1.2.0.0, ProductVersion 1.2.0 |
| W3 | PASS | Pre/post bytes+SHA256 identical for 1.0.0, 1.1.0 and both legacy installers; no publication action |
| W4 | PASS | All six 598×464 RU wizard images viewed; readable controls, Desktop task off; branded sidebar/header consistent with reference/splash; Inno 6.4.1, RU-only |
| W5 | PASS | Isolated Temp install 1.1.0 → upgrade 1.2.0 → reinstall → uninstall, each exit 0; HKCU/shortcuts exact restore; 106 user files unchanged |
| W6 | PASS | Installed EXE without CLI/Python (`pythonResolved=false`); splash 560×450, main 800×540/min 760×520; client 784×501/744×481, DPR=1; scroll [0,0]; action+total visible |
| W7 | PASS | D1–D5 75600/79275/71400/63000/70875 with cheapest-first 5 m; combined 151000/7550/158550; САКЗ/ПК/район/НДС; legacy/mixed 422; ГСН regression; five settled PNG viewed, `opacity=1` |
| W8 | PASS | Occupied 65531→chosen 65532, listener 127.0.0.1; close terminates backend/launcher with no children, no force kill; RU error/exit 1; reduced motion normal `gas-flow`, OS/flag `none`/0.8 |
| W9 | PASS | Upgrade/reinstall/uninstall exit 0; two user sentinel files retained; no network/signing; RU-only; prior bytes/user files restored |
| W10 | PASS | Live diff matches saved product diff: only installer iss/build script + three `installer/assets` files; `app/frontend/packaging/requirements*/tests` zero-diff; targeted 36 OK, full suite 219 OK/exit 0, static 137 checks, `git diff --check` 0 |
| W11 | PASS | Local artifact path/size/SHA256 correct; old artifacts intact; no push/merge/deploy/release |

## Finding

- **VP02-R2-N1 — NIT (evidence wording only).**
  `evidence/VP-02-evidence.md` says the manifest lists "48 real PNG", but
  `logs/VP-02-resumed-manifest.json` actually records **39 PNG + 9 JPEG**
  (the JPEGs are stored with `.png` filenames; six wizard and three old native
  frames). This does not affect vision review or W1–W11; the coordinator
  corrects the wording without re-shooting or a new review cycle.

## Images reviewed with vision (23)

`docs/design/splash-installer-reference.jpg`; `visual-02-wizard-welcome`,
`-dir`, `-tasks`, `-ready`, `-installing`, `-finish`; `visual-02-native-splash`;
`visual-02-resumed-native-target-gsn/gsv/combined`;
`visual-02-resumed-native-minimum-gsn/gsv/combined`;
`visual-02-resumed-native-startup-error`;
`visual-02-resumed-splash-os/flag/animated`;
`visual-02-resumed-desktop-gsv-D1..D5-settled`.

## Explicit NOT_RUN / residual limits

- Reviewer did not re-run installer/build/install/tests/API/browser/live
  app/network; it relied on preserved primary evidence.
- Clean VM without Python/WebView2, other DPI values, and full OS packet
  capture are not proven by this packet.
- Remote releases were not re-queried (network forbidden in review).
- The original GUI numeric wrapper exit is absent; compensated by finish/raw
  log and four cycle exits 0.
- This R2 PASS does **not** replace the separate final stage acceptance.
