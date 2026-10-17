---
name: w4-10-menu-compose-gotchas
description: W4-10 (2026-09-26) composed menu - a padded wrapper drawn after the header ate its taps (bounds checks passed); jest -u deletes *.snap under artifacts; RNTL folds NBSP; midnight-safe seeding
metadata:
  type: project
---
- A transparent layout View drawn AFTER other controls and overlapping them steals their taps on Android (hit test picks the topmost view, responder bubbles to its ancestors, not siblings). jest + uiautomator bounds all passed; only an adb tap + DB read caught it (♪ did nothing). Fix `pointerEvents="box-none"`. Rule: any new wrapper box gets a tap check on every control it covers.
- `jest -u` (even with a path + `-t` filter) deletes any `*.snap` under rootDir it considers obsolete — it removed a provenance copy in artifacts/. Keep snapshot copies as `.snap.txt`.
- RNTL text matchers normalise whitespace, so U+00A0 matches a space; assert raw `props.children` to test NBSP.
- Seeding `today`-dependent keys: compute the day from the device's `date` per capture (the task crossed midnight).
- BASE with every W4 menu flag ON already overlapped at 360x640 (stats line vs entry row 8.7 dp; 36 dp at font 1.3) — composites need a flags-ON capture at the smallest size, not per-feature checks.
