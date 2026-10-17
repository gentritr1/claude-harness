---
name: pizza-suit-photos
description: Tondo — the oven shows a photoreal pie per active topping (Higgsfield-generated), crossfaded; how to regenerate and the gotchas
metadata:
  type: project
---

The table swaps a **photographed pizza per active suit** (2026-08-21): `public/assets/pizza-{pep,bas,chz,anc}.webp`.
All four were generated with Higgsfield `nano_banana_2` (2 credits each, 2k) using the user's own
`pizza-table-v2.png` as an `image_references` input, with prompts that pin the crust, pan, framing
and transparent background as IDENTICAL and change only what sits on the sauce. That reference-image
approach is what makes them **crossfadeable** — generating four pies from text alone would drift in
angle/scale and the dissolve would read as a jump cut. Downscaled to 1024 and `cwebp -q 84` (~250KB each).

Wiring: `#pizza-photos` holds all four `<span>` layers inside `#ring`; only `opacity` animates
(`--t-pizza: 420ms`). `renderCenter` sets `photos.dataset.suit = activeSuitOf(g)`. The attribute goes
on the photo stack, NOT on `#ring`, so a suit change re-runs selectors for four children instead of
the whole oven subtree.

**Gotchas:**
- Suit keys are full words — `pepperoni | cheese | basil | anchovy` — while card codes are PEP/BAS/CHZ/ANC.
  I first wrote `[data-suit="bas"]` and nothing lit up.
- All four layers stay in the DOM on purpose: swapping `background-image` on one node pops white on
  its first paint because the image decodes after the swap.
- The user's CSS count-toppings (`renderPizzaToppings`, piece count = card number) still render ON TOP
  and were deliberately kept — the photo carries suit identity, the pieces carry the number.
- Debugging trap hit again: the pane tab was `document.hidden`, so the opacity transition sat
  `running` at 0 forever and the layer looked broken while the CSS was correct. See
  [[browser-pane-click-flakiness]].
