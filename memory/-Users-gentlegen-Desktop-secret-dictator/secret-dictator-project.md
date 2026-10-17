---
name: secret-dictator-project
description: "Secret Dictator — playable Secret-Hitler-style game built from a claude.ai design doc; stack, art pipeline and where the rules came from."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9d90e3f0-7698-483d-a615-b31b363ed1c5
  modified: 2026-08-08T16:47:01.404Z
---

Built 2026-08-07/08 from the claude.ai/design project `Game screen layout variants`
(`ce1b0895-0f2c-449b-9fe2-c0ce4fd0e9ce`), file `Secret Dictator.dc.html`. Pushed to
`git@github.com:gentritr1/secret-dictator.git` (branch `main`).

**Status (2026-08-08, loop closed, user accepted):** four review rounds shipped —
base game, 9b motion-spec alignment, walkable plaza staging (new plates, depth
scale, gate entrances, citizen portrait nameplates), and free-roam agency
(autonomous bot roaming + click-to-move). Design doc complete through Turn 10 with
`design/HANDOFF.md`. Open cosmetics: chip overlap at 44px personal space, small
chips at the 10p reveal, Loyalist ~63% bot winrate. Higgsfield balance ~71 credits.

**Scope the user chose:** playable vs AI, single-file-ish vanilla HTML/CSS/JS, no
server. Not pass-and-play, not networked.

**Where the rules live:** the design doc's tutorial screen `8a` is the authoritative
ruleset — power ladder (Peek Allegiance, Foresight, Emergency Vote, Purge, Block at
five), win conditions, chaos behaviour. The doc states one power ladder for *all*
player counts, unlike the board game it descends from; the build follows the doc and
says so in the README. Deck composition (6 Reform / 11 Seize) was not specified and
was chosen.

**Import gotcha:** `DesignSync get_file` caps at 256 KiB, so the local copy of the
`.dc.html` is truncated mid-"Turn 3". The canonical screens (5a, 6a–6d, 7a–7d, 8a)
all landed intact — the loss is only the oldest exploration turns. If the tail is
ever needed, it cannot be fetched through that tool.

**Art pipeline:** the `ff14dda3-…` MCP *is* Higgsfield. `recraft_v4_1` is the useful
model here because it takes a `colors` palette (up to 10 hex) and `background_color`,
so generated art can be pinned to an existing design palette. Kenney CC0 packs supply
standees/icons, applied as CSS `mask-image` so the PNG gives the shape and the
stylesheet gives the design's colour.

**Higgsfield cost scar (2026-08-08):** 2K-resolution images cost several times the
1K rate — a 5-image batch (2×2K + 3×1K) consumed ~28 of 30 credits when I had
estimated ~6 ("~1.25/image"). Never quote a spend estimate without running
`get_cost:true` preflight first; `generate_image_batch` has no preflight, so probe
one representative config through `generate_image` before batching. Account was
left at ~1 credit. **Free alternative to `remove_background`:** generate props on a
flat `background_color: #22cc44` green screen and chroma-key locally with
PIL/numpy (mask g>r+38 & g>b+38, de-spill, crop to alpha bbox) — worked cleanly for
`assets/art/prop-noticeboard.webp` and `prop-haycart.webp`.

Related: [[css-var-url-resolves-against-stylesheet]],
[[grid-center-degrades-to-start-on-overflow]]
