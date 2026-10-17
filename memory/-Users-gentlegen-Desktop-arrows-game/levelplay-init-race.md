---
name: levelplay-init-race
description: LevelPlay.init() resolves on dispatch not completion — loadAd before onInitSuccess fails with error 625
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 030fc7e5-cf70-4c1f-bc34-ef34df6c38e9
---

`LevelPlay.init(request, listener)` in the RN wrapper resolves its promise when the native call is *dispatched*, not when init *completes*. Calling `loadAd()` right after `await init(...)` fails with errorCode 625 "Load must be called after init success callback". The pre-migration code (ported from Unity) had this bug; caught only via emulator logcat.

**Why:** SDK wrappers often return dispatch-promises; completion arrives via listener callbacks/events.

**How to apply:** Gate all post-init SDK calls on the actual `onInitSuccess` callback (wrap init in a promise resolved by the listener). Review rule: for any SDK "init then use" sequence, verify on-device via logs which moment the promise actually represents — logcat evidence, not wrapper docs. Detection: grep logcat for the SDK's error codes on first device run.
