---
name: appcare-next-projects-research
description: "Oct 2026 AppCare \"next level\" security research — report path, baseline branch, top-3 ranking, and code-vs-copy mismatches found"
metadata:
  node_type: memory
  type: project
  originSessionId: 613e518a-c988-496b-b044-35f6a8efbfb4
  modified: 2026-10-12T22:52:20.903Z
---

Report: `design/appcare-research/REPORT.md` (untracked, not committed), notes in `design/appcare-research/research_notes/`. Written 2026-10-13.

- AppCare code lives in `~/Desktop/SlopRemover`. The scanner is on `origin/feat/dashboard` (fa78639), not on the checked-out `feat/landing-next-level`. Earlier competitor research is on `feat/claude-platform` (`research/out/competitors.md`, `landing-teardown.md`). Read branches with `git show`; never check one out (the owner's tree stays on the landing branch).
- Top 3 (inferred ranking): (1) Probe 2.0: the anonymous probe only knows legacy JWT anon keys, Supabase retires them in late 2026, and the grant change lands 2026-10-30. (2) Prove anonymous write/delete/RPC exposure from the catalog, without writing. (3) What a leaked AI or paid-API key can spend.
- The landing copy names Gitleaks, Splinter, ZAP and OSV-Scanner, but the checks are custom TypeScript. It also says "AI ranks severity", which the code does not do.
- Owner ruled "no free check" on 2026-10-09.

**Why:** the owner asked which security projects take AppCare to the next level. The main session uses this for brand/landing showcase decisions.
**How to apply:** start from this report instead of redoing the research. Re-check the Supabase key and grant dates before acting on them. Related: [[brand-3d-fresh-direction]].
