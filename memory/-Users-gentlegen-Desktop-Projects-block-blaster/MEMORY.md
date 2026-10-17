# Block Destroy — memory index

- [Project identity & release](project-identity-and-release.md) — com.blockrow.game, keystore in credentials/, version duplicated in app.json + build.gradle, 1.0.0(3)
- [Env fail-closed ads](env-fail-closed-ads.md) — banner unit now a source constant in src/config/ads.ts; privacy/support URLs still missing from .env
- [Web preview limits](web-preview-limits.md) — browser pane can't click RN Pressables here; screenshots only, gameplay is device-only
- [Android measure offset](android-measure-offset.md) — measureInWindow drops the status-bar inset under edge-to-edge; drag/burst overlays drew one row high; use measure() pageY
- [Reanimated loop parking](reanimated-loop-parking.md) — withRepeat(withSequence(+withDelay)) parks after one cycle; drive a single linear phase ramp instead
- [Animation-gated visibility](animation-gated-visibility.md) — 'lost pieces' emulator repro was a HARNESS false positive (tap cancelled by HOME); useSettle/tree-swap hardening verified for reveal-vs-pause; unplayable opacity 0.28→0.45; device cause still unconfirmed
