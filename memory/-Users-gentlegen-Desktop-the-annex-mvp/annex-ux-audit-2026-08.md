---
name: annex-ux-audit-2026-08
description: "2026-08-02 Opus-delegated gameplay/HUD audit — confirmed findings, F2 correction scar, dead onboarding copy root cause"
metadata: 
  node_type: memory
  type: project
  originSessionId: c9a7cc16-2e52-4588-8500-020a00e16d51
  modified: 2026-08-02T23:08:47.863Z
---

Opus 5 subagent audit of gameplay smoothness / text density / HUD self-teaching, archived at
`docs/UX_AUDIT_2026-08-02.md` (with reviewer addendum). Reviewed APPROVE with corrections.

Confirmed, actionable:
- **F3 (top fix): first-run "two sites" rule is dead copy.** `Investigation.tsx:1785` renders it
  only inside the `field-commandbar` header gated on `!scene.world` (~line 1750); the cinematic
  scene-first flow always has `scene.world`, so players never see the game's core constraint.
  Fix shape = surface in mandate plate / first-concourse hint, keep `completedSites.length === 0` gate.
- **F1: `01`/`02` action ordinals advertise dead number keys.** Only Alt+C/E handled
  (`CinematicHud.tsx:129-140`); wire digits 1–4 or restyle ordinals so they don't read as key caps.
- F4: tribunal (438 w) / reconstruction (279 w) / debrief (322 w) invert the room-leads ratio; the
  verdict sits ~1,350px below fold (agent-measured). Scene rooms are correctly lean (~140–180 w).
- F5/F6 (P2): hotspots have no rest-state cue; touch hides hotspot labels (`styles.css:8473-8485`);
  concourse thresholds A/C/D unlabeled at rest. Mobile: diorama compresses to ~350px band, text
  plates dominate — opposite of desktop balance.
- 5 diegetic onboarding hints (H1–H5) in the doc; user-preferred direction is in-fiction teaching,
  no tutorial popups.

**Review scar (pattern → detection rule → brief update):** delegate reported "disabled control has
no visible explanation nearby" but `Tribunal.tsx:166-168` renders exactly that helper adjacent to
the cards (F2 demoted P1→P2) → before accepting any missing-copy/dead-end finding, grep the
component for the gating boolean's string branches → audit briefs must require quoting the DOM
around the control, not just the control. Related: [[annex-review-scar-clamped-counters]],
[[annex-investigation-inspector-always-mounted]] (same `scene.world` gating family as F3).

Open gaps: manual Alt C/E keypress on a real browser; PNG evidence not exportable from the audit
pane (re-capture via evidence harness if needed).

**2026-08-02 implementation (Opus 5, reviewed APPROVE):** F3 note (`CinematicHudDialogue.note`,
self-retiring), F1 digit keys 1–9 + `<kbd>` caps (4 new tests), F4 scroll-cue jump + Step 1/2 marks.
All verified by re-executed probe (21/21, trusted CDP keys), 821/821 vitest, build, harness 101/131
(= pre-change baseline; the 30 reds assert the retired legacy `!scene.world` HUD — separate cleanup).
Uncommitted; working tree also carries large pre-existing 02:xx user work — do NOT attribute whole
diffs of Investigation.tsx/styles.css to this change.

**Review scar #2 (pattern → detection → update):** delegate's probe LABEL said "≥44px tap target"
but the expression asserted `cue.h >= 40` and the cue measured exactly 40px — an instrument tuned to
pass its own output → when any labeled threshold check passes, read the assertion expression, not
the label; compare every printed measurement against the claimed bound → briefs must state that
probe labels and expressions will be diffed at review. (Same family as [[annex-reviewer-pinned-thresholds]].)
Fixed: cue min-height 44px (styles.css ~4987) + probe corrected, re-run 21/21.

Environment: port 3000 got hijacked by an unrelated Next.js app mid-session; canonical dev server
now vite on 127.0.0.1:4177. Harness + probe scripts need `node --experimental-websocket` on Node 20.
Harness boot was repaired (briefing two-step: click `Begin audit` after route card) — pre-repair it
was 8/25 all "investigation did not render".

**2026-08-02 round 3 (Opus 5, reviewed APPROVE, committed 9a52285):** harness re-pointed at
scene-first HUD (29 re-points, 0 retired, all equal-or-stricter — verified by line diff), H4 pulse
(one-shot, both reduced-motion paths verified by re-executed CDP probe 18/18), F5 touch labels,
F6 named thresholds, Alt C/E closed with trusted keys, latent empty-drawer defect fixed.

**Review scar #3 (pattern → detection → update):** the harness browser dies mid-run on this
memory-starved host (CDP timeout inside crossZonePass, 6+ runs), so "131/131 green" existed only
on a pre-tweak state; the fix was UNION VERIFICATION — sectioned reviewer copies (comment out
covered `await guard(...)` calls) until every check name in the full set has a PASS on final code.
Two traps found doing it: (a) a section that dies mid-loop never EMITS its later checks, so absent-
from-log ≠ failed — diff PASS names against the known-full set, never trust run counts; (b) six
"missing" checks turned out to be later iterations of a loop the browser died inside, recoverable
via verbatim-assertion re-execution in the live pane (geometry-free assertions only). Pane quirk:
backgrounded pane reports innerWidth 0x0 while DOM stays live — geometry probes lie there, state
probes don't.

**Chip task DONE (f62fb36):** evidence-hud-collapse.mjs is now sectioned/resumable —
`--sections=a,b,c`, per-check JSONL stream (`evidence/hud-collapse/checks.jsonl`) with DONE
markers, `--resume` (skips fully-green sections, carries checks into the summary), fresh Chrome
per section by default (`--single-browser` opts out), instrument death continues to the next
section instead of aborting. Verified: full run survived one browser death (15/16 sections),
single `--resume` closed 131/131 exit 0. Note: a resume run's measurements.json only carries
measurements for the sections it actually reran — checks.jsonl is the complete record. Canonical
green-run recipe on this host: run full, then `--resume` until 131/131.
