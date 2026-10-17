---
name: rubble-scripts-write-into-review-folders
description: "Codex's rubble measurement scripts default their output into design/reviews/ evidence folders (often via env vars like WALK_OUTPUT, PAIR_OUTPUT), so a reviewer run in the shared worktree overwrites uncommitted evidence unless the output is redirected first"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df4dd4c1-38f3-4c2b-8e0b-c496f217dd8b
  modified: 2026-09-06T16:53:19.462Z
---

On 2026-09-06 my walk-comparison re-run overwrote Codex's untracked design/reviews/rubble-phase-2/env-facade-a/walk-* files because I rewrote the script's output path with a sed pattern that no longer matched (the path had become `process.env.WALK_OUTPUT || '...'`). Restored from Codex's checkpoint tarball (/private/tmp/rubble-facades-bc-review-<sha>.tar.gz), which is why those archives matter.

**Why:** the shared-worktree rule in project memory says commit by explicit path and never reset while another agent works; the same care applies to any file a script writes. Untracked evidence has no git safety net.

Update (phase 2, a5c6bda): Codex added `if(existsSync(out))throw Error('Output exists; refusing to overwrite evidence')` to the newer scripts (e.g. measure-rubble-kit-walk.mjs), so do NOT `mkdir -p` the output folder first; pass a path that does not exist yet.

**How to apply:** before running any scripts/*.mjs or *.py from Codex in /private/tmp/rubble-square-art, grep it for `const out=`, `writeFileSync`, `mkdirSync`, `process.env.*OUTPUT` and pass the documented env var (WALK_OUTPUT, PAIR_OUTPUT, REVIEW_URL, PAIR_ASSET, PAIR_REFERENCE) or a positional out dir pointing at the scratchpad. Verify with `grep -n "const out"` on the copy after any sed. Related: [[rubble-vite-ipv6-localhost]].
