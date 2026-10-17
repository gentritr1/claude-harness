---
name: android-package-is-frozen
description: The Android applicationId com.snaxxtech.geoguesser must never change — a rename strands the existing Play closed test
metadata:
  type: project
---

The Play listing and closed-testing track are bound to `com.snaxxtech.geoguesser`.
An applicationId cannot be changed after publishing, so any rename creates a
brand-new app with a new listing and testers re-invited from zero.

On 2026-08-28 `origin/main` HEAD (`a727de7`, by danteberishaj) renamed it to
`com.geo_guesser_world_rd.myapp` as a self-declared non-compiling WIP. No
rationale is recorded anywhere in the repo, `LEGAL-HANDOFF.md` still documents
the old package, and the change was originally written when versionCode was 3
(2026-07-25) — before the 1.2.2 (7) closed-test release. Gentrit confirmed on
2026-08-28: keep the package as it was, bump version numbers only.

**Why:** the rename is an unexplained, unfinished change that would silently
destroy the closed-testing track it gets shipped into.

**How to apply:** when merging main, resolve `app.json` to
`com.snaxxtech.geoguesser` and delete any `com/geo_guesser_world_rd/` sources —
they collide with the gradle `namespace` and fail with "Unresolved reference:
R / BuildConfig". Only revisit if Dante produces an actual second Play listing.
See [[geoguesser-release-build-steps]].
