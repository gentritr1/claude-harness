---
name: monetization-kosovo-constraint
description: "Kosovo payout constraints drive Planet Drop's ad/IAP SDK choices — AdMob is banned, LevelPlay is the ad stack"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6539bd1a-7772-4fc8-b91c-0e14e2366a49
---

Planet Drop's developer is based in Kosovo, which gates the monetization SDK stack (decided Post-MVP Task #2, 2026-06-20):

- **Google AdMob / AdSense is UNUSABLE** — Kosovo is not a supported country for AdMob/AdSense *signup* (not just payouts; the account can't be created). Do not propose AdMob for ads, ever, unless Google re-enables Kosovo.
- **Ad SDK is Unity LevelPlay** (mediation), run WITHOUT the AdMob adapter in the waterfall (ironSource + AppLovin + Unity Ads + Vungle etc.). Pays via **Tipalti → Payoneer → local Kosovo bank** (ProCredit/TEB). Caveats accepted: Net 60 terms; public reports of delayed LevelPlay payouts. AppLovin MAX was the runner-up if LevelPlay payout reliability becomes a problem.
- **IAP payout is a SEPARATE, still-unverified gate:** IAP money flows through Google Play's merchant/seller payout (not LevelPlay). Google Play merchant registration has historically been restricted for Kosovo. The IAP adapter chunks (D/E) are blocked until the user confirms a paid Google Play merchant account is available from Kosovo (or uses a company entity in a supported country).

See [[planet-drop-orchestrator-workflow]]. The async IIapService rework (Task #2 Chunk A) is SDK-agnostic and stands regardless of which ad network ships.
