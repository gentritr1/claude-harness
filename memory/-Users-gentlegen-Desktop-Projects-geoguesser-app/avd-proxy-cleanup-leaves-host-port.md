---
name: avd-proxy-cleanup-leaves-host-port
description: "`settings delete global http_proxy` does not clear an AVD's proxy — global_http_proxy_host/port stay set and every game start fails (found 2026-09-17)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T23:47:20.603Z
---

An A2-era agent logged ad requests via `adb shell settings put global http_proxy 10.0.2.2:8888` on the
Pixel_8_Pro AVD (2026-09-16 14:52Z) and "cleaned up" with `settings delete global http_proxy`. Android
had already derived `global_http_proxy_host=10.0.2.2` and `global_http_proxy_port=8888`, which the delete
leaves in place, so the proxy stayed live: with nothing listening on 8888 every game start failed on the
AVD until E1b-2's implementer noticed (2026-09-17).

**Why:** the proxy technique is documented in EXECUTION.md §3, so the next agent to use it repeats the
trap; a silently broken AVD also poisons later device evidence ("loads fail" looks like an app bug).

**How to apply:** clear with `settings put global http_proxy :0` AND delete `global_http_proxy_host` /
`global_http_proxy_port`, then read all three back and prove a game start reaches a panorama. Any brief
that uses a device proxy must name this cleanup. Target adb by serial — the owner's other project runs
fleet_floor_api31 alongside.
