---
name: mapillary-single-shared-token
description: One Mapillary token is shared by every installed copy AND dev scripts; cap any probe script at <=600 req/min and abort on the first rate-limit error
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T13:42:55.920Z
---

There is exactly **one** Mapillary token. `.env`'s `EXPO_PUBLIC_MAPILLARY_TOKEN` is byte-identical
to `BUNDLED_TOKEN` in `src/services/mapillary.ts` (checked 2026-09-16, compared redacted). It ships
inside every APK, so any dev script that calls the Graph API spends quota that live players share.

Limits, SEARCHED 2026-09-16:
- Search API (`graph.mapillary.com/images?bbox=...`): **10,000/min per app**.
- Entity API (`graph.mapillary.com/:image_id`): **60,000/min per app**.
  Source: https://www.mapillary.com/developer/api-documentation
- Exceeding either throttles the whole app ("Application request limit reached") — every player.
- The often-quoted **50,000/day** cap is for `tiles.mapillary.com` (vector tiles), by app ID, per
  Mapillary staff: https://forum.mapillary.com/t/50-000-requests-day-rate-limit-scope/10644 . IP-level
  blocking can also trigger on sudden throughput spikes — that hits the dev's IP, not players'.

**Why:** the content-integrity brief's own critique flagged that its ~17k-request coverage probe on
the shipped token could throttle live closed-test players.

**How to apply:** any script that probes Mapillary — coverage discovery, daily-manifest verification —
must read the token from env without ever printing or writing it, enforce **<= 10 req/s and <= 5 in
flight with a real token bucket**, and **abort the run on the first 429 / "request limit" error**
(checkpoint, then stop — never retry through it). At 600/min a probe uses 6% of the search limit.
If the owner ever creates a second developer token for tooling, prefer it.

Related: [[webviews-load-libs-from-unpkg]]
