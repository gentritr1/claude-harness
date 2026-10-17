---
name: sound-design-2026-09-30
description: Owner finds the exit sound irritating; Higgsfield can't make SFX; candidates are synthesized from scripts/generate-sfx.js
metadata:
  type: project
---

Owner (2026-09-30): current exit sound is "irritating", wants cute ASMR sounds. Measured cause: pop is a bright 1100→650 Hz blip with a 2 ms noise click at -6 dBFS, climbing +16 semitones on fast chains (pop7 ≈ 1.9 kHz zero-cross).

Higgsfield MCP `generate_audio` is **speech-only**; its SFX model (mirelo) is restricted to its game-generation pipeline — do not use it for sound effects. Sounds are synthesized by `scripts/generate-sfx.js` (writes assets/audio + iOS Resources).

Candidates rendered 2026-09-30 to ~/Desktop/Arrows-sound-candidates-2026-09-30 (script in session scratchpad sfx/candidates.js): A soft bubble "plip", B wood marimba, C soft kalimba — all -12 dBFS, no click, low-passed, ±cents jitter, same pentatonic ladder. **Awaiting owner pick** before changing generate-sfx.js (taste call). Related: [[arrow-skins-direction-2026-09-29]].

Update same day: owner found tonal sounds "too annoying", asked for **subtle soft wind**. Rendered D breath / E swish / F breeze+hush-note (filtered noise, peak at 16 ms, -16..-18 dBFS vs today's -6; scratchpad sfx/wind.js). Awaiting pick.

**Ruling 2026-10-06:** after hearing the 8-tap ladder vs flat clips (artifacts/W2-12/), owner said the arrow sound is bad — **no exit sound at all**, keep the other sounds. Implemented as `EXIT_POP_ENABLED = false` in src/ui/exitCombo.ts (`feedbackSoundOn` gates native + fallback; exit haptic kept). Candidates A–F are effectively declined unless the owner reopens it; the ladder code stays for a future replacement.
