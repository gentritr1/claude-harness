---
name: globe-after-entrance-direction
description: 2026-10-08 "globe looks static" answer — night band audited accurate; ranked ideas (Sun catches up first); awaiting owner pick
metadata:
  type: project
---
Owner asked (2026-10-08) why the home globe looks static after the ART-4b entrance spin and whether the night is accurate.

- The night band was audited (agent run, scripts in the scratchpad audit/ folder). It is ACCURATE: within 0.01 deg of NOAA, within 1 min of 66 published sunrise/sunset times, and identical in 5 time zones (it uses UTC only).
- The today slice is a calendar marker at 0 deg E, not the player's location. That follows the owner's fixed-view decision; treat it as a copy question, never a reversal ([[brief-must-not-reverse-owner-decisions]]).
- Ideas ranked by me + Fable 5.1, prototyped on the Claude Design canvas https://claude.ai/artifact/Ep2maH5ozvca9gDw5L91Pz:
  1. The Sun catches up (ART-4c): the resume spin also sweeps sunView from the background wall clock to now.
  2. Drag to spin, reduced to a 1:1 drag plus a spring home. It needs react-native-gesture-handler (not installed), a resident Skia layer and a coast stroke in the shader.
  3. Today's fill from the pole: reshape the existing weekReward FadeIn as an SVG clip, not a shader.
  4. New day from the east: parked, because it fires on cold start, where the spin never plays.
- No telemetry exists, so every "A/B" means the owner looks at it on the phone.

**Why:** ambient loops fail the frequency gate. The ART-4b phone smoothness is still UNVERIFIED, so nothing should stack a resident Skia layer on it first.
**Owner pick (2026-10-08): ALL of them, as time-triggered easter eggs, smooth with stable fps.** Unit queue, each behind its own default-OFF flag and stacked on art-4b:
- ART-4c: the sun catches up (in progress);
- ART-4d: the today fill wipe (SVG clip);
- ART-4e: the new-day slide, riding the owed spin when the day key changed since the last home in this process (memory only; a cold start skips it);
- ART-4f: drag and flick, with a hard flick doing a full turn as the easter egg. Owner 2026-10-08: YES to adding react-native-gesture-handler (npx expo install) for ART-4f; new-day slide ONLY when the app stayed open (no persisted field).

**How to apply:** none of these merge to feat/next-level before the owner accepts ART-4b on the phone.

Canvas gotcha (2026-10-08): the owner saw no animation on boards 2 and 3. In a local harness the engine ran fine: the ease-out effects finish ~75% in 150 ms and read as an instant swap, and the boards shared a `data-globe="one"` selector. Fix: per-board canvas ids, lazy init from the rAF loop, and a slow-motion x4 toggle. Prototype effects under ~600 ms need a slow-motion control to be judged.
