---
name: shared-builder-leak-scar
description: "Editing a shared content builder for one app silently changed Arrows' policy; byte-diff the other app's rendered text before/after every time"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b62b1de2-f7a8-4456-9ed0-e02fe8e3cc49
  modified: 2026-07-27T21:19:09.941Z
---

Pattern → detection rule → brief/test update, recorded 2026-07-27.

**Pattern:** `buildPrivacy()` in `src/legal/content.ts` is shared by Arrows and Block Destroy. A one-line wording change requested for Block Destroy ("X is a general-audience app…") was written unconditionally and silently rewrote **Arrows'** Children's Privacy section too. Typecheck, lint, and build were all green — nothing catches it, because it is a legitimate string change.

**Detection rule that caught it:** capture the *other* app's rendered article text at HEAD, apply the change, re-render, and byte-compare. `git stash push <files>` → capture → `git stash pop` → capture → compare lengths and first differing index. Arrows' privacy article is 7150 chars; any delta is a leak. This has now caught one real regression on the first run and confirmed clean on three later runs.

**Why:** these are published legal documents for a different app. An unintended edit to Arrows' policy is a compliance change nobody asked for, and reading the diff would not reveal it — the diff looks like exactly the requested change.

**How to apply:** whenever a shared builder/template serving multiple apps is touched, gate the new text behind a profile flag (`generalAudience`, `rewardedAdsOnly`, `noBackend`, …) rather than editing the shared string, and prove the untouched app is byte-identical before committing. Never accept "the change was only for app X" from reading the code. See [[block-destroy-legal-2026-07-27]].
