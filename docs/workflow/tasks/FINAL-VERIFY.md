# FINAL verification — integrated Windows installer stage (R0 evidence)

## Authority

Approved Windows installer stage (AGENTS.md, ARCHITECTURE.md, ROADMAP.md steps
8–9, APPROVALS.md 2026-11-11). WI-01, WI-02 and WI-03 are accepted and
committed. You are the OpenCode verification worker. Make no product changes and
do not award project PASS; the coordinator records R0 checklist acceptance and
Codex performs the final R3 stage acceptance afterwards.

## Baseline

- Branch/worktree: `feature/windows-installer`,
  `D:/Antigravity/GasProjectCalculator`.
- Accepted commits: WI-01 `7fab960`; WI-02 `144a75c`; WI-03 `9eaed0a`.
- Expected installer artifact:
  `installer\Output\GasProjectCalculator-Setup-1.0.0.exe`,
  15 256 037 bytes, SHA256
  `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`.
  Verify it yourself; do not trust this line.

## Allowed changes

- New evidence only: `docs/workflow/evidence/FINAL-WINDOWS-INSTALLER-EVIDENCE.md`
  and `docs/workflow/evidence/logs/FINAL-*-*.txt`.
- Do NOT edit application code, packaging, installer scripts, README or planning
  documents. Do NOT commit, push, merge, deploy or publish.

## Required verification (reuse accepted evidence, do not rebuild)

No source change occurred after the accepted WI-02 artifact, so do not rebuild
the app or installer and do not repeat install/uninstall unless a real evidence
gap exists. Verify and consolidate:

1. `git diff 144a75c..9eaed0a --stat` (and `--name-only`) shows only docs/README/
   evidence/review changes — no app, packaging, installer, tests or requirements
   change.
2. Artifact exists at the exact path, size 15 256 037 bytes, SHA256
   `2973278F47A4A2A479177B12A4C4CCA01ED59D1CA8D2D9CE107C4E7A2E37428F`.
3. Run the full suite once on the integrated final state:
   `.\.venv\Scripts\python.exe -m unittest discover -s tests` → 146 OK, exit 0.
   Save raw log.
4. Confirm the user's developer uvicorn on port 8000 is untouched (or note it if
   no longer running); do not stop it.
5. Confirm README points to the exact artifact path/hash and keeps the developer
   path.
6. Map every stage frozen checklist item to its accepted evidence:
   clean x64 build; installer + Start Menu + optional Desktop shortcuts; no
   Python/terminal prerequisite; first launch readiness; all three modes;
   localhost-only + port conflict; window close exits backend; understandable
   failure; install/uninstall preserves user files; developer uvicorn path;
   README directs to installer.
7. Record residual risks/backlog: `WI02-R1-F1` MINOR, second-machine validation
   not available, unsigned artifact/SmartScreen, WebView2 requirement.

## Evidence format

Write `docs/workflow/evidence/FINAL-WINDOWS-INSTALLER-EVIDENCE.md` with: final
revision, baseline, commands, CWD, exit codes, results, artifact path/size/hash,
the checklist-to-evidence map, NOT_RUN items, and a statement that no product
change was made. Raw logs under `docs/workflow/evidence/logs/FINAL-*.txt`.
A success assertion alone is insufficient; include exact command output.

## Reporting

Return: what you verified, evidence paths, suite result, artifact hash, any
deviation or gap. Do not claim project PASS.
