---
name: web-previews-show-fallback-fonts
description: "Expo web screenshots render art_v2 text in a browser serif, because the app fonts exist only in android/app/src/main/assets/fonts; the owner judged \"the new font\" on that fallback"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-06T15:10:37.958Z
---

On 2026-10-06 the owner said the new font "doesn't look good". Every art_v2 screenshot sent since ART-2 had been rendered
on Expo web, which has no @font-face for Overpass, Overpass Mono or Big Shoulders. Those TTFs ship only in
android/app/src/main/assets/fonts and nothing loads them on web, so the browser fell back to a default serif (Georgia or
Times). The captions said "fallback fonts", but that did not register as "this is not the font". A side-by-side with the
real TTFs (docs/plan/evidence/font-check.html) settled it: the owner kept the approved Road & Signage fonts.

**Why:** a taste verdict on a fallback can reverse an approved decision for the wrong reason. It nearly did.

**How to apply:**
- Every web screenshot of the art_v2 look must inject the real fonts: @font-face from the android asset TTFs, base64,
  injected through CDP before load. Otherwise label the shot "LAYOUT ONLY, wrong font" in the image itself, not just in
  the caption.
- Font and taste judgements go on device screenshots, or on a page that loads the real TTFs.
- A web harness should assert that a real font loaded (`document.fonts.check`), the same way it asserts the Graph
  requests were blocked.

Related: [[web-preview-qa-gotchas]], [[custom-font-android-gotchas]], [[pixel-exact-before-after-screenshots]].
