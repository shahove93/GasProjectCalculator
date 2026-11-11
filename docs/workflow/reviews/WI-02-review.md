# WI-02 review record — Inno Setup installer

- Logical TASK: WI-02; risk class R2; approach A1; cycle C1 (first full review).
- Branch/worktree: `feature/windows-installer`,
  `D:/Antigravity/GasProjectCalculator`.
- Baseline: `7fab9606ae4f704fe82cafa1caa1e4091b175533` (WI-01 PASS).
- Implementer: OpenCode `deepseek/deepseek-flash`, dispatch `ctx_ba47202b5ed0`,
  task `task_350718a368b4`.
- Reviewer: Codex `gpt-6.1-sol` high, dispatch `ctx_5ec0b1f12577`,
  task `task_57bb5b55d7aa`.
- Evidence pack: `docs/workflow/evidence/WI-02-evidence.md` and
  `docs/workflow/evidence/logs/WI-02-*`.
- Frozen checklist: `docs/workflow/tasks/WI-02.md`.

## Verdict

**PASS**, with one MINOR backlog finding and no BLOCKER/MAJOR findings.

- I1 genuine Inno Setup 6.4.1 build; artifact
  `installer/Output/GasProjectCalculator-Setup-1.0.0.exe`, 15 256 037 bytes,
  SHA256 `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`.
- I2–I11 verified from supplied evidence: non-admin HKCU silent installs exit 0;
  Start Menu target/args correct; optional Desktop present/absent as expected;
  Python-free GUI launch; readiness before window; mode totals
  131250/105525/145950; loopback 8124 after occupied 8123; close exits 0 with no
  listener/children; native failure dialog exit 1; both uninstalls preserve all
  three user markers.
- I12: reused WI-01 developer-uvicorn evidence; no application/API diff; suite
  146 OK.
- Toolchain deviation accepted within scope: the task-specified ISCC directory
  lacked `ISCmplr.dll`; the build script validated candidates and used the local
  full Inno Setup 6.4.1 distribution without system installation or config change.
- x86 setup bootstrap/32-bit logged install mode is not a violation: the payload
  is AMD64 and `ArchitecturesAllowed=x64compatible` gates targets.

## Backlog (outside frozen checklist, no correction cycle)

- `WI02-R1-F1` MINOR — `installer/verify-runtime.ps1:22-23` recursively deletes
  an arbitrary caller-supplied `WorkDir` after only `GetFullPath`; a verification
  helper should restrict cleanup to its own dedicated scratch directory. Closure
  requires bounded scratch ownership/path validation and a safe demonstration
  that unrelated existing directories are refused. Carried to FINAL-REPORT.

## Accounting

- Codex calls used for WI-02: 1 (C1 full review, PASS). Cap: 4 calls / 3M input
  tokens for R2. No provider-limit failure.
- Reviewer made no repository changes; all execution evidence reused without
  rerunning build/install/runtime/tests.
