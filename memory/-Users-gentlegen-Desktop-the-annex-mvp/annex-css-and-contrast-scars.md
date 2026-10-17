# CSS + contrast measurement scars (2026-07-25 design-gap pass)

## CSS syntax errors are invisible to every green check in this repo
A malformed comment in `src/styles.css` shipped a stylesheet that failed PostCSS while
`tsc`, `eslint` and `vitest run` (294 passed) all stayed green. The only signal was the
dev server returning an error document for `/src/styles.css`, which surfaced two steps
later as a harness failure reading `landing did not render`.

**Detection rule:** any pass that edits `src/styles.css` runs `npx vite build` (or curls
`/src/styles.css` off the dev server) BEFORE running a harness. A green suite is not
evidence the stylesheet parses.

## A contrast probe that reads declared background colours verifies a fiction
Once a panel is translucent over a photograph, `getComputedStyle().backgroundColor` is not
the background the text is read against. `scripts/audit-contrast-probe.mjs` measures the
composited pixels instead. Three separate FALSE FAILURES were produced while building it:

1. `visibility: hidden` to remove glyphs also hides the element's **own** scrim, so a
   label chip gets measured against whatever is behind the chip. Use
   `color: transparent; text-shadow: none` instead.
2. A child with its own `color` (a white `<strong>` inside a dim caps label) does not
   inherit `transparent`; its surviving glyphs then get sampled AS background. Apply the
   transparent colour to the element **and every descendant**.
3. Text covered by a higher-stacked surface has no reader and no contrast problem — but
   sampling "behind" it measures the covering surface's glyphs. The plate caption under a
   docked console reported a fixed 1.66:1 against `--fog-dim`, which is console text.
   Filter glyph boxes by `document.elementFromPoint`, forcing `pointer-events: auto` on
   the target for the hit test (the caption sets it to `none`, so elementFromPoint would
   otherwise see straight through it).

Also: sample the union of `Range.getClientRects()` glyph boxes, inset 1px — an element
rect includes its own currentColor border and, for a flex caption spanning the plate,
hundreds of px of empty track.

## "Text is too dominant" is a HIERARCHY measurement, not an area measurement
Measured 2026-07-25: the concourse spent 7.7% of the viewport on glyphs; the debrief (the
screen the user LIKED) spent 11.8%. The difference was 13 distinct font sizes in a 1.76:1
range vs 14 in a 6.2:1 range. 44% of concourse glyph area sat at one size (11.52px) in
three weights, so nothing was ever the biggest thing and the eye had to read everything.

**Rule for the next "too much text" complaint:** measure distinct sizes / size-weight-case
pairs / largest-to-smallest ratio per screen FIRST. Do not chase glyph-area down — a first
cut of this pass promoted body copy and left the band untouched, which pushed distinct
sizes UP (13→14) and glyph area up on every surface. Type consolidation is close to
mass-neutral by design; the win is triage, not less ink.

Corollary: the glyph-area metric measures line boxes, so it **cannot see a font-weight
reduction**. The caps-mono label drop from 650 to 500 weight is a real reduction in
perceived ink that no number in `measurements-after.json` reports. Tag it as an eyeball
claim backed by the screenshot pair.

## Where the scale lives
`src/styles.css` `:root` — seven working-band tokens (`--type-micro/label/meta/body/read/
title/scene`) plus `--label-weight` / `--label-tracking`, with a `@media (max-width: 700px)`
block stepping the whole band down one notch. 232 declarations were snapped onto it.
The display band (>1.5rem, ten values) is deliberately NOT tokenised — see
`docs/design-gap-audit-2026-07.md` P3-A.
