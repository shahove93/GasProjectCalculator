# VP-02 / 1.2.0 — final stage acceptance (independent)

2026-11-12. **FINAL ACCEPTANCE: PASS.** Reviewer: real Orca Codex
**`gpt-6.1-sol`**, effort **`high`**, task `task_38ba500ce885`, dispatch
`ctx_059202c6763a`, terminal `term_d7b471f9-7afe-4b66-9195-d415ceb6daa7`.
Requested/effective confirmed in
`evidence/logs/VP-02-final-stage-effective.json`: `agent=codex`,
`model=gpt-6.1-sol`, `effort=high`. Different context from the implementer and
from the R2 reviewer; read-only; no files changed, no build/install/tests/
network re-run, no commit.

Baseline/HEAD `1689773718c818a4ebca400afc2d8a4206b6458e`, branch
`feature/gsv-mixed-diameters`.

## Criterion results

1. **Scope completeness — PASS.** Reused VP-01 PASS (V1–V12, MD02-N1 closed);
   live diff confirms accepted header/footer/splash products unchanged.
   Only installer branding/version/output-guard changed; no math, field order,
   mode names, or main-window geometry changes. VP-01 was not re-audited.
2. **Actual artifact — PASS.** `installer/Output/GasProjectCalculator-Setup-1.2.0.exe`:
   15 373 267 B, FileVersion 1.2.0.0, ProductVersion 1.2.0, SHA256
   `4579FB3AA7B2E6220C1204E3AA2A6048648AE5A344B8E2D45DD00CF19F856113`.
   Prior 1.0.0/1.1.0/legacy byte+SHA256 unchanged; no push/merge/deploy/release.
3. **Evidence sufficiency — PASS.** W1–W11 supported by primary evidence:
   build logs, artifact hashes, RU wizard 598×464, isolated cycle with
   4×exit 0 and exact HKCU/shortcut restore, native app without Python,
   target 800×540/min 760×520 with `scrollX=scrollY=0`, D1–D5
   75600/79275/71400/63000/70875 with `opacity=1`, combined
   151000/7550/158550, legacy/mixed/ПК 422, targeted 36 OK, full suite
   **219 OK/exit 0**, static 137 checks, manifest 5 artifacts / 48 screenshots
   (39 PNG + 9 JPEG named .png) / 106 user files, `git diff --check` 0.
4. **Scope/diff integrity — PASS.** Live diff: only
   `installer/GasProjectCalculator.iss`, `installer/build-installer.ps1` and
   three new `installer/assets` files as product changes; `app/frontend/
   packaging/requirements*/tests/backend/API/calculator` zero-diff.
5. **Independence — PASS.** VP-01 R2 (`ctx_fd6edd091391`), VP-02 R2
   (`ctx_df0f7573e041`) and this final acceptance (`ctx_059202c6763a`) are
   distinct real Codex `gpt-6.1-sol`/high contexts; the Astra implementer
   (`ctx_988a8c02d5c3`) did not accept its own work. Findings: MD02-N1 closed,
   VP02-R2-N1 closed; new BLOCKER/MAJOR/MINOR/NIT = 0/0/0/0.
6. **Completion readiness — PASS.** Ready for coordinator FINAL-REPORT/README/
   STATE and scoped local commit; commit intentionally pending, not a failure.

## Images viewed with vision

`docs/design/splash-installer-reference.jpg`,
`docs/screenshots/visual-02-native-splash.png`,
`visual-01-compare-header.png`, `visual-01-compare-footer.png`,
`visual-02-wizard-welcome.png`, `visual-02-wizard-finish.png`,
`visual-02-resumed-desktop-gsv-D1-settled.png`.

## Residual limits / NOT_RUN

- Reviewer did not re-run build/install/uninstall/lifecycle/API/browser/tests/
  static or query network/releases; preserved primary evidence was used.
- Not proven by this packet: clean VM without Python/WebView2, other DPI
  values, full OS packet capture, independent remote release re-query.
- Original GUI wrapper numeric exit is missing; compensated by finish/raw log
  and four cycle exits 0.
- Push/merge/deploy/release/signing remain unauthorized.
