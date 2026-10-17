---
name: animation-easing-eats-duration
description: A front-loaded animation timing function spends the keyframe timeline early, so a declared duration overstates the visible one ~5x; per-keyframe easing cannot fix it
metadata:
  type: project
---

2026-10-06: every one-shot fade in `public/styles.css` was visible for about a
**fifth** of its declared duration. Measured by pausing the animation and
seeking `currentTime` in 5ms steps, taking the window where opacity is ≥40% of
its own peak:

| effect | declared | was visible | on `linear` |
|---|---|---|---|
| dir-sweep | 620ms | 100ms (16%) | 375ms (60%) |
| sauce-wash | 520ms | 80ms (15%) | 355ms (68%) |
| tondo-ring-pulse | 220ms | 40ms (18%) | 135ms (61%) |
| token-hop | 280ms | 50ms (18%) | 170ms (61%) |

**Mechanism.** An animation's timing function warps TIME INTO PROGRESS for the
entire keyframe timeline. `cubic-bezier(.16,1,.3,1)` and `--e-out`
(`cubic-bezier(.23,1,.32,1)`) are strongly front-loaded, so by ~16% of the
duration the timeline is nearly spent and the opacity has collapsed.

**The obvious fix does not work, and I measured that before shipping.** Moving
the easing onto the fade-out KEYFRAME (`animation-timing-function` on the
mid-keyframe, which is this file's own pattern for `tondo-stamp`) measured
IDENTICAL — because the input progress is already front-loaded before any
per-keyframe curve applies. Only the **animation-level** function changes it.

**Pattern → detection rule → brief update.** "This effect is too subtle" is a
duration bug before it is a value bug. Never tune alpha, width or colour on a
flourish until its visible window has been measured — otherwise the new value is
tuned against the timing fault and overshoots once the timing is fixed. The
measurement is cheap: pause the animation, seek it, read computed opacity; no
screenshots needed.

Keep `--e-out` for anything **arriving or leaving** (a fast start reads as
responsiveness). It is wrong for a one-shot whose whole job is to be seen for
its stated duration. A fast rise can be kept by putting the eased curve on the
FIRST keyframe only, with the rule on `linear` — the wash reaches 80% of peak in
45ms and still decays over 355ms.

Related: [[2026-08-animation-pass]], [[2026-09-16-action-legibility-fx]]
