# Memory index

- [Product roadmap](product-roadmap.md) — THE north star: scope freeze, 4 phases, never-build list, strategic order. Read before proposing any feature.
- [Market research 2026-07](market-research-2026-07.md) — competitor table (fjaleza/fjalth match our digraphs!), positioning = trust+editorial bundle, streak forgiveness open question.
- [Retention plan 2026-08](retention-plan-2026-08.md) — Rrethi/challenges/motion plan; **M1 nine endpoints implemented 2026-08-11, gate OFF, 251 tests green**; 3 contract defects fixed as deviations D6/D7/D8; open: real-Neon race run, browser Cache-Storage check, native copy pass, flip REWARDS_ENABLED before the Shenja store screenshot ships.

- [Dev environment gotchas](dev-environment-gotchas.md) — Node 14 default breaks checks (use nvm 24), port 3000 taken, synthetic typing doesn't reach the game.
- [Daily pool immutability](daily-pool-immutability.md) — first 62 answers are SHA-pinned; append-only; growing the daily pool needs an epoch scheme + user sign-off.
- [Archive verification technique](archive-verification-technique.md) — date-dependent features need a clock-shim server; diff profile JSON to prove streak invariance.
- [pglite Neon bridge](pglite-neon-bridge.md) — Neon adapter SQL vs real WASM Postgres, no database: now in-repo (scripts/neon-pglite-bridge.mjs, `npm run test:neon-bridge`, CI neon-bridge job, 27aeb65).
- [Review scars](review-scars.md) — timer boundaries need fake-clock runs at T-30s; grids need 320px screenshots; generated Albanian copy is unverified until native pass.
- [Git remote](git-remote.md) — github.com:gentritr1/fjale.git, main; push authorized; agent rounds = atomic commits/worktrees.
- [Hint-attempt design](hint-attempt-design.md) — 2026-07-19 round: legacy saves keep free hint (deliberate), FJALË/ROSAK clues leak stems, SHA pin covers words only so clue edits are safe.
- [Art asset pipeline](art-asset-pipeline.md) — Recraft vector mode = true SVG, headless Chrome for OG PNG, JSON-LD edits break the pinned CSP hash, new-asset wiring checklist.
