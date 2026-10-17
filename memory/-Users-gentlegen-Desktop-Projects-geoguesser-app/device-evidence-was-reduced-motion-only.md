---
name: device-evidence-was-reduced-motion-only
description: "SND-1's device log and all its GameSummary tests ran with reduced motion ON; the animations-ON path (cue fires at resume) was never exercised"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-08T00:27:35.650Z
---

SND-1 (2026-10-08): the bug evidence (v2 logcat) was captured with animator scales 0, and all 5 rendered GameSummary tests used reduceMotion: true. With animations ON the count-up settles only after the host resumes, so the cue fires during the post-ad re-warm and is lost as why=cold. Review F1 found this; the fix had passed every gate.

**Why:** our pixel-exact harness sets animator scale 0 by default ([[pixel-exact-before-after-screenshots]]), so device evidence silently covers only the reduced-motion branch of any timing-dependent behaviour.

**How to apply:** pattern → detection rule → brief update. Timing/lifecycle evidence captured at animator scale 0 → check the device run's animator scales before trusting it for a timing bug → every brief touching a count-up, settle or resume path requires tests and a device run with motion ON AND OFF. Related: [[never-read-nativeevent-inside-a-state-updater]].

**Correction, 2026-10-09 (ART-4c device run):**
- **Finding:** with ONLY the animator scale at 0, the app did NOT enter reduced motion. The return sweep ran normally. `skip why=reduced` appeared only with all three scales at 0.
- **Source (the agent read it; I did not re-check):**
  - RN `AccessibilityInfoModule.kt:101-116` reads `transition_animation_scale == 0`;
  - Reanimated `NativeProxy.java:484` does the same.
- **So:** earlier "reduced motion" evidence that set only `animator_duration_scale 0` may never have exercised reduced motion. It only shortened Android animators.
- **How to apply:**
  - Reduced motion: set `transition_animation_scale 0` (or all three).
  - Motion ON: set all three to 1.
  - Print all three read-back scales in the evidence.
