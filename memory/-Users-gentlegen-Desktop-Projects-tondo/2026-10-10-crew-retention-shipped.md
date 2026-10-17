---
name: 2026-10-10-crew-retention-shipped
description: "Crew-lite + Render-ready hosting built on branch crew-retention (PR gentritr1/tondo#2, open); what is verified, what Task 10 (owner-gated deploy) still must prove"
metadata:
  node_type: memory
  type: project
  originSessionId: 3fb08f38-07c3-4529-b2e2-21cde8419a74
  modified: 2026-10-10T11:36:30.159Z
---

**State on 2026-10-10:** crews and the Render-ready hosting work are built on branch `crew-retention`, 25 commits, head 4ea121c. PR https://github.com/gentritr1/tondo/pull/2 is open against main and NOT merged. The repo has no CI.
- The owner accepted the T7/T8 screen captures.
- The playbook lessons are in PR https://github.com/gentritr1/agent-playbooks/pull/1, also open.
- The plan's own docs: `docs/superpowers/specs/2026-10-10-crew-retention-design.md` and `docs/superpowers/plans/2026-10-10-crew-retention.md`.
- The ledger with every ruling: `.superpowers/sdd/2026-10-10-crew-retention/progress.md` (git-ignored; kept until Task 10).

**Verified locally (real runs):**
- 202 tests.
- A real 4-slice pie saved to a crew, also with ONLY the portable env vars (`npm run check:portable`).
- A headless browser opened `/?crew=<id>` against a real server; Start a table reached the lobby with the crew attached.
- Shoot gates `crew-save-fits`, `crew-card-fits` and `live-regions-rendered`, each sabotage-proven.

**NOT verified, all in plan Task 10, which needs the owner's accounts and an explicit yes per outward step:**
- DONE 2026-10-10: Render is behind Cloudflare; TONDO_TRUST_PROXY=1 was WRONG (shared 10.x hop). TONDO_CLIENT_IP_HEADER=CF-Connecting-IP verified live (real IP logged; forged header 403).
- Neon: wake time, `statement_timeout` / `query_timeout` on a real stuck query, the wrong-password drill, and compute suspending after 10 min idle (DATA-005 measurement).
- `FOR UPDATE` concurrency.
- Real phones and real screen-reader speech.
- Node 20 is EOL: test on 22/24 before launch.

**Why:** the owner's next step is the deploy: Render free now, Fly later ([[hosting-free-tier-facts]]).
**How to apply:** start the next session at plan Task 10. Before reaching for something new, read the ledger's `Parked:` and `minor (deferred)` lines.

Related: [[brief-predicted-red-is-a-hypothesis]].
