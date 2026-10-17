---
name: git-remote
description: FJALË GitHub remote and git workflow agreement
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a376e78-fea1-4e3f-b833-76f2dbc19ef6
---

Remote: `git@github.com:gentritr1/fjale.git`, branch `main` (user-provided 2026-07-16, push explicitly authorized).

**Production:** user deployed the repo to Vercel at `fjale-self.vercel.app` (seen 2026-07-16). Pushes to `main` auto-deploy — treat every push as production-visible; merge only reviewed work.

Workflow agreed with user: repo was initialized AFTER the first verified fix round (baseline = accepted state, with .gitignore). Every subsequent agent round lands as an atomic commit or branch; agents should work in git worktrees for isolation now that the repo exists. See [[daily-pool-immutability]] for what must never change in `src/words.js`.
