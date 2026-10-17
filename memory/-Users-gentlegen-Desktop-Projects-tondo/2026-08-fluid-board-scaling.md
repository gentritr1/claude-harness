# Fluid board scaling (2026-08-21)

Made the board a continuous function of available space instead of a capped
table plus per-breakpoint pixel steps. `public/styles.css` + `public/js/app.js`
only. 44 tests still green.

## The unitless-`--cs` scar is now OBSOLETE — length/length works

`2026-08-stone-oven-port.md` says card widths must be UNITLESS because
`--cs: calc(var(--cw) / 96)` yields a length. That is true but it was the wrong
fix: dividing by a **length** types as a `<number>` per CSS Values 4.

    --cw: 96px;  --cs: calc(var(--cw) / 96px);   /* a plain number */

Verified empirically in Chrome 148 before relying on it (do this again, never
assume): `CSS.supports('width','calc(100px * (96px / 96px))')` → true, and a
runtime probe with `--cw:96px` → width 200px / font 22px / padding 10px,
`--cw:48px` → 100px / 11px / 5px — exactly halved. Cards are now real lengths,
so a card can be sized from `clamp()`/`min()` of the space. Rejected the
em-based alternative: it forces every text size into `em`, risks nested-em
compounding, and measured 10.0003px where length-division gives exactly 10px.

## Selector-ORDER clobbering — THIRD instance, promote to a standing check

The shared rule `.card, .top-card, .under-card, … { --cw: var(--card-w) }`
sits AFTER `.top-card { --cw: var(--top-card-w) }` at equal specificity, so the
**discard has always rendered at the hand card's width**, while `#under-1` /
`#under-2` (ID selectors, so they win) used `--top-card-w`. Invisible for a
year because the two numbers were close (94 vs 97.6 at 1280x900); the fluid
model pulled them apart (132 vs 191 at 2560x1440) and made it obvious.
Fixed with `.pile > .top-card`, matching `.pile > .under-card` and
`.deck > .deck-face` — the same fix this file already needed twice.
→ **Detection rule:** after ANY change to a shared multi-class rule, assert
   `el.offsetWidth === parseFloat(getComputedStyle(el).getPropertyValue(itsVar))`
   for one element per class in the selector list. Reading the CSS will not
   catch it; only comparing the variable against the rendered box does.

## Registered custom properties: derive furniture from an UNREGISTERED source

`--table-d` is `@property`-registered and transitioned (200ms). Anything
derived from it via `var()` re-resolves **every frame of that transition**, so
naively deriving `--top-card-w` from `--table-d` would have animated the
discard's size — and `flyToPile()` computes the flight ghost's landing scale
from `topEl.getBoundingClientRect()` at play time, which would then be stale.
This matters in real games: `is-compressed` is toggled from the SAME snapshot
that starts a flight (a callout appears exactly when an opponent plays down to
one card).

Pattern that solves it without duplicating the expression:

    --table-fit: min(...);          /* unregistered token stream: cannot animate */
    --table-d: var(--table-fit);    /* registered <length>: transitions */
    --top-card-w: calc(var(--table-fit) * .219);   /* registered, but SNAPS */

Measured: `--table-d` eased 445.68 → 371.76 over ~200ms while `#top-card`
offsetWidth snapped 98 → 81 at frame 0 and never moved. Also confirmed the code
order that makes it safe — `renderGame()` toggles the class (app.js:410) before
`runTravel()` reads the pile rect (411), and `getBoundingClientRect()` flushes
style, so the read already sees the final size.

## Fan overhang is a RATIO of the card, not a constant

`.hand-row` inline padding must be ≥ the fan's rotation overhang or end cards
are clipped and unreachable at the scroll extremes. JS clamps `--off` at 3, so
the lean saturates at 3 x 4deg + jitter and the overhang settles at a fixed
**0.371 x --card-w** (measured 48.97px at --card-w 132, identical from 10 cards
up to 16). The old flat `20px` was only ever enough for small cards — it is
below the requirement at --card-w 96, so **desktop 12-card hands were already
clipping before this pass**; growing cards to 132 just made it show at 10.
Now `calc(var(--card-w) * .43)` desktop / `* .31` mobile (mobile leans 2.6deg,
not 4deg, so it needs a smaller ratio). Verified reachable at 11 viewports x
hands of 7/10/12/16, worst clearance 1.5px.
→ Any padding sized against a transform must be a ratio of whatever the
   transform scales with, and must be re-measured when that thing can grow.

## `--seat-edge` must derive from the seat's WIDEST part

`--seat-edge` keeps a seat on stage, and the widest part of a seat is its
status pill, not its tile. Deriving it from the tile (`tile * 1.6`) reproduced
the old desktop/mobile numbers but left a 320px-wide phone pinned 60px in with
its tile 2px inside the MATCH plaque. `calc(var(--pill-max) * .5 + 6px)`
self-corrects in every band that caps the pill narrower.

## Two floors, opposite directions

`--seat-edge` stops a seat leaving the stage when the table is LARGE.
`--min-orbit` (new) stops it landing on the MATCH plaque when the table is
SMALL — a seat on the circumference must never sit nearer the centre than the
centre column's own half-width. Only the first existed, because a capped table
could never get small enough for the second to matter. A table that tracks the
stage continuously can.

## `100dvh - chrome`, not `vh`

`vh` was the wrong height term: the stage is the viewport MINUS the strip and
the tray, and those are a roughly constant number of PIXELS, not a fraction.
`--chrome-h: calc(259px + var(--card-w) * 1.4375)` reproduces the measured
strip+tray (53 + 344 = 397 at --card-w 96) exactly, re-measured per band
(277px on phones, 265px on the shortest). That is why the table can keep
growing on a tall screen instead of stalling at a fixed fraction.
Result: table diameter is now 86-89% of stage height at EVERY viewport tested,
vs 55-91% before (576px flat cap on anything large).

## Verification method notes

- **Sweep viewports with IFRAMES, not `resize_window`.** An iframe has its own
  viewport, so `vw`/`dvh` and media queries resolve to its box: 10 viewports x
  7 scenes in two tool calls instead of 70 resizes. Cross-checked against real
  `resize_window` at 1600x1000 and 375x812 — same numbers.
- **Measure sizes with `offsetWidth`, not `getBoundingClientRect()`.** Nearly
  every element here is rotated (cards -3deg, tiles -5deg, deck -6deg), so the
  rect is the inflated bounding box: it reported a 96px card as 118.5px and
  sent the first BEFORE table out by ~20%. Use rects only for overlap.
- **The `[hidden]` audit must settle ~700ms.** Reading `display` in the same
  tick reports `flex`/`block` for every `.fx-*` node, because
  `transition: display allow-discrete` legitimately holds it rendered through
  the exit. First run showed 12 "leaks", all false. After settling: 21 nodes,
  0 leaks.
- **The pane cannot screenshot a viewport bigger than its frame** — it scales
  the whole app into a corner. Numbers were taken by script; the large-screen
  "does it look right" remains a user eyeball.

## Pre-existing, found but NOT introduced by this pass

- A flight launched while the PREVIOUS `top-card-land` is still running reads a
  transiently-scaled pile rect, so the ghost lands up to ~2% off. Bounded by
  that keyframe's own scale range (0.982-1.07). 16/17 landings measured exactly
  0.00px; the outlier had no size change and no compression change, which is
  what ruled out my first (wrong) hypothesis that compression caused it.
  → When a mismatch appears, check for an animation still running on the target
    before blaming the sizing model.
- `RING_TALLER_THAN_STAGE 15.2px` at 375x812 in the compressed callout scene
  (now fixed by the continuous model).
