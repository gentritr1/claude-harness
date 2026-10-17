# Warm budget is a shared, nearly-spent resource — and how the anti-tell gate was made falsifiable

Gate 13 (`ambience-weather`, 2026-08-10), lanterns + the board-as-weather.

## Detection rules earned here

- **Measure the baseline on a worktree at the branch point, never from the last
  step doc.** Adding lanterns took the trial frame to 21.8% warm against a 10%
  ceiling. A parallel session had just landed warm plaster and cobbles, so
  "their albedo work spent the budget" was the plausible and completely wrong
  read. `git worktree add <scratch> <branch-point>` + a second vite on 5174 said
  the square was at 7.21% with no lantern hung — all 14.6 points were mine.
  Pattern -> rule: **any change that adds warm to a night frame must quote a
  before number it took itself, on a worktree, with the same camera.**
- **The warm budget now has ~2.3 points of headroom and more than one claimant.**
  "It was under budget last week" is a claim about somebody else's commits.
- **A permutation test over a player-safe view is close to tautological.** The
  channels are pure functions of a projection that carries no roles, so they
  agree trivially. Made meaningful by three halves: check the *view* under
  permutation too (the premise), audit the composed pipeline through a recording
  Proxy (catches non-role-shaped tells), and **mutation-test the detector** with
  injected tells that must each be caught plus a control that must be caught by
  nothing.
- **The mutation test found its own bug immediately**: mutants applied *after*
  the permutation saw the same permuted game, agreed with themselves, and all
  seven reported clean. Rule: **a mutation test must assert `caught > 0` per
  mutant, or it is a green light with nothing behind it.**
- **A scripted capture must stop the match loop before forcing a debug state.**
  `setLighting` aims the rig; the next `refresh()` aims it back, so three
  "weather" frames were three different lighting states. The giveaway was a
  nonsense metric (lit fraction 37.9 -> 71.1 -> 25.2). Rule: **print a second,
  redundant metric beside the one you care about — an impossible shape in it is
  the cheapest detector of a broken harness.**
- **Two placements of one GLB share the loader's cached material.** Extinguishing
  one lantern by writing its emissive put out both. Clone per placement, dispose
  only what you cloned. (Third occurrence of the shared-cache family, after cast
  geometry and per-seat material overlays.)
- **A light going out is not a lamp going out.** The asset's authored emissive
  kept the glass burning; the feature's whole point ("nobody had to be told the
  score") needs the visible body too.

## Facts worth keeping

- Trial frame, 1280x720, HUD composited, project classifier (hue 15-70,
  s>0.16, l>0.18): 7.21% baseline -> 7.74% shipped, budget 10%. HUD costs
  +0.68 pt, same as step-11 measured independently.
- Lantern rig sweep: d9/decay1.4 = 21.80, d9/decay2 = 9.19, d6.5/decay1.6 = 9.40,
  **d6.5/decay2 = 7.77 (shipped)**, d4.2/decay2 = 7.36 (too tight to read).
- Weather at 0/1/2 Seizes, same camera and forced state: warm 8.53/7.76/5.28,
  lit 27.44/26.21/22.61 — both monotonic.
- Presentation flicker is ONE-SIDED (`1 - amp*sample`, sample in [0,1]) so every
  declared warm budget stays an upper bound. A two-sided flicker would quietly
  turn every warm measurement in docs/ into a statement about the average frame.
- Reform's feedback is stability, never brightness: steadying the flame is the
  only one of the three candidate responses that is budget-neutral by
  construction.
