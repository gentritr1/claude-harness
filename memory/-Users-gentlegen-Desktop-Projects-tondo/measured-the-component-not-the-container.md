---
name: measured-the-component-not-the-container
description: A width signed off by measuring the element itself shipped the help button off-screen — in a fixed-direction row, measure the LAST sibling's edge against the container
metadata:
  type: feedback
---

Tondo's slice chip grew 97.2 -> 200.2px when the standings clause was added.
I verified it by measuring **the chip** at 1280x800, where it fits with 80px to
spare, and shipped. `.strip-inner` is one non-wrapping row, so the 103px came
straight out of the controls after it: at 390x844 the `?` button — the only
route into the rules, with nothing there to scroll — ended **17.2px past the
viewport**. Before the change it sat at 378 of 390. It was live ~20 minutes.

The gate could not see it either; it had no assertion about that bar at all.

**Why:** an element that fits proves nothing about a layout that cannot wrap,
shrink or scroll. The question is never "does this fit" but "what did it push".

**How to apply:**
- In a fixed-direction, non-wrapping container, assert the **last sibling's
  outer edge against the container's content edge**, at the narrowest supported
  width — never the changed element's own width.
- Derive the budget before writing copy: here 390px: 178, 360px: 153, 320px:
  113, against a worst-case string of 209. No phone width could hold it, so the
  clause is gated on the layout where it was measured.
- Worst case means the longest *reachable* string (three-digit gap), not the
  example in front of you.
- Gate it: `strip-fits` in scripts/shoot.js now asserts this at 320/360/390/
  1280, with "at least three visible children" as a premise so a refactor that
  moves the buttons cannot leave it passing over an empty row.
- Generalises [[sampled-viewport-gate-blind-spot]]: that one measured the right
  thing at too few sizes, this one measured the wrong thing at one size.
- It was taking BEFORE/AFTER SCREENSHOTS that found it, not any check. Shooting
  the real pairs is cheap and catches what assertions were never written for.
