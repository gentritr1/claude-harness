---
name: mapillary-api-quirks
description: "Live Mapillary API behaviors that differ from docs (map_features filters, object_type spelling)"
metadata: 
  node_type: memory
  type: project
  originSessionId: a067363c-ba38-4d38-8a74-8d9d95ca553e
  modified: 2026-08-08T14:07:38.168Z
---

Found 2026-08-08 while building the v1.3 sign hint (branch feat/v1.3-playful):
- `graph.mapillary.com/map_features` with only a bbox returns **panoptic features only** (poles, street lights, catch basins). Traffic signs come back ONLY when `object_values=regulatory--*,warning--*,information--*,complementary--*` is passed explicitly.
- Live `object_type` for signs is `trafficsign`, not the documented `traffic_sign` — don't filter on it.
- Image search accepts extra fields cheaply: `captured_at` (ms epoch), `creator{username}`, `thumb_512_url`, `quality_score` (0–1) — all used since v1.3.
- Curl the endpoint with the token from `.env` to sanity-check any new field before coding against the docs; the docs drift.

**Why:** the first hint implementation silently showed "no signs" in downtown Toronto because both doc assumptions were wrong; only a direct curl exposed it.
**How to apply:** treat Mapillary doc field names/filters as hypotheses; verify with one live request first. Related: [[mapillary-token-baked-in]].
