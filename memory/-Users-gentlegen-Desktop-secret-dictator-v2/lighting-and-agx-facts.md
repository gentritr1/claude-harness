# Lighting, AgX and three.js facts learned in Gate 3 (2026-08-09)

Hard-won, all measured in a headless Chromium tab at 1440×900 against
`npm run dev`, not reasoned about.

## Rendering facts

- **`scene.background` (a plain `THREE.Color`) is NOT tone mapped**; the
  geometry beside it is. The trial background measured exactly `(24,24,40)` =
  the style bible's `#181828` while the lit ground crushed to `(3,3,4)`. That
  mismatch is why the ambient needed lifting, and it will mislead any future
  colour argument that compares a declared hex against a screenshot.
- **Raising a hemisphere light's `intensity` cannot rescue a near-black colour.**
  4× on `#1d2440` moved the ground from `(3,3,4)` to `(3,4,9)`. Intensity
  multiplies a colour; the fix was the colour's hue and value (`#505a8a` over
  `#38385c` at a lower intensity). Darkest trial pixel is now `(1,11,20)`.
- **AgX at these levels is a highlight decision, not a midtone one.** Same rigs,
  tone mapping off vs on: means move by ≤3/255, but the trial frame goes from
  0.48% to 0.13% of pixels at ≥250. The beam pool is the only highlight in the
  game, which is what makes AgX worth having at all. `play.html?tone=linear`
  toggles it.
- Two shadow-casting lights (sun 2048² + beam spot 1024²) ship always-on.
  Toggling `castShadow` at runtime forces a shader recompile and a visible
  hitch; if profiling demands it, use a threshold with hysteresis.

## Measuring against the concept art

Same HSL classifier (hue 15–70°, s>0.16, l>0.18) over the references and the
game. `mood-night-trial.png` 4.46% warm / meanL 0.047 vs game trial 3.43% /
0.107 — close, and it is the signature image. `mood-dusk-gathering.png` 48.4% vs
game 3.6%; `mood-day-discussion.png` 25.2% vs game 2.9%. **Those gaps are albedo,
not light** — the references are amber plaster, timber and cobbles and the
square is grey boxes. No lighting change closes them; the façade and the ground
treatment do.

## Transitions

- A transient state needs its **own** (much shorter) transition or it never
  arrives: a 1.4 s tile sting inside a 1.9 s crossfade reaches ~40% and reads as
  a wobble. Read the override off the *target* so the settle back runs normally.
- "Arrived" must be a **relative** tolerance. A flat 0.5 unit epsilon made a
  beam crossing 140 units need 4.6 time-constants while a hemisphere crossing 3
  needed 1.8, so the readback reported the old state for seconds after the
  screen stopped changing. Now 1.5% of the target's own magnitude, and an
  interrupted fade reports `state: null` rather than a stale one.
