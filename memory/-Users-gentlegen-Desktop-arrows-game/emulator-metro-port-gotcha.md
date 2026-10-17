---
name: emulator-metro-port-gotcha
description: "Android emulator RN debug builds fetch JS from host 10.0.2.2:8081 directly — another project's Metro on 8081 serves the wrong bundle"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 030fc7e5-cf70-4c1f-bc34-ef34df6c38e9
---

RN debug builds on an Android emulator load the bundle from `10.0.2.2:8081` (host loopback), IGNORING `adb reverse`. If another project's Metro owns port 8081 (lucky-shelf's did), the app silently loads the WRONG project's bundle — symptom: "Cannot find native module 'ExpoLinking'" (or any module the other project uses).

**Why:** `npx expo start` won't steal a busy port non-interactively; it skips the dev server, while curl to 8081 answers from the other project and looks healthy.

**How to apply:** When an emulator dev build shows a missing-native-module error for a module the project doesn't even import, check `lsof -iTCP:8081` first. Workaround used for Arrows on emulator-5554: Metro on 8082 + app pref `debug_http_host=10.0.2.2:8082` written via `run-as com.danteb.arrows` into shared_prefs (still set on that emulator). Related: [[levelplay-ads]].
