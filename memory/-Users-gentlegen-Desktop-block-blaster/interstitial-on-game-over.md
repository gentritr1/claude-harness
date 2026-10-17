---
name: interstitial-on-game-over
description: "2026-07-27 added an AdMob interstitial on Game Over -> Play Again only, with unit-tested pacing; adding it invalidated \"no forced ads\" copy in five places"
metadata: 
  node_type: memory
  type: project
  originSessionId: d535c8d5-5f0d-4b2d-86f0-def74e501750
  modified: 2026-07-27T21:08:26.078Z
---

2026-07-27: the user asked for a **banner on the Game Over screen**. I argued
against it and they took the alternative: a **paced interstitial** instead.

**Why not the banner:** in that modal a banner would sit directly above
"Shuffle & Continue" / "Play Again" — the buttons the player is already reaching
for. That adjacency is exactly what AdMob's invalid-traffic policy targets, and
on a new account it is the least affordable risk. An interstitial at a natural
break has no adjacency problem and earns more. A banner/MREC would also have
needed a **native view component** (Expo `View` definition + layout), a much
bigger lift than the fullscreen path that already existed.

**Placement rule that matters:** the interstitial fires from
`restartFromGameOver` (Game Over → Play Again) **only**. `restart` is shared with
the mid-run reset button in the header, and firing an ad there would be an
unexpected mid-session interruption. Anyone touching this must keep the two
paths separate.

**Pacing lives in `src/ads/interstitialGate.ts`, pure and unit-tested (8 tests):**
no interstitial until 2 runs have finished, at most one per 3 minutes, and none
within 60s of a rewarded ad (never stack two ads). `lastInterstitialAtMs` is
stamped **before** the ad runs, so a no-fill cannot retry on every game over.

**The scar worth remembering — adding an ad format silently falsifies your copy.**
"No forced ads" / "ads only start after you choose Watch Ad" was written in
**five** places: the Play full description (already sitting in the Desktop
listing folder ready to upload), `PrivacySupportModal`, the privacy policy,
`store.config.example.json`, and `product.md`. All five became false the moment
the interstitial landed, and Play's ads declaration is checked against exactly
that wording.
→ **Detection rule: any change to which ads exist must be followed by
`grep -rn "forced ad\|only start\|no ads between"` across docs, listing text,
and in-app copy — including the already-exported Desktop listing folder.**

Related: [[admob-migration]], [[release-folder-recipe]].
