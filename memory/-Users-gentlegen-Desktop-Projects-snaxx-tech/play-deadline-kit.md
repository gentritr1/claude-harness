---
name: play-deadline-kit
description: "Oct 2026 Play API 36 upgrade kit + Ignite Expo52→54 proof; repo paths, verified facts, owner apps already compliant, open owner decisions"
metadata:
  node_type: memory
  type: project
  originSessionId: 57d0f1a0-2955-4592-bd99-734d2ffb01f0
  modified: 2026-10-15T20:09:14.525Z
---

Built 2026-10-15. The kit lives in `~/Desktop/Projects/play-deadline-kit` (branch `kit-v0`; pushed 2026-10-15 to private https://github.com/SnaxxTech/play-deadline-kit with main, kit-v0, market-sizing). The proof fixture is `~/Desktop/Projects/pdk-fixture-ignite` (branch `upgrade/api-36`; private https://github.com/SnaxxTech/pdk-fixture-ignite, Ignite MIT LICENSE added).

**Contents**
- `pdk` CLI: zero-dependency Node. Checks source and artifact; the artifact is the authority.
- `scripts/device-check.sh`: all adb calls bounded; a wedged device gives ERROR.
- PLAYBOOK.md and VERIFY.md.
- OFFER-DRAFT.md: draft, not published.
- Evidence in `evidence/`.

**Final review:** Fable REQUEST CHANGES, then one fix wave, then a Fable re-review APPROVE. Suite 78/78 with real artifacts.

**Verified facts (2026-10-15)**
- Play requires API 36 for updates; the extension ends 2026-11-01.
- Apps at API 34 or lower lose discoverability.
- 16 KB is required for updates from 2027-02-01.
- Expo SDK 50–52 templates hard-code target 34. Expo 53 gives 35 (RN 0.79). Expo 54 / RN 0.81 gives 36.
- SDK 54 is the last Expo SDK with the Legacy Architecture.

**The owner's own apps already target 36 and are 16 KB-ready** (Arrows, Block Destroy, Rowflare, Geo Guesser). That's why the proof used Ignite. One audit RISK applies to all the games: portrait-locked without `android:appCategory="game"`, so Android 16 ignores the lock on tablets.

**Scars learned**
- `zipalign -P 16` passes 4 KB ELF libraries. Scan `p_align` instead (pdk or llvm-readelf).
- `react-native-mmkv` 2.x lacks `-DANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=ON`. The fix is a patch-package patch.
- `BackHandler.removeEventListener` was removed in RN 0.77.
- The emulator plus a Gradle build at the same time drove load to 66 and wedged adb.
- A tablet ANR under load was cleared by an identical rerun.

**Open owner decisions**
- PR kit-v0 → main not opened yet. market-sizing session hit its usage limit; its results are unreviewed.
- Publish the free checker as a lead magnet.
- Prices in OFFER-DRAFT ($300 / $1.5–3.5k / New Architecture from $2.5k; hours are UNVERIFIED).
- Run the market-sizing session's findings.
- Delete NDK 26.1 (3 GB). Disk was at 19 GB free.

Related: [[notes-mining-opportunity-map]]

**§7 learning lines**
- A tool "agreed with itself" on 16 KB, and zipalign passed a broken APK. Detection rule: every alignment claim needs an independent oracle (llvm-readelf) plus the device's own dialog. Future briefs: name two oracles for any binary-format check.
- A final review found the source checker contradicting artifact mode (BLOCKER despite an artifact at 36). Detection rule: test every combined-mode exit code against artifact-only on the same artifact. Future briefs: when the spec says "X is the authority", write a test that X overrides every other source.
- A review found PLAYBOOK VERIFIED tags that the code contradicted (severity words). Detection rule: a reviewer greps each documented severity or field against src. Future briefs: generate docs tables from code where possible.
