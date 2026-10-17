---
name: parallel-agents-share-one-worktree
description: "A background agent's branch checkout moves MY branch too — commit by explicit path and push by ref, never reset"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-10T21:45:31.756Z
---

2026-08-10, running an ambience-code agent in parallel with my own Blender/asset lane: the agent created and checked out `ambience-weather` in the SAME working tree, so my next art commit silently landed on its branch instead of `main`, and `git push` failed with an autoSetupRemote error rather than anything that named the real cause.

**Why:** background agents are not isolated checkouts by default — one repo directory, one HEAD, one index. The agent's uncommitted files (`lighting.js`, `audio.js`, `main.js`, `package.json`, tests) were live in the tree at the same time.

**How to apply, when running a parallel agent in the same repo:**
- Always `git branch --show-current` immediately before committing; never assume HEAD is where you left it.
- Commit by **explicit path only** (`git add <paths>`), never `git add -A` — this is what kept the agent's in-progress files out of my commits, and vice versa.
- To land a stray commit on main, `git push origin <sha>:main` then `git branch -f main <sha>`. Both are non-destructive and touch neither HEAD nor the working tree.
- **Never** `git checkout`/`reset --hard` to fix branch confusion while an agent is mid-task — its uncommitted work is in that tree and would be destroyed.
- Better still: give a parallel agent `isolation: "worktree"` when its files might overlap, or hand it a strictly disjoint file set and say so (that part worked — see the ownership block pattern in the ambience brief).
