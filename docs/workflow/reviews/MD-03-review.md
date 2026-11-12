# MD-03 review record

## C1 — R2 Codex review

- Reviewer: Codex `gpt-6.1-sol` high, dispatch `ctx_17fecbd4f9d8`,
  task `task_5cfeeca1c63c`, read-only.
- Baseline `fb080aa9dfcb7420fa83ff32cdc52e223ac96dd5`; A1/C1.
- Verdict: **PASS**, no BLOCKER/MAJOR/MINOR/NIT findings.
- Confirmed: actual tracked diff limited to two version lines in
  `installer/GasProjectCalculator.iss`; `app/`, `frontend/`, `tests/`,
  `requirements*` zero diff; extra review packet consistent with the task;
  reviewer changed no files, made no commit.
- B1–B12 confirmed from `MD-03-evidence.md` and raw `logs/MD-03-*`: builds
  exit 0; packaged/installed exe `F374EEED…459690`; real installer
  15 293 993 B, FileVersion `1.1.0.0`/ProductVersion `1.1.0`, AppId preserved,
  SHA256 `3BFFFFB2F7C7F73185B48B5AC5E5CDE06BF4197A1A3D4D0F66E763905AC5B710`;
  unchanged 1.0.0/legacy pre/post/final hashes; HKCU/shortcuts restored and
  user install 106 files/37 372 847 B/PID 13248 unchanged; RU wizard and
  optional Desktop; reinstall/uninstall preserved user files; Python-free
  launch with splash/readiness; loopback 127.0.0.1, occupied 8123→8124,
  close leaves no backend/children; mixed 75600/79275/71400/63000/70875,
  combined 158550, legacy/422/GSN/САКЗ/ПК/район/НДС; native target 800×540 /
  min 760×520 with action/total visible and accessible inner detail; local
  unsigned artifact without publication.
- Reviewer did not rerun build/install/runtime/hash (reuse rule).
- Counters MD-03: full reviews 1, failed 0, Codex calls 1/4.
- **MD-03 ACCEPTED**; scoped commit owned by coordinator; full suite remains
  deferred to MD-05; next TASK MD-04.
