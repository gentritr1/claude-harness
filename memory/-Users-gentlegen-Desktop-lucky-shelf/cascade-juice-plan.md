---
name: cascade-juice-plan
description: "Fable's ranked \"make combos feel alive\" animation plan —"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3bb5b22f-cf63-495e-be5e-4f3f9b194708
---

**FEEL GATE CLOSED (2026-07-11, human):** after the NaN-transform fix (`6c037c3`) the human played a
cascade with a combo on the sim and ruled "animations look smooth now" — items #1 travel, #2 receive
bump, #4 combo hop are ACCEPTED. #3/#5 remain queued/optional.

**Context (2026-07-11):** human said combos "look like lines, not animations"; wanted more life
without perf cost. Consulted Fable 5 (agent) for a plan; root diagnosis: a ruleFire was a 3px bar
that scaled in — nothing physical moves. Fix = a **give → travel → receive** chain. The cascade
sequencer is SERIAL (one trace event on screen at a time, 260ms/130ms dwell), so the perf budget is
tiny (≤ a handful of concurrent Reanimated animators; NO Skia needed; this is the web-verifiable
path). Full plan in the agent transcript; ranked by feel ÷ cost:

1. **Coin-token travel — SHIPPED (unverified feel).** Reworked `src/juice/cascade/CascadeArrow.tsx`:
   a chunky gold coin lobs source→target with a sine arc + overshoot landing + tail-fade; the old
   line is demoted to a faint comet trail; arrowhead deleted. New tokens `motion.durations.tokenTravel`
   (renamed from `arrowDraw`) + `motion.cascade.{tokenArcFraction:0.16,trailOpacity:0.35}`. Passes
   `player.speed` so flight halves at 2× (fixes a latent truncation bug). Reduced-motion: coin static
   AT target, trail full, no fade/scale. tsc + 292 tests green. **GATE: iOS-sim recording of a ≥3-fire
   day + a reduced-motion recording.**
2. **DONE (unverified feel, uncommitted).** Target squash-and-stretch: `CascadeItem` fires a
   non-uniform squash (scaleX +0.09 / scaleY −0.11) via `motion.springs.impact` whenever its
   `frame.slots[key]` total GROWS (a coin landed), delayed by `tokenTravel` so it fires on arrival.
   Coin-synced without threading event data; skips initial base + reduced motion. Completes give→receive.
3. Source "lean" toward target as the coin departs (±4° rotate).
4. **DONE (`8e4c467`, unverified feel).** Combo "members take a bow": named-combo members hop once in
   reading order (`frame.combo.slots` + `motion.cascade.hopY/hopStaggerMs`); reduced motion = static
   gold ring (`itemMember` style) for the banner's lifetime. ≤5 animators, once per combo.
5. Day-total coin absorption: 4 coin dots fly into the DAY TOTAL pill on dayTotal. STILL QUEUED.
   (#3 source-lean also queued.)

**Also shipped this session:** cascade #1 coin-token + pacing (`0258875`), #2 receive-squash
(`f6226d5`), audio revert (`0070738`), build card (`3c18b3a`), summary personal-best rows clearer
(`a557a81` — killed the double-"Best" label/caption + redundant tied number). Human accepted #1/#2 on
device; #4 + summary pending eyeball.

**Pacing pass (2026-07-11 feel-gate, unverified/uncommitted), TWO rounds:**
- Round 1: `cascadeStep` 260→340, `tokenTravel` 180→220 + `Easing.out(Easing.cubic)`, softer landing.
- Round 2 (human still saw "green lines too fast"): ROOT CAUSE — the demoted trail line was tinted by
  `arrowPalette` (green for some sources) and the coin faded to opacity 0 on arrival, so the LINE was
  the lingering visual, not the coin. Fix: **removed the trail line entirely** (no more lines at all),
  the coin now HOLDS on the target (no fade) with its ring tinted by the source colour + a `shadows.card`
  lift, `cascadeStep` 340→**380**, `tokenTravel` 220→**280**. Removed dead `motion.cascade.trailOpacity`.
  If the human still reports "green lines," suspect a DIFFERENT element (RowAuraGlow sweep), not the ruleFire. NOT yet done (offered as next step if still not coherent enough):
delay the beneficiary slot's count-up/pulse to the coin's ARRIVAL so the number ticks as the coin
lands (currently ticks at step start, while the coin is mid-flight) — `useCountUp`/`SlotTag` in
CascadeLayer would take a `startDelay`, active-slot-only, skip self-fires.

**Audio "music plays on combos with music off" — NO music-bed bug; FIXED the real cause (`29a0bdf`).**
`setMusicTrack` (run.tsx:69) already no-ops when `musicEnabled` is false. The sound was the SFX channel
— `playCascadeSting()` (run.tsx:111, on score) + `playDiscoveryJingle()` (CascadeLayer:133, first-ever)
— which gated ONLY on `sfxEnabled` (default on) and are the ONLY two sfx in the app, both the melodic
`cascade.mp3` placeholder → read as "music." Fix attempted (29a0bdf) then REVERTED
(0070738) — human decided the melodic combo stings are wanted even with music off, so they ride
`sfxEnabled` alone (the "Sound effects" toggle is the control). NOT a bug; final state = SFX-gated. Real polish still
pending: the bespoke discovery jingle asset (RELEASE-PLAN Gate 1.5) — placeholder doubles on first-ever
combos (jingle + payout sting, same mp3). Recording the human sent has NO audio track (video-only).

**Explicitly NOT doing (Fable):** ambient idle-bob on all 16 shelf items (kills the still-shelf
contrast + `screen-animations` scar), Skia per-fire particles (wasm scar, casino-trend; apex
`SparkBurst` keeps that budget exclusive — spectacle-without-swing), persisting arrows across steps,
screen shake/wash on normal tier (byte-identical guarantee at `CascadeLayer.tsx:313`).

**Invariants for every item:** all motion values live in `motion` in tokens.ts (no inlines);
never touch `useCascadePlayer` cadence/`stepIndex`; write the reduced-motion branch FIRST; verify on
the iOS simulator ([[ios-ui-verify-on-simulator]]) — web can't prove this motion class.

Related: [[screen-animations]] [[b-m6-cascade-spectacle]] [[cascade-self-fire-pop]] [[text-centering-pattern]]
