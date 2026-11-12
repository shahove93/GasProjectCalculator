# MD-04 review record — R0 coordinator acceptance

- TASK: **MD-04** README/screenshots/docs 1.1.0; risk **R0**, no Codex.
- Implementer: OpenCode Flash dispatch `ctx_ad932786f52d`
  (`task_e4d3a03ba69f`); baseline `d08148c014f66193ad5049f4cdfd427ee0076c52`.
- Coordinator acceptance by frozen checklist T1–T6 on evidence:
  - **T1 PASS:** README describes three independent lengths, single 5 m base,
    cheapest-first order до Ø25 → Ø32–40 → Ø57, rates 2500/3500/4000,
    zero-surcharge ≤5 m and base-only all-zero case.
  - **T2 PASS:** D1–D5 and combined 151000/7550/158550 match MD-01/MD-03
    evidence; `MD-04-numbers-check.txt` all True.
  - **T3 PASS:** installer 1.1.0 path/size 15 293 993 B/SHA256
    `3BFFFFB2…B710` re-checked; release v1.0.0 explicitly not replaced.
  - **T4 PASS:** 18 relative links checked, MISSING_COUNT=0; new MD-02/MD-03
    screenshots exist.
  - **T5 PASS:** developer/three-mode/RU install-uninstall/user-file facts
    preserved; no signing/publication-of-1.1.0/telemetry claims.
  - **T6 PASS:** only `README.md` changed (56+/19−); other new files are
    allowed MD-04 evidence/logs; hash facts real.
- Reviewer/acceptance author: coordinator (R0); Codex calls 0.
- **MD-04 ACCEPTED**; scoped commit owned by coordinator; next TASK MD-05
  (integrated full suite).
