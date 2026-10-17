---
name: shipping-defects-found-2026-09-09
description: "Four defects live in the shipped build found by the 2026-09-09 audit: reduce-motion feedback blackout, interstitial counter reset, splash with no backstop, test-ad modal in production"
metadata: 
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-09T15:03:12.321Z
---

Found 2026-09-09 auditing versionCode 6. All are in the shipped build; none were known.

**1. Reduce-motion feedback blackout (accessibility + teaching failure).** VERIFIED by computing
the curves. Every `withTiming` in the feedback layer uses Reanimated's default
`ReduceMotion.System`, so with the OS setting ON progress jumps straight to 1. At k=1:
`blockerOpacityAt(1) = 0`, `blockedBumpAt(1) = 0`, hint pulse amplitude `= 0`. A reduce-motion
player therefore gets **no blocker flash, no bump, and no hint pulse** — the game's only explanation
of its core rule vanishes, and the *rewarded-ad-paid* hint renders nothing at all. Sites:
`src/ui/StaticBoardSurface.native.tsx:264,:308,:348` and `src/ui/BoardView.tsx:842,:887,:934`.
The fix is not just `ReduceMotion.Never` — a reduce-motion player still needs a *static* magenta
blocker state, not a shorter animation.

**2. Interstitial counter resets on every cold start (revenue).** `src/ui/ads.tsx:255`
`let finishedGames = 0` is a module-level in-memory variable and is not in
`SaveSystem.PersistenceKeys`. A player who kills the app between levels — the exact session shape
PRODUCT.md describes ("commute, couch, before bed") — never reaches `GAMES_PER_INTERSTITIAL = 2`.
Separately, the interstitial is only reachable from the win panel's *Next level*; the loss panel's
*Retry* calls `loadLevel` directly, so a struggling player never sees one either.

**3. Splash has no completion backstop.** `src/ui/SplashScreen.tsx:47-49,:53-56` — both `onDone`
paths fire from a Reanimated completion callback. No JS timer, no AppState-active fallback, and
`grep AppState src/` = 0 hits app-wide. If the animation never completes the player is stuck on the
splash. This is the exact "visibility-critical property that only reaches its resting value if an
animation completes" pattern from the global harness §6.

**4. The simulated TEST AD modal ships in production.** `AdHost` is compiled into and mounted in
release builds and is the fallback whenever `initAds()` fails. `initAds()` is called once from a
`useEffect([])` and never retried, so a cold start with no network can leave real players seeing a
fake "TEST AD / A word from our sponsor" panel. Rewarded no-fill is also a silent no-op — the button
does nothing and says nothing.

**Why:** all four are invisible to the existing verification stack (node-env Jest on `.test.ts`
only, so every `.tsx` is untested; the Android harness sets `animator_duration_scale 0`, which is
itself the reduce-motion path, and PERF_MODE boots straight into `game` so splash/menu are never
exercised).

**How to apply:** these are the W0 "stop the bleeding" items and should land before any feature work.
See [[game-design-truths-measured]] and [[perf-architecture-and-evidence]].
