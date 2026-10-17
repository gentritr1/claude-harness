---
name: codex-generated-images-path
description: "Where Codex's built-in image tool writes its PNGs, so the orchestrator can review a candidate before Codex copies it into the repo"
metadata: 
  node_type: memory
  type: reference
  originSessionId: df4dd4c1-38f3-4c2b-8e0b-c496f217dd8b
  modified: 2026-09-05T18:03:34.296Z
---

Codex's built-in image generator saves every output to
`~/.codex/generated_images/<session-id>/exec-<uuid>.png` (session id changes per Codex thread; list with `ls -t`).
Codex's own review JSON (e.g. `design/reviews/rubble-phase-1/cobble-source-profile.json`) records the absolute path and sha256 of the image it measured, so the exact file can be re-measured and eyeballed independently.

**Why:** On 2026-09-05 the accepted cobble tile existed only there for a while; the worktree held just the profiler output. Reviewing it early caught that the tile was 1254×1254, not the brief's 1024, before any Blender or runtime work depended on it.

**How to apply:** When Codex reports an accepted image, re-run the named instrument on the sha256-matching file and view it (plus a 2×2 tiled composite for seamless tiles) before approving. Related: [[rubble-square-art-pass]].
