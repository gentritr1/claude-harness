---
name: archive-verification-technique
description: How to verify FJALË archive/date-dependent features — clock-shim server pattern
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a376e78-fea1-4e3f-b833-76f2dbc19ef6
---

The Arkiva feature (play past daily words) can't be exercised on the real clock near launch day (ARCHIVE_EPOCH = 2026-07-16; range is [epoch, yesterday]). Verification pattern that works: a scratch HTTP server that serves the real repo files but injects a `Date` shim into index.html's `<head>` faking "today" (script at scratchpad `shim-server.mjs` pattern — recreate as needed; scratchpads are session-scoped). Run it on its own port so localStorage starts clean per-origin.

**Why:** date-dependent behavior verified only on "today" misses the whole archive path.

**How to apply:** seed a profile via localStorage, play an archive day via `document.querySelector('button[data-date=...]').click()` + `button[data-key=...]` clicks, then diff `__FJALE__.getProfile()` before/after — currentStreak/bestStreak/lastDailyWin must be untouched by archive games. See [[dev-environment-gotchas]], [[daily-pool-immutability]].
