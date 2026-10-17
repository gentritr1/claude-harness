---
name: metro-cannot-resolve-esm-js-specifiers
description: "Metro won't remap ESM ./x.js specifiers onto .ts/.tsx sources, so consuming merge-core as source needs a resolveRequest shim"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:08:54.762Z
---

`merge-core` and `merge-shell` are consumed as TypeScript **source** and use explicit ESM
specifiers (`import './math.js'`) — correct for `verbatimModuleSyntax` + `moduleResolution: Bundler`,
and fine for tsc and vitest. **Metro does not do that remapping**: it looks for `math.js`, then
`math.js.ts`, then fails with "None of these files exist".

**Why it matters:** the fix cannot go in the core — the core's specifiers are correct, and it was
frozen for v0.2 anyway. So the remap belongs in the app's `metro.config.js`: try the specifier as
written, fall back to the extensionless form.

**How to apply:** in `apps/*/metro.config.js`, wrap `config.resolver.resolveRequest` and retry
`moduleName.slice(0, -3)` for relative `.js` specifiers that fail. Any new app in this monorepo
needs the same shim (plus `watchFolders` = workspace root and `node-linker=hoisted` in `/.npmrc`,
since Metro and iOS autolinking cannot follow pnpm's symlinked store).

Verify with `npx expo export --platform ios` — it exercises the whole module graph in seconds and
is far faster than finding this in a native build.
