---
name: review-scar-promised-discount
description: "Executor's builder promised a −5% set discount that checkout silently dropped; detection rule for promised-value carry-through"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0157fad9-ce3b-44e7-ad02-c9c9f0325873
---

Pattern: the table-builder UI promised "Kurse X € (−5%)" but cart/checkout charged full price — the executor's own report verified each view in isolation (builder total ✓, checkout total ✓) and missed that the two disagreed. Also found a 1-cent rounding mismatch between builder and cart once the discount was carried (fixed by rounding the saving once, identically in both).

**Why:** per-view verification passes while the cross-view invariant (money promised = money charged) fails — exactly the kind of trust-breaking bug a premium-brand prototype cannot have.
**How to apply:** when reviewing any flow that PROMISES a number in one view and CHARGES it in another (discounts, shipping thresholds, per-person prices), verify the same scenario end-to-end and diff the numbers across views; add "promised value survives to the final invoice, to the cent" as an explicit acceptance criterion in briefs. Related: [[browser-pane-verification-scars]], [[kik-home-project-state]].
