---
name: verify-webview-maps-without-a-device
description: How to actually see the WebView maps render without an emulator — compile webviewHtml.ts and drive the generated HTML in a browser
metadata:
  type: project
---

The guess and result maps are HTML strings built by
`src/components/webviewHtml.ts` and handed to a `react-native-webview`. They can
be verified without building the app:

1. `./node_modules/.bin/tsc src/components/webviewHtml.ts --outDir <tmp> --module commonjs --target es2020 --esModuleInterop --skipLibCheck`
2. `require()` it in node, write `guessMapHtml()` and `resultMapHtml(a, b)` to files
3. serve with `python3 -m http.server` and open in a browser
4. stub `window.ReactNativeWebView = {postMessage: ...}` to capture the bridge payloads

Used on 2026-08-28 to confirm the OpenFreeMap/MapLibre swap: style loaded (47
layers), tiles rendered with labels, OpenFreeMap attribution and no "API KEY
REQUIRED" watermark, tap posted `{type:"guess",lat,lng}`, result map drew both
markers plus the dashed line.

**Why:** this catches real rendering failures in seconds where reading the diff
proves nothing — but it is Chromium, not the Android System WebView.

**How to apply:** treat it as necessary-not-sufficient. Device rendering stays
UNVERIFIED until someone opens the build. Also confirm the change reached the
shipped bundle: `strings -a base/assets/index.android.bundle | grep -c <url>`
(it is Hermes bytecode, so plain `grep` on it misbehaves).
