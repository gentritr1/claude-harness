---
name: webviews-load-libs-from-unpkg
description: Both WebViews fetch MapLibre and mapillary-js from unpkg at runtime with no SRI — an outage breaks the game and the guess map fails silently
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-09T18:05:46.224Z
---

`src/components/webviewHtml.ts:6-9` loads MapLibre GL and mapillary-js from
**unpkg.com at runtime, on every WebView mount**, with no `integrity=` attribute and
nothing bundled. Measured 2026-09-09: **0.55 MB compressed / 2.31 MB uncompressed**
per cold load.

Two consequences:

1. **Availability.** unpkg has no SLA. `streetViewHtml` has a try/catch that posts
   `{type:'error'}`, so the panorama at least says "This view could not be loaded".
   `guessMapHtml()` has **no try/catch** — `maplibregl` being undefined kills the
   script before the click handler is installed, giving a silent black rectangle with
   a working "Make guess" button and no pin possible.
2. **Supply chain.** A compromised or MITM'd response executes arbitrary JS inside a
   WebView that holds the Mapillary token (injected at `webviewHtml.ts:145`) and a
   `postMessage` bridge to the Zustand store. `StreetView.tsx:52` sets
   `originWhitelist={['*']}`. Pinning the version does not help without SRI.

**Why:** this is one of two things that can brick 100% of installs at once. The other
is the hardcoded Mapillary token (`mapillary.ts:15-18`), which also means `hasToken()`
can never return false — making `needsToken`, `NEEDS_TOKEN_MESSAGE` and their branches
dead code.

**How to apply:** add SRI or vendor the libraries. Both fixes are pure-JS string
changes — but with `expo.modules.updates.ENABLED=false` (`AndroidManifest.xml:18`) they
require a full Play release, which is itself currently blocked. This is the strongest
argument for adopting expo-updates: the "no backend" constraint means no accounts and
no server-held player state, and the app is *already* a hard runtime client of unpkg,
tiles.openfreemap.org, graph.mapillary.com and AdMob.

Related: [[play-targetsdk-36-blocks-updates]], [[verify-webview-maps-without-a-device]]
