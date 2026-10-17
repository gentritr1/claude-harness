---
name: port-env-collision
description: "Dev harness injects PORT env var — game server must use ODD_PORT, not PORT"
metadata: 
  node_type: memory
  type: project
  originSessionId: c0bff7d7-4d12-4eb5-addf-8dea9a66ddb9
  modified: 2026-08-16T11:01:28.524Z
---

The Claude Code preview harness (launch.json `port` field) exports `PORT=5173`
into `npm run dev` children. The WS game server originally read
`process.env.PORT ?? 8787`, so it bound vite's port 5173 → dual-bind flakiness
(IPv4/IPv6 split): pages loaded, some WS connects worked, others EPIPE'd, and
intents (e.g. guided start) silently died. Symptom to recognize: server log
says "listening on :5173" and vite proxy prints `write EPIPE`.

**Why:** generic `PORT` is a common injection point for dev harnesses/hosts.

**How to apply:** server reads `ODD_PORT` (fallback 8787) — keep it that way;
never "simplify" back to `PORT`. Fixed 2026-08-16 in src/server/main.ts.
