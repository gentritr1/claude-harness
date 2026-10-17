---
name: avd-stale-global-proxy
description: "Pixel_8_Pro AVD carries a stale global HTTP proxy (10.0.2.2:8888, nothing listening) — every game start fails with 'Could not find street-level imagery'"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-17T03:16:52.872Z
---

Found 2026-09-17 during E1b-2 device QA. `adb shell settings get global global_http_proxy_host` → `10.0.2.2`,
`global_http_proxy_port` → `8888` (the plain `http_proxy` key reads `null`, so it is easy to miss), left
from an earlier ad-request logging session (EXECUTION.md §3 proxy recipe). Nothing listens on host port
8888, so every app fetch fails, and `boxCandidates` in src/services/mapillary.ts swallows each failure as
"no candidates": after 8 tries the app shows the coverage error. Ping and DNS from the emulator still
work, which makes it look like a Mapillary outage.

**Why:** two full capture runs were lost to it before the cause was found. The same symptom as a dead network.

**How to apply:** before any in-round device QA, read both global proxy keys. Either clear them (owner's
call: it is device config) or run a local pass-through proxy on 127.0.0.1:8888 for the session (E1b-2 did
that, evidence in docs/plan/evidence/e1b-2/device/passthrough-proxy.cjs) and stop it afterwards. A game
starting within ~10 s is the check that the network path works.

**It comes back on every quickboot (found 2026-09-17, E1b-3).** E1b-2's fix round cleared the keys, yet the next
boot read host 10.0.2.2 / port 8888 again. Cause: the AVD quickboots from snapshot `default_boot`
(`~/.android/avd/Pixel_8_Pro.avd/snapshots/default_boot`, saved 2026-09-16 21:42 local, after the proxy was set),
and agents boot with `-no-snapshot-save`, so every change made in a session — the proxy clearing, installs,
settings — is discarded at shutdown. The emulator log says "Loading snapshot 'default_boot'"; boot_completed within
seconds is the tell. Clearing inside a session works for that session only. Making it stick needs a boot that saves
a new snapshot (e.g. clear the keys, then exit without `-no-snapshot-save`) — that rewrites the AVD's snapshot, so it
is the owner's or controller's call; E1b-3 did not do it.
Related: [[pixel-exact-before-after-screenshots]], [[verify-webview-maps-without-a-device]], [[avd-proxy-cleanup-leaves-host-port]].
