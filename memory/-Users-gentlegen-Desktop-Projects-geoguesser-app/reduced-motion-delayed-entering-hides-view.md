---
name: reduced-motion-delayed-entering-hides-view
description: "Reanimated delayed `entering` + Remove animations left HowToPlay's first-page step icon invisible on first mount (1.4.0 bug, seen on device 2026-09-16)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T19:42:53.410Z
---

On the Pixel_8_Pro AVD (API 36, QA APK) with animations off (animator scale 0), HowToPlay's
page-1 step icon — `Animated.View/Text` with `entering={FadeIn.delay(80).duration(260).reduceMotion(ReduceMotion.System)}`,
mounted inside the pager ScrollView after onLayout — was blank on first open: the 1.4.0 emoji
2 of 4 opens right after install (and once after a reboot); E1b-1's v2 SVG icon with the same
entering 4 of 5 fresh installs. With animations on: 3/3 fine. Pages 2-3 and the card (no delay) were fine.
It is not the emoji font: the SVG icon blanked too.

**Why:** a visibility-critical property that only reaches its resting value if an animation completes
(CLAUDE.md §6) — and it hits exactly the players who turned animations off.

**How to apply:** E1b-1 dropped the entering from the v2 icon (0/5 blank after). The 1.4.0 path is
unchanged (art_v2 OFF must stay 1.4.0) — E2 owns the unflagged reduced-motion fix. Test by
reinstalling (`adb install -r`) and opening the screen fresh several times, with animator scale 0;
count distinct colours in the icon's box (1 = blank), don't trust one screenshot.
