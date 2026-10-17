---
name: seed-store-from-browser-for-visual-qa
description: "How to visually verify state-gated screens (RoundResult, GameSummary) on expo web without playing a game"
metadata: 
  node_type: memory
  type: project
  originSessionId: f540ac07-823f-4ad3-b751-b24154396262
  modified: 2026-08-31T20:38:55.091Z
---

To eyeball screens that only render mid-game, temporarily append to `src/store/gameStore.ts`:
`if (typeof globalThis !== 'undefined') (globalThis as any).__gameStore = useGameStore`
then drive state from the browser console: `__gameStore.setState({ status: 'revealed'|'finished', rounds: [...], isNewHighScore: true, ... })`. Keep `guess: null` in seeded rounds so RoundResult skips its WebView (react-native-webview has no web impl). Remove the harness after — verified clean with tsc on 2026-08-31. Related: [[verify-webview-maps-without-a-device]].

**Why:** RoundResult/GameSummary need real game state; web preview + seeded store verifies layout and animation choreography without a device or Mapillary quota.
**How to apply:** Screenshot at ~0.4s / mid / settled to verify anticipation → payoff ordering, not just the final frame. Device is still required for haptics and spring feel.
