---
name: za-audit-program
description: External audit (2026-08-09) resolved in two agent waves on table; worktree-base staleness scar; what remains open
metadata:
  type: project
---

2026-08-09: external "$impeccable" audit of za-game resolved across 4 Opus
agents in 2 waves, all landed on `table` (tip 9f137f7): reconnect state
machine (no send queue exists any more), room-TTL/host-election/45s-idle
server policies (+5 tests, suite now 54), leave arm-to-confirm, auto-rematch
deleted, short-height reflow, scrollable near rail, roster/lobby
reachability, focus management (openedPopover/closePopovers with
restoreFocus+instant), computed-contrast fixes, rib suit letters
(suitLetter in cards.js), shared announcer (exists from boot), pit-scrub
geometry cache, press listener sessions, generation-scoped shutter, ambient
pause on inactive screens, HOUSE RULES overlay (9 server-cited sections,
4th screw at 135°, syncAppInert + one openModal tab trap).

SCAR (promote if it fires again — it fired 3× this cycle): **worktree agents
based themselves on stale refs (main instead of table)** — U, motion, and
onboarding all built against main; symptoms: "49 tests not 54", "no 45s
clock", "conveyor does not exist", edits to the deleted chef column. Detection:
check the agent's merge-base against the intended branch FIRST, read its
"corrected premises" as base-staleness clues, and expect merges to need
seating-era conflict resolution. The reviewer must re-verify landed features
on the real branch UI after such merges (rib letters, badges, short-height
were re-proven on table).

Still open ([[za-table-and-log]]): table→main merge verdict (user's call, now
carries seating + audit hardening); $impeccable re-audit suggested after
merge; audit items NOT done: browser tests for reconnect/timers/breakpoints
(deferred), the auditor's ultrawide "under-scaled" taste note, window.blur
press release (edge), non-host round-over text render check.
