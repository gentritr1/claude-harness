---
name: cloned-node-modules-carry-native-caches
description: "A `cp -cR` clone of node_modules for a worktree carries stale android/.cxx and android/build caches; the Gradle build then fails in ninja (missing libworklets.so)"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-08T00:45:11.994Z
---

2026-10-08 (art-4s, adding Skia in its own worktree): main's node_modules was APFS-cloned so that a dependency could be added without touching main. The first `npm run build:qa-apk` failed after 9 min: `ninja: error: .../react-native-worklets/android/build/intermediates/cmake/release/obj/arm64-v8a/libworklets.so ... missing and no known rule to make it`. The clone had copied 15 native cache dirs (node_modules/*/android/.cxx and android/build), configured for another tree.

**Why:** native build caches live inside node_modules packages, so a copied tree inherits ninja state that does not match its own build.

**How to apply:** after cloning node_modules into a worktree, delete every `node_modules/**/android/{.cxx,build}` and the worktree's android/app/build before the first native build. Use `rm -rf -- "${W:?}/${c:?}"`, because unguarded variable paths are refused by the safety check. A worktree whose node_modules is a symlink to main's (the usual setup) does not need this. Related: [[agent-worktree-isolation-cuts-from-main]].

**Correction 2026-10-09 (art-4cd):** deleting the caches is NOT enough. A fully fresh native build failed the same way: reanimated's ninja wants `react-native-worklets/android/build/intermediates/cmake/release/obj/arm64-v8a/libworklets.so`, but worklets now builds to `.../cxx/RelWithDebInfo/<hash>/obj/arm64-v8a/libworklets.so`. Fix: after the first (failing) build, `ln -f` the built .so into the cmake/release path, then rebuild (incremental). Main's tree works only because it carries that legacy path from an old build.
