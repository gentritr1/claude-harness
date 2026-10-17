---
name: w5-02-08-harness-gotchas
description: W5-02/W5-08 (2026-09-27) - uiautomator escapes emoji as &#NNN;, the "#" toggle eats solver taps, capture seeds leave a composed menu that moves Play, zoomed-camera solve by pan+re-register, same-APK null itself hits p<0.05
metadata:
  type: project
---
- uiautomator dump writes 💡 as `&#128161;` (and ' as &apos;): decode numeric entities before matching labels, or a "wait until hint enabled" silently times out (W5-02 first menu run).
- The POLISH-T4 "#" grid toggle (44 dp, bottom-right, hitSlop 8) floats over the board: a solver tap there toggles grid lines, the arrow stays, later taps go blocked. Exclude its box from "visible cell" (artifacts/W5-02/scripts/cap502.mjs).
- META_ZOOMED_CAMERA win panels are reachable: level index 52 (Square 16x16) opens at fit on 411 dp; at 360 dp tap any visible cell of the arrow, else a long horizontal swipe pans to the clamp, re-register on the REMAINING arrows (reg507.py), ~14 registrations per solve.
- Capture seeds with total_solved > 0 leave a COMPOSED menu: pace503's fixed Play tap (720,1925) then opens "Today's board" (63 left). Perf runs must reseed total_solved=0.
- Same-APK null in a P/A/N rotation reached p=0.043 on one of 7 game metrics (P sits early more often): one flagged metric at p~0.03 is the instrument's false-positive level; compare ON against ALL OFF runs too.
- react-native-svg Android SvgView caches a bitmap and draws it per frame; invalidate() recycles it. Idle-menu ON runs showed a small RT p95 (+0.6 ms) / janky increase on the SwiftShader emulator (post hoc) - device check before any ART_ICONS flip.
- bash on this Mac is 3.2 (no `declare -A`); zsh does not word-split "$VAR" in for-loops (a `for f in $F` swap loop silently did nothing - use bash scripts for file swaps).
