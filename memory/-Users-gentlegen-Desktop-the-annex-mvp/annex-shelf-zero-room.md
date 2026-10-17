---
name: annex-shelf-zero-room
description: "Shelf Zero classification room shipped 2026-07-22 (4df4da0) — design, review scars, headless keyboard-evidence recipe"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4d6cdaf4-b2fd-463b-bd6d-2951a3eeed31
  modified: 2026-07-22T22:18:33.295Z
---

**SHIPPED 2026-07-22 (4df4da0), full-path review APPROVE.** The Small Archive is
now a bounded classification room ("Shelf Zero", concept A of 3): file 4
question-cards → the unclassifiable one is refused by every category → refusal
reveals shelf zero → placing it reveals 3 removal slips → both discoveries
unlock the two unchanged canonical methods. Outcome-specific concourse
alteration (opened amber seam / sealed barred frame) in WebGL + poster DOM +
switcher chip + aria. Pure reducer `src/game/room.ts`; content-driven
`worldOutcome`; zero engine/persistence change; 188 tests. Opus 4.8 implemented
from my brief (scratchpad brief-shelf-zero.md pattern); one review-caught defect.

**Review scar (promoted rule): rAF-deferred focus loses the race when the
focused element unmounts in the same commit.** The implementer's
`requestAnimationFrame(() => querySelector(sel)?.focus())` silently dropped
focus to <body> after shelf-zero placement (filing rack unmounts). Caught ONLY
by trusted-key headless evidence — synthetic clicks and structural review both
passed. Fix: pending-focus ref consumed in a post-commit `useEffect` that
retries until the target mounts ([[annex-preview-pane-quirks]] explains why the
pane could not catch this: hidden pane suspends rAF entirely).

**Headless keyboard-evidence recipe (scripts/evidence-room-keyboard.mjs):**
raw-CDP Chrome needs ALL of: `Target.activateTarget`,
`Emulation.setFocusEmulationEnabled {enabled:true}`, and Enter as the
`rawKeyDown`/`char`(\r)/`keyUp` TRIPLE — a plain keyDown+keyUp never activates
a focused button. WebGL pages also need the swiftshader flag trio or the
renderer wedges the CDP channel mid-run. Save-seeding fixture: events must pass
`isGameEvent` (seed `events: []` instead). Outcome screenshots:
scripts/evidence-room-outcomes.mjs seeds one save per committed action.

**Open (UNVERIFIED):** physical-device touch pass; user's own audition of the
room's feel and pacing (per the standing proof-of-feeling gate in
[[annex-campaign-decisions]]).

**STAGECRAFT PASS SHIPPED 2026-07-22 (5bfcedc), reviewed APPROVE.** Room became
a fixed 384px in-place tableau (was a 538→1306px scroll): one card at a time,
fixed category targets, reserved empty fourth cell, pocket card only after 3
routine filings, shelf zero only after the 3rd refusal (per-category disable +
escalating `refusalLines[3]`), log fans in place, methods REPLACE the tableau.
Plate participates in source space; return-to-concourse holds portal emphasis
~950ms (verified by in-page MutationObserver: set +10ms, cleared +957ms);
opened/sealed distinguishable with labels hidden (light-spill vs 4-bar
shutter). Reviewer record: evidence/shelf-zero-stagecraft/REVIEW.md. Review
also validated implementer deviations: site description hidden via
`:has(.classification-room)`, announcement clamped to fixed height, lockedLine
now unused but still authored.

**READING BEAT SHIPPED 2026-07-23 (6780840), reviewed APPROVE.** Fixed the
review-found rush: TURN_SLIP no longer swaps to methods; the log persists as
row-tabs + a stable full-fragment reading area, with an explicit in-voice
proceed control ("Take your reading to the Archivist") gating the view-level
swap. `roomUnlocked` untouched (canonical gate unchanged) — new `proceeded`
flag + `PROCEED_TO_METHODS` event in the view-local reducer only. Announce
region stays the single live region but is visually sr-only in log/methods
(freed height paid for larger method type). Plus: recessed empty fourth cell,
plate INQUIRY/PROCEDURE markers suppressed until methods, card corner-fold
keyline. 195 tests; reviewer record evidence/shelf-zero-reading-beat/REVIEW.md.
Design lesson worth keeping: when a bounded interaction's payoff is TEXT the
player should sit with, an unlock rule must not double as the scene-change
trigger — acknowledge, don't auto-advance.

**Host scar (headless Chrome renderer hangs):** on this Mac, long headless-CDP
sessions randomly wedge at PROCESS level (wedge point moves between runs;
`Runtime.terminateExecution` unreachable; zero console errors; pre-change code
hangs identically). Do NOT debug it as an app defect — cross-check in a real
browser and with short fast probes; accept union-of-runs evidence and record
honestly. Fast, few-evaluate probes usually finish before a wedge.
