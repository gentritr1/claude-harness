---
name: 2026-08-22-message-deck-perf-pass
description: Tondo 2026-08-22 Opus-5 delegate pass — hand message fade, deck docked beside the hand, perf audit; what was measured, what the review caught, standing rules
metadata:
  type: project
---

Delegated (Opus 5) after the user reported: "Doesn't match…" line pops in abruptly; draw deck
too far on large screens; wants 60fps. Reviewed 2026-08-22 by re-running every scenario.

**Outcomes (all re-measured by the reviewer, headless Chrome CDP + pane):**
- `setText()` `instant` now means text→TEXT only; empty→text fades in via `.txt-fade:empty
  { opacity: 0 }` (+3px settle), text→empty runs `.is-swapping` first. `.message { min-height:
  1lh }` reserves the line — before the fix a hover shoved hint/Leave 17px on desktop and the
  whole hand 29px on phones (bottom-anchored tray). Rects identical at 5 viewports after.
- `#deck` moved out of `.stage` into `.hand-dock` beside `#hand-wrap`; `--deck-w` moved to
  `:root` (= .7 × --card-w). Reach deck-centre→nearest card: 508px → 77.7px at the user's
  2000×1290; 0.59–0.82 card widths everywhere `.btn-draw` is hidden. Phone band unchanged.
  `pileRect()` caches the last on-screen deck rect because `.hand-wrap[hidden] + .deck
  { display:none }` hides the deck in the exact snapshot a drawn card arrives.
- Perf: `updateFades` reads-before-writes + rAF-coalesced (`scheduleFades`), `showBanner`
  only forces a reflow when the banner was already showing. Honest result: RecalcStyle −26%,
  task −9% (non-overlapping across shuffled A/B) but ZERO change in frames >16.7ms — the deal
  frame is a genuine first layout, not a forced one. Headless rAF runs at ~120Hz; "expected
  frames" must be window/8.33 there. No real-display 60fps confirmation exists.
- Accepted cost: at 320×568 the reserved message line clips the pie 1.6px top/bottom.

**Review lessons → rules:**
- Measuring rects in the same tick as `window.__mock.goto()` returns PRE-layout boxes (deck
  read 166px too high, "overlapping" two cards). Read in the next frame / after a second
  evaluation; an overlap seen only once is suspect.
- zsh expands a leading `=` (`echo ====X` → "command not found"); quote log markers.
- Delegate reports that say "no frame win" and disclose moved costs (forced layout migrating
  to `moveToken`) are the good kind — the reviewer's job was to confirm, not to find a win.
Related: [[2026-08-polish-pass]], [[headless-cdp-media-emulation]], [[keyframe-js-handoff-pair]].
