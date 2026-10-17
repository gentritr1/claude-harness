---
name: audio-polish-next
description: Premium audio pass — hybrid SFX(procedural)+music(real); Chunks A & C shipped, B & D remain
metadata: 
  node_type: memory
  type: project
  originSessionId: b7b5666e-42d5-4a69-918e-ab5a27fc74d2
---

The post-MVP #3 PREMIUM AUDIO pass (after the visual/feel polish, [[ui-art-polish-direction]]).
**Direction chosen = HYBRID**, mirroring the visual strategy: procedural SFX backbone + real
generated music hero assets + (planned) AudioMixer. Chunk plan: **A** premium SFX synth → **B**
AudioMixer/reverb/ducking → **C** real theme music bed → **D** UI sounds + iOS haptics.

**SHIPPED & committed** on `post-mvp/3-ui-art-polish` (commit 6fa382e, "feat(audio): premium SFX
synth + theme-driven music bed"):
- **Chunk A (SFX):** `AudioManager.cs` rebuilt — 44.1kHz deterministic additive synth (ADSR,
  detune, fixed-seed filtered attack noise, tanh soft-clip). Merge = 12-clip major-pentatonic
  ladder (ToTier→note) + chain-accent + top-tier shimmer; drop=tactile tok, combo=pluck,
  game-over=gentle fall. SFX are procedural → **0 APK cost**.
- **Chunk C (music):** 9 themes → **3 shared looping beds** (serene/warm/cool) in
  `Assets/_Project/Resources/Audio/Music/music_{serene,warm,cool}.mp3` (user AI-generated via
  Suno; mapping: default/void/galaxy=serene, ember/golden/rose=warm, frost/aurora/verdant=cool).
  Imported **mono / Vorbis q0.5 / streaming** (~1MB each, APK-safe). `ThemeDefinition.musicId`
  added + 9 `ThemeDatabase.asset` mappings. AudioManager loads per-theme music via
  `ThemeChangedEvent`, **1s dual-source crossfade** between families, drone fallback if a clip
  is missing. (musicId is NOT in SaveModel → no save-wipe risk, see [[save-additive-schema-safety]].)
- **Mix balance:** real normalized music buried the gentle SFX → added `MusicMixCeiling=0.55`
  (code-side scalar on music output, slider stays raw 0–1) + `SfxAmplitude 0.22→0.5`. Lesson
  captured in `docs/ARCHITECTURE.md` §14.
- **Chunk B (mix glue, commit c0a6bff):** done **code-only, NO AudioMixer asset** — a `.mixer` is
  the one Unity asset Codex can't author safely (effect/snapshot/param GUIDs, no editor to
  validate). Music ducks on big merges (ToTier≥8 / top-tier-bonus, 0.55/0.45, 0.6s recover) and
  the pause menu sweeps music through an `AudioLowPassFilter` (22000→800Hz) + duck (0.6, 0.35s),
  composing with the crossfade via `EffectiveMusicVolume`. Music sources moved to **dedicated
  child GameObjects** so the low-pass stays on music and SFX stays unfiltered. Pause→Settings
  keeps it muffled; Paused→Playing/Home restores. **Reverb deliberately skipped** (global SFX
  reverb risks washing out the tactile drops/merges).

- **Chunk D (UI sounds + iOS haptics, commit f98b35e):** procedural UI SFX via the synth — soft
  click on every uGUI button (`UIKit.ButtonClicked` static event, throttled), overlay open/close
  cues off `GameStateChangedEvent` (Paused/Settings/Codex/Shop/Cosmos/Daily, excl. GameOver), and
  a reward chime on `CodexUnlockedEvent`. `HapticIntensity {Light,Medium,Heavy}` — merge=Light
  (Heavy for tier≥8/top-tier), game-over=Heavy. Android keeps `Handheld.Vibrate()`; **iOS gains
  real taptic** via native plugin `Assets/Plugins/iOS/PlanetDropHaptics.mm`
  (`UIImpactFeedbackGenerator`), `DllImport` guarded `#if UNITY_IOS && !UNITY_EDITOR`, plugin meta
  verified **iOS-only** (Android excluded) so the Android build is unaffected.

**AUDIO PASS COMPLETE (A/B/C/D all shipped on `post-mvp/3-ui-art-polish`).** Remaining/known gaps:
- **iOS haptics ships UNVERIFIED** — no iOS device; only managed + `clang -fsyntax-only` compiled.
  Verify taptic on a real iOS build/device before relying on it.
- Deferred **EditMode audio test** (Chunk A skipped it; tests blocked anyway by the Unity Licensing
  batchmode runner hang the user keeps hitting — worth fixing so verification isn't by-ear only).
- **Reverb intentionally skipped** in Chunk B (global SFX reverb risks washing out tactile SFX).
- **MERGED to main** 2026-06-25 via PR #23 (squash `9e8ebfc`), follow-up to the visual PR #22;
  remote branch deleted. The whole post-MVP #3 (visuals + audio) is now on `main`.

Workflow unchanged: [[planet-drop-orchestrator-workflow]] (I orchestrate/review/git, Codex codes,
user runs Unity from **Boot.unity** + verifies SFX/music by ear), [[reviewing-codex-output]].
