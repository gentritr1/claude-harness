---
name: 2026-08-wide-two-column
description: "Wide-window two-column layout (2026-08-21) — the media condition, the side-column composition, the avatar floor, and three new measurement traps"
metadata: 
  node_type: memory
  type: project
  originSessionId: 479acb05-7521-41bf-ac52-1be2f66124e9
  modified: 2026-08-20T23:32:38.610Z
---

The fluid pass made the table a function of the space, but the space itself was
wrong on a WIDE, SHORT window: the portrait stack gives the stage
`100dvh - chrome` (~390px of strip+tray), so at 1800x876 the ring was
height-bound at 428px = **23.8% of the stage width**. All the wasted space was
horizontal and no tuning of the portrait model could reach it.

## The media condition is a SHAPE test, not a size test

    @media (max-height: 540px) and (min-width: 560px),
           (max-height: 720px) and (min-width: 720px),
           (min-aspect-ratio: 3/2) and (min-width: 1100px)

Measured ratios decided the threshold: 1800x876 = 2.05, 1920x900 = 2.13,
1366x768 & 2560x1440 = 1.78, 1680x1050 & 1440x900 = 1.60 all want the split;
1280x900 = 1.42 and 1024x768 = 1.33 do not. 3/2 sits in the gap between 1.42
and 1.60 with headroom on both sides — 16/10 at exactly 1.60 would put two of
the most common laptop shapes ON the boundary. A second `min-height: 701px`
block carries the desktop-only tuning so it never mixes with the phone band
(<=700px), which brings its own --chrome-h, seat ratios and a 2.6deg fan lean.

## Size the TRAY from what the STAGE cannot use

First attempt gave the tray a guessed `42vw`. Wrong shape of answer: on these
windows the table is height-bound, so stage width beyond what the height needs
buys nothing and just re-creates the voids.

    --tray-col: clamp(340px, calc(100vw - min(calc((100dvh - 41px) * .86), 960px) * 1.16), 1000px);

The 1.16 is the .88 width-share inverted plus ~2% cushion so rounding can never
make the width term bind instead. At 1800x876 that is 833px of stage / 967px of
tray: the ring stays 718px and the hand gained ~210px of column **for free**
(card 89 -> 114). Result: ring 428 -> 718 (+68%), 23.8% -> 86.2% of stage width.

## Two bugs I introduced and caught by LOOKING, not by reading

1. `.tray { display: flex }` turned the base rule's inherited
   `margin-inline: auto` from inert (block child already fills its parent) into
   **cross-axis centring**, which shrink-wraps a flex item to its content.
   `.hand-wrap` silently stopped being column-width: a 12-card hand became a
   1400px box inside a 967px column and pushed the PAGE into horizontal scroll
   instead of scrolling inside the hand row. Fixed with an explicit
   `align-self: stretch; margin-inline: 0`.
   -> **Rule: switching a container to flex requires auditing every inherited
   `margin: auto` on its children.** Reading the diff shows nothing.
2. Stretching then made `.label-row` and `.hint` (both `flex: 1 1 auto`) throw
   "4 PLAYABLE" and "Leave" against the far edge of a 930px column. Centring
   those rows to match the centred cards fixed it. Only a screenshot showed it.

## --min-orbit did not exist outside the phone band

`.seat-left/.seat-right` read `var(--min-orbit, 0px)` and the variable was only
ever declared inside the phone band, so **every desktop window ran with the 0px
fallback**. Invisible while desktop tables were large; it surfaced the moment
the seat tile got a floor. Now derived in base `.stage`.

The centre column's width is TEXT, so it cannot come from --table-fit. Worst
case is `Match ↻ ● Pepperoni or Flip` — longest suit against the longest
ACTIONS label — measured **272px** desktop / 218px phone. **Every mock scene
renders `Basil or 7` at 205px.** Sizing against what the mocks happen to show
would have left the real worst case overlapping by ~11px.
-> **Rule: any clearance sized against rendered TEXT must be measured with the
longest real string, injected deliberately — the fixtures are not the worst
case.** (Sweep now injects Pepperoni/Flip before measuring.)

