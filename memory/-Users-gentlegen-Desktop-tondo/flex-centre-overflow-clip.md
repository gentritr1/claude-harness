---
name: flex-centre-overflow-clip
description: Tondo — adding content to the flex-centred home/lobby card clipped its top unreachably at 320×568 (v0.2 polish review, 2026-08-22); detection rule + brief rule
metadata:
  type: project
---

`#screen-home` / `#screen-lobby` are `display:flex; align-items:center; overflow:auto`. When the
card grows taller than the viewport, flex centring pushes the overflow equally above AND below,
and the part above `scrollTop 0` is unreachable (classic flex-centring overflow clip).

Fired 2026-08-22: the v0.2 welcome-screen pass added a card fan + hook + facts (~113px).
HEAD card = 487px (fits 568); post-change ≈ 600px → card top at −52px, fan top at −30px at
320×568, `scrollTop` pinned at 0. The delegate's report claimed "verified at 320×568".

FIXED 2026-08-22 with `margin:auto` on `.home-card, .lobby-card`: 320×568 top +20px, 320×480 top
+20px (bottom reachable), 1280×720 still centred (42.75px above / 42.76px below).

**Why:** a screenshot of the centred card looks fine if you don't know what's missing above it;
only `card.getBoundingClientRect().top` at `scrollTop = 0` reveals it.

**How to apply:** (1) fix = `margin:auto` on the card (auto margins respect overflow) or
`align-items: safe center`, not more padding; (2) any change that adds height to a centred
screen card must report `scrollHeight vs clientHeight` and the card's top rect at the smallest
target viewport; (3) briefs for welcome/lobby content must name 320×568 AND the measurement.
See [[2026-08-polish-pass]] for the rest of the v0.2 review.
