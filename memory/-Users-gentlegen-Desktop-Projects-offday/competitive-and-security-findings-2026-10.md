---
name: competitive-and-security-findings-2026-10
description: "2026-10-03 research — Offday's security gaps, competitor table stakes it lacks, and the \"coverage-aware smart PTO\" white space"
metadata:
  node_type: memory
  type: project
  originSessionId: 02d5ec16-3f1c-4954-aab9-7fd49de9be33
  modified: 2026-10-03T20:54:14.764Z
---

Research run 2026-10-03 on main @ f28cf4a (3 subagents: code audit, competitor matrix, smart-PTO pains).

Security (verified by reading code, NOT by running requests):
- /api/assistant has no requireUser and no rate limit → anyone can burn ASSISTANT_API_KEY.
- Auth rate limit key is `auth:local:<action>` when TRUST_PROXY unset (global lockout after 12 hits, successes count); leftmost XFF when TRUST_PROXY=true (spoofable).
- No security headers (no headers() in next.config.ts, no proxy.ts).
- Global-unique emails + no delete → attacker workspace can squat any address forever.
- Privacy page claims "managers can remove anyone" and "demos not kept" — both false in code.
- Sick-leave type visible to all coworkers; assistant defaults to api.deepseek.com.

Market: Offday is the cheapest paid tool ($0.40/user at 25–50) but $3/extra person past 50 is a cliff. Missing table stakes: accrual, carryover, half-days, calendar sync (iCal), Slack/Teams, request notifications, offboarding, custom leave types, holiday packs.
White space: bridge-day optimizer that respects team/shift coverage — no SMB competitor found doing both (absence claim from ~20 searches, UNVERIFIED). Timetastic Rota (£5.50) and OrOut do coverage/shift-conflict checks, so coverage alone is not unique.

**Why:** decides roadmap order (security → table stakes → smart layer).
**How to apply:** re-verify the security items by curl against `next start` before claiming them fixed; the smart-layer spec should build on lib/shifts.ts needs-cover logic. See [[verifying-motion-locally]] for UI verification.

Update 2026-10-03: branch `fix/security-hardening` (uncommitted at time of writing) fixes assistant gating + 30/15min limit, per-account/per-address failed-login limits (rightmost XFF), security headers, streamed body caps, Origin:null 403, reopen re-checks allowance/overlap. Verified by tests/security.spec.ts (RED first) + before/after `next start` curl runs with a counting fake LLM. Still open: email squatting, offboarding/privacy-page claims, sick-leave visibility, self-approval, DeepSeek disclosure, demo cleanup, register/demo shared limit without TRUST_PROXY.
Gotcha: Playwright restarts the worker after a failure, so module-level IP counters in specs reuse addresses that already have attempts — use random addresses.

Update 2026-10-04: PR SnaxxTech/offday#18 (security) and stacked #19 (remove employee + Workspace.former, demo cleanup after 7 days, coworkers see type "Away", self-review blocked when another manager exists, requests.reviewed_by → "Reviewed by" export column). Item 1 done in #20 (signup code + "Not my workplace" /release link). #18 and #19 merged to main 2026-10-04; multi-workspace membership deferred.
Gotcha: adding a column breaks positional `INSERT INTO t VALUES(...)` — #19 converted organizations/requests inserts to named columns; do the same for any table that gains a column.
Perf 2026-10-04 (PR SnaxxTech/offday#21): before indexes every workspace load did `SCAN requests` across all orgs; at 1000 orgs/200k requests GET /api/workspace p50 was 25 ms (main) vs 3 ms (indexed), interleaved runs. tests/db.spec.ts guards the plans; scripts/bench-workspace.mjs + scripts/query-plans.mjs reproduce. Suite wall-clock is unreliable on this machine when other projects run tests (load avg hit 61 on 8 cores) — compare with interleaved benchmarks, not suite time.
Coverage warnings v1 (PR SnaxxTech/offday#22, 2026-10-04): lib/coverage.ts runs in the browser on every keystroke. Lesson from final review: a client-side check that relies on a server limit (one calendar year per request) must enforce that limit itself — a mistyped year froze the form 1.5–4.8 s before the guard. Also: test addresses must be unique across spec files (limits.spec reused limit-owner@ from workspace.spec and broke a CI-only run order).
2026-10-04: merged #21 (DB pass), #22 (coverage warnings + UI polish: avatar stack "N people free", per-team limit dropdowns, one app-wide --select-arrow, reassurance line, "Also off", "Plan cover in Shifts", closest partial match). #23 open: plain-English errors + tests/messages.spec.ts guard (no validator wording, ≤110 chars, no jargon). Remaining roadmap: "best time to take off" planner (smart B), rest radar, year-end forecast; table stakes: request emails, iCal feed, half-days, carryover/accrual, custom leave types, holiday packs.
Process note: on this machine the dev test server times out under load (load avg 40–60); run UI specs against `npm run build` + CI=true instead, and never background with `&` in a Bash call (the build gets killed) — use run_in_background.
- Parked owner decisions and deferred polish live in the repo at docs/open-questions.md (since 2026-10-04); add new ones there, not only in chat.