Second half of that derivation: the term is the seat BOX's half-width, not the
tile's. A side seat is `fan | tile` (row-reverse on the left) and is centred on
the offset, so the tile sits a full half-box inward — the tile-only version was
short by exactly `fan + gap`.

## Avatar floor: ratio OR floor, whichever is larger

    --seat-floor: clamp(46px, min(4.9vw, 6.9dvh), 62px);
    --seat-tile:  clamp(28px, max(calc(var(--table-fit) * .108), var(--seat-floor)), 104px);

.108 reproduces the reference 62px tile at a 576px table, but a squarish laptop
is height-starved (1280x900 -> 446px table -> 48px avatar, SMALLER than before
the fluid pass). Floor is fluid so it does not become a new fixed step, and
stops mattering above a 574px table where the ratio overtakes it.
1280x900: 48 -> 62. 1024x768: 37 -> 50. Mobile untouched (the phone band
overrides --seat-tile and never reads --seat-floor).

## THREE new measurement traps (all cost me a wrong reading)

1. **An unfocused/occluded browser surface stops advancing CSS transitions and
   WAAPI.** `.fx-panel` reveals via `@starting-style`, so every panel read
   `height: 0; opacity: 0` FOREVER — the tray collapsed and I measured the
   portrait stage as 696px tall when it is 508px, i.e. a phantom regression in
   a layout my diff could not touch. Flights were worse: 23 travel animations
   started, **0 resolved** `finished`.
   -> Probe now calls `getAnimations().forEach(a => a.finish())` on every
   element before measuring; that IS the settled state. For WAAPI, wait real
   time then `anim.finish()` and measure.
   -> Corollary: a "regression" at a viewport your diff provably cannot affect
   is a measurement bug until proven otherwise. Diff-inertness is checkable —
   at 360x640 the phone band overrides both changed variables, and the tile
   measured 36px before and after.
2. **`resize_window` sets the OUTER window.** 1800x876 outer = 1800x**699**
   inner here (177px chrome), which silently drops into the <=700px phone band.
   The display could not fit an 876px viewport at all. Render a true viewport
   as a sized IFRAME inside real Chrome instead — layout is faithful; add a
   `transform: scale()` only to fit the capture in frame (transforms do not
   affect layout).
3. **Cancelled flights masquerade as landings.** Polling for `.travel-card` and
   keeping the last sample captures whatever size a CANCELLED ghost died at
   (fast plays cancel in-flight ghosts). Hook `Element.prototype.animate` and
   use `finished.then(onResolve, onReject)` — rejection means cancelled, and
   only the resolve path is a landing.

## Invariant 2 (ghost hand-off) re-verified, and it got stronger

Deterministic test — toggle `.is-compressed` and read `#top-card.offsetWidth`
in the SAME TICK: 1280x900 98->81, 1024x768 76->60, 375x812 93->66, identical
at 400ms. It **snaps**, so --top-card-w is not easing and a ghost launched from
the same snapshot targets the final size. Real bot games: 23 flights at
1800x820 and 14 at 375x812, **max pile-width drift 0px** (the 375 run saw the
pile at both 93 and 66 across the session).
New: in the two-column layout the hazard cannot arise at all — the bar lives in
the tray column, `--bar-h: 0px`, so `.is-compressed` changes nothing
(table 718.1 -> 718.1, top card 157 -> 157).

## Live-editing collision (2026-08-21 ~01:14-01:21)

The user edited styles.css / server/index.js / server/bot.js and added
`public/assets/pizza-table-v2.webp` WHILE this session was running: `.ring`
became `background: #0F1420 url('/assets/pizza-table-v2.webp') center / cover`.
The file 404s because the **running dev server (started 22:47) predates the
`.webp` MIME entry added to server/index.js at 01:21** — a restart serves it.
Screenshots taken after ~01:14 therefore show a dark ring; geometry unaffected.
-> Re-read files before editing AND re-run the numbers at the end; `git status`
mid-session is worth a glance when something visual changes under you.
