---
name: android-measure-offset
description: measureInWindow vs RNGH absoluteY mismatch on Android edge-to-edge shifted drag/burst overlays one row up
metadata: 
  node_type: memory
  type: project
  originSessionId: 2051cf29-c6f2-47e3-8fbd-76df141b5684
  modified: 2026-09-02T14:48:36.978Z
---

Found 2026-09-02 on the Pixel 8 Pro emulator (release APK, versionCode 3): `Grid` measured itself with `measureInWindow`, which under Android edge-to-edge (RN 0.85 / Expo SDK 56, `edgeToEdgeEnabled=true`) returned a y **144px (status-bar height) too small**, while RNGH `absoluteY` and the root-level overlay layers use full-screen coords. Net effect: the floating dragged piece and ClearBurst flashes drew one row ABOVE the true cell, and drops aimed at row 7 computed row 8 → rejected. Pre-existing before this branch (same measurement code at HEAD). Fixed by measuring with `measure()` pageX/pageY (root-relative) in `src/components/Grid.tsx`.

**Why:** the two APIs disagree by the status-bar inset only when the RN root extends under the status bar; the web preview never shows it. The tap-placement path (ghost preview drawn inside Grid) was always correct, which is what made the drag path look "randomly cancelled".

**How to apply:** any overlay positioned from a measured view must use the same coordinate API as the gesture feeding it; verify on a real Android build with a hover screenshot (floating piece vs ghost cell must coincide). Detection rule: an adb `input swipe` drop that visually snaps but reverts = coordinate mismatch, not an injection artifact.
