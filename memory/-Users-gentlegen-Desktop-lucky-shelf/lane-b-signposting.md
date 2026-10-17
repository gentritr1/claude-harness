---
name: lane-b-signposting
description: "Lane B #5 build-signposting progress — the run-HUD build-identity panel is done (0e2e772); buildAccents tokens + remaining sub-items."
metadata: 
  node_type: memory
  type: project
  originSessionId: a55d034b-799c-4add-95d3-38f4c5c38f10
---

**Lane B #5 = make the loop-v2 depth legible ("I'm building a food shelf / this
signature changed my run / the target reward matters"), NOT new mechanics.** Sits on
the store view-model boundary ([[sim-ui-boundary-viewmodels]]).

**Slice 1 — run-HUD build-identity panel: DONE + device-approved, `0e2e772` (2026-07-08).**
Replaced the three interchangeable stacked pills (order/target/synergy) in [run.tsx](src/app/run.tsx)
with one `BuildSignpost`: hero = dominant-tag build (`🍷 DRINK SHELF`) + live ×mult + next-tier hint,
driven by a new `buildIdentityView` (tag/count/mult/active/next) in [store.ts](src/state/store.ts);
order + target demoted to compact full-width goal chips. **Active builds celebrated** (gold-tinted card +
big ember ×mult; muted parchment while still building). **Per-tag color accent** via a new tokenized
`buildAccents` map in [tokens.ts](src/ui/tokens.ts) (10 synergy tags → warm hues; reuse for signature
badges next). Verified on the iOS sim in BOTH active (×1.4 gold) and building (×1 neutral) states via the
seeded-HUD technique. Design was user-gated: shipped v1, user asked for 4 tweaks (celebrate active /
roomier chips / build accent / swap boxy 🎟️→🔁), applied all, re-screenshotted, approved.

**Slice 2 — signature-item badges in the shop: DONE + device-approved, `88e51c7` (2026-07-08).**
[restock.tsx](src/app/restock.tsx) daily-shop signature offers get a gold-framed row + thumbnail, a
`✦ SIGNATURE` badge, and a one-line effect blurb replacing their tag chips. The rule→English describer
`signatureBlurb(item)` lives in [store.ts](src/state/store.ts) (maps the 5 Phase-2c rule kinds to text,
null for non-signatures) so the screen never reads scoring internals. Verified: 5 blurbs scripted +
seeded restock shop screenshot (2 signature vs 1 normal offer). Default-off safe (engine only offers
signatures with SIGNATURE_ITEMS_ENABLED). Real signature sprites are still the #7 art pass (boxes are
placeholders now).

**Slice 3 — Daily Shop identity: DONE + device-approved, `4417089` (2026-07-08).** The v2 restock now
reads as a shop: mode-aware title ("Daily Shop" vs "Restock"), "TODAY'S STOCK" label, a
"Day N · Xc to spend · Y spots open" context line (buy-many rhythm), and a "Done Shopping" button — all
keyed off the `loopV2` snapshot via a `shopHeaderView(gameState)` VM in [store.ts](src/state/store.ts).
v1 mode keeps Restock wording, just gains the context line. Verified both modes on the sim.

**Slice 4 — supplier picker archetype cards: DONE `da63285` (2026-07-08).** [draft.tsx](src/app/draft.tsx)
build-steering picker: each supplier is a card with the tag emoji + name + accent-colored border
(`buildAccents`), previewing the build identity. Promoted the tag→emoji map to a shared `tagEmoji` token in
[tokens.ts](src/ui/tokens.ts) (fixed its coverage; run.tsx hero uses it too). Verified on the sim.

**Slice 5 — target-hit cascade celebration: DONE `8b66038` (2026-07-08).** When the daily target is met, a
gold "🎯 TARGET HIT · N/target · 🔁 Free reroll earned" banner springs in under the DAY TOTAL slam in
[CascadeLayer.tsx](src/juice/cascade/CascadeLayer.tsx). Threaded via `CascadeMount.targetResult` (from
`afterOpenShop.dailyTargetResult` in `cascadeMountAfterOpenShop`) → run.tsx → CascadeLayer. Verified via the
**cascade-harness** dev screen (`/cascade-harness` renders the real CascadeLayer with a fixture trace — the
easiest way to eyeball cascade UI headlessly: seed a `targetResult` prop + redirect to it).

**#5 signposting COMPLETE — all 5 slices done + device-approved.** Everything still behind the loop-v2
depth flags (default OFF), so nothing renders in the shipping default; still pending Fable + the wider
device feel-gate. Reusable design language established: `tagEmoji` + `buildAccents` tokens + gold
"active/celebrated" treatment (sunlight bg + goldDeep border + emberDark text), used by the build hero,
supplier picker, signature badges, and the target banner.
