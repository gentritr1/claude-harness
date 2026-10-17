# Stone Oven port — game screen (2026-08-20)

Ported public/{index.html,styles.css,js/app.js} from the dark-blue "Ring Table"
look to the Stone Oven design. Scars worth keeping:

## CSS scale system: `--cs` must divide a UNITLESS number
`--cw: 96px; --cs: calc(var(--cw) / 96)` yields a LENGTH (1px), so every
`calc(22px * var(--cs))` becomes px² and is dropped — silently. Chrome then
renders the browser-minimum 13.33px and `background-size: auto`, which looks
like "the design is just a bit off" rather than an error, and produces NO
console output.
- Detection rule: after any proportional-scale CSS system, read back
  `getComputedStyle(el).fontSize` on a scaled element and assert it is not
  13.33px / not `auto`. Eyeballing a screenshot will not catch it.
- Fix: card widths are unitless (`--card-w: 96`), lengths made at point of use
  (`calc(var(--cw) * 1px)`).

## Selector ORDER clobbering, twice in one pass
A later equal-specificity rule silently re-asserted a property an earlier rule
had set. Both were invisible in a screenshot until measured:
- `.deck-face { position: absolute }` beaten by the later shared `.back-face`
  (`position: relative`) → the deck face collapsed to height 0.
- `.under-card { position: absolute }` beaten by the later shared card-anatomy
  group (`position: relative`) → buried discards took real layout width and
  shoved the top card ~45px off centre.
- Detection rule: when adding a SHARED rule whose selector list includes a
  class that already has its own rule, grep for that class and confirm which
  comes last. Assert with `getComputedStyle(...).position` in the browser.
- Fix: raise specificity (`.deck > .deck-face`, `.pile > .under-card`).

## `hidden` vs `display` — now guarded globally
Third occurrence class of the repo's known bug. Instead of per-class guards,
styles.css now opens with `[hidden] { display: none !important; }`.
Verified by script: set `hidden` on all 20 JS-toggled elements and assert
`display === 'none'` — 0 leaks.

## Seat/plaque collision is a GEOMETRY constraint, not a style bug
New seats are ~2x taller than the old pip fans. `.seat-top` is clamped
(`max(50% - --table-d/2, Npx)`) so it is not cut off at the stage top; whenever
the stage is not much taller than the table, the clamp drags the seat off the
circumference and its name pill lands on the MATCH plaque.
Two failure regimes that pull in OPPOSITE directions:
- stage SHORTER than table (clamp binds) → need a SMALLER table
- stage MUCH TALLER than table (seat sits on circumference, near centre) →
  need a BIGGER table; the invariant is `--table-d >= column height + seat
  group height`.
- Detection rule: never eyeball this. The repeatable check is a scripted
  rect-overlap sweep over all 7 mock scenes x ~10 viewports, asserting
  pill/tile vs plaque, tile vs top-card, seat vs stage-top clipping,
  deck vs ribbon, and body horizontal scroll. Kept in the session transcript;
  re-create it before touching seat or table geometry again.
- Verified clean at: 1440x960, 1280x900/860/820/800/780/740, 1024x768,
  844x390, 616x416, 375x812, 360x640.

## Pre-fix comparison is cheap — use it
To decide "regression or pre-existing?", `git show HEAD:public/<f>` into a
scratch dir + `python3 -m http.server` on another port, then load
`?mock=1&scene=...` there. `mock.js` needs no backend. This turned a guess
into evidence (the top-seat/plaque overlap WAS a regression; ~8px clearance
before).

## Browser-pane gotchas (adds to browser-pane-click-flakiness.md)
- `resize_window` sets the EMULATED viewport; the pane frame may stay larger,
  so screenshots show the app in the top-left with dead space. `innerWidth`
  is the truth — measure, do not judge size from the screenshot frame.
- A `getComputedStyle` opacity read in the SAME tick as a class toggle returns
  the transition's START value. `body.is-offline .deck` read 1, then 0.55 in a
  separate call. Split add-class and read into two tool calls.

**Fan-rotation clip (user-reported 2026-08-20, FIXED):** `.hand-row` had zero inline
padding while end cards rotate up to ~12deg around origin 50%/120% — the swung top corner
overhangs the layout box by ~17px (mobile) to ~33px (md), and for the FIRST card that
overhang is left of the scroll container's content start, which overflow clipping makes
permanently unreachable. Fix: inline padding sized to the measured overhang (20px base /
18px mobile+landscape), plus a new 720-989px x >=700h breakpoint (--card-w 82) so
narrow-but-tall windows don't get the full 96px desktop cards. Rule: any transform that
rotates/translates children of a scroll container needs edge padding >= the transform
overhang at the extremes, measured via getBoundingClientRect (bounding box includes the
transform), not eyeballed.

