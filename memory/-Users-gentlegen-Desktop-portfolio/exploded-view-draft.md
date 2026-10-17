---
name: exploded-view-draft
description: "/drafts/exploded-view is the owner's chosen direction (2026-10-11); how the SVG drawing and the 3D stack are kept identical"
metadata:
  node_type: memory
  type: project
  originSessionId: 71d00c39-45c1-490a-8542-7433d53286cb
  modified: 2026-10-11T00:48:10.769Z
---

The owner loves `/drafts/exploded-view` and chose it as the main direction on 2026-10-11. It is built from his "Exploded View" build prompt, on plain three.js in Vite (not Next.js or R3F).

It has one fixed canvas, and the stack is anchored to the drawings themselves: the hero SVG, then a sticky stage frame. Scene states (rewrite, tokens, tenants, reader, stack, contact) are set by `[data-scene]` sections crossing the middle of the viewport. Case pages live at `/drafts/exploded-view/<slug>`, in the brief's order.

**Why:** the SVG drawing doubles as the reduced-motion and no-WebGL fallback, so any mismatch with the 3D shows as a jump at the handover.

**How to apply:** when either one changes, recompute the matching numbers and run the overlay check. The numbers today: a world unit is 0.102 of the drawing width (its plate diagonal is 300/520), the centre sits at 0.365 / 0.481, a 44 px drawing gap equals 0.96 in the 3D, labels start at H+0.96 with leaders to H+0.86, and corners are rounded at 8%. The overlay check is `scratchpad/shot/xvmatch.mjs`: capture the reduced-motion drawing and the live 3D, merge the two into colour channels, and look for fringes.

Gotcha: a three.js mesh at opacity 0 still writes depth and cuts a hole in the plate above, so faded effects must set `visible = false`. Also, on phones a paused canvas keeps its last frame, so hide it when pausing. See [[event-horizon-draft]].

Taste-fail pass (2026-10-15): labels now read `--xv-label-k` (1 / 1.2 below 1280 / 1.3 below 861) in BOTH the SVG text and the 3D label CSS, so they stay ≥13 px and keep one start point. Gotchas found: the old `.xv-root :is(h1,…)` reset out-ranked every class margin (More work had 0 gap) — now `:where`; and on ≤860 the hero SVG shrank to the 300 px default inside the centred grid figure until it got `width: 100%`. Pre-existing, not fixed: in the `stack` state the 3D opens wider (gap 1.4) than the stage drawing, so 3D labels sit ~44 px left of and spaced wider than the SVG labels (same at HEAD 71345fd).
