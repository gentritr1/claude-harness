---
name: hosting-free-tier-facts
description: Fly.io has no free tier for new orgs (read 2026-10-10); Neon is a DB not a WS host; Render free sleeps — inputs to the Workstream 2 hosting decision
metadata:
  node_type: memory
  type: project
  originSessionId: 3fb08f38-07c3-4529-b2e2-21cde8419a74
  modified: 2026-10-09T23:18:48.198Z
---

Read 2026-10-10 for the hosting move (docs/HANDOFF-2026-10-10.md, Workstream 2):

- **Fly.io** (docs.fly.io/about/pricing, official): no free tier or allowance for orgs created after 2024-10-07. Trial = 2 Machine-hours or 7 days, whichever comes first. Smallest machine (shared-cpu-1x 256MB) costs ~$2.19 per 30 days running 24/7 in iad/ewr, plus egress at $0.02/GB. Orgs from before the cutoff keep the old allowance, so ask the owner whether theirs is one.
- **Neon** is Postgres, not an app host. Its "WebSocket" is only the driver's transport to the DB, and it cannot hold player sockets. Free plan: 100 CU-h per project per month, 0.5 GB, scale-to-zero after 5 min. That is enough for crew rows only if nothing polls it: the 5-min pinger trap in ~/.claude/CLAUDE.md §12.
- **Render free** sleeps after 15 min without inbound HTTP or WS messages. WS messages have counted since 2026-02-24. Cold start is ~1 min, and it may restart at any time, which loses the in-memory rooms. That makes it a poor fit for a marketed launch.

**DECIDED 2026-10-10 (owner):** test on **Render free** now and move to **Fly** if it goes commercial. Keep the server host-agnostic: plain Node, env-only config (`PORT`, `DATABASE_URL`), crews in Neon outside the host, one app serving page + WS. The WS Origin check needs the same host for both.

**Why:** the owner asked "is Fly a better free choice than Neon for websockets", which mixes up two different layers.
**How to apply:** treat the stack as host (Fly) + store (Neon free, or SQLite on a Fly volume). Budget about $2–3/mo for the host, and re-read the prices before the spec pins any number.
