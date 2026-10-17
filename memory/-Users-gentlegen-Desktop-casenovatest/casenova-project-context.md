---
name: casenova-project-context
description: CaseNova (casenovapremium.live) redesign project — audit findings and prototype location
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a52912a-3b91-4a3f-b763-394d74765783
---

CaseNova sells premium iPhone cases in Kosovo (Albanian site, COD-only, free shipping, 1–2 day delivery). Live site: casenovapremium.live (React SPA, Supabase product images at yrpizozonpxcijqvgnpj.supabase.co/storage/v1/object/public/product-images/).

Redesign prototype built 2026-07-11: `casenova-prototype.html` in the project root (single self-contained file, dark+gold "Fraunces + Manrope" luxury direction). Key conversion moves: 2-step quick-order modal (model chips → 3-field COD form → success), always-visible Porosit CTAs on cards, compare-at prices, bundle −20% on 2nd case, camera-protector upsell (+3.99), live weekly countdown (auto-targets next Sunday 23:59), sticky mobile buy bar, WhatsApp order fallback.

2026-07-12 (later): DnD discoverability pass on v2 after user feedback — (1) tray cards equalized (`.dropzone` align-items:stretch + `.dz-name` 2-line clamp with min-height:34px); (2) **floating drop dock**: fixed bottom pill ("Lësho këtu — Bli 2, kurse 20%") that slides up on any `dragstart` and accepts drops anywhere on the page, so users never scroll mid-drag to reach the below-fold drop zone (hidden ≤760px); (3) one-time dismissible tip chip above the grid (`cn_tip_dnd` localStorage flag). Lesson: a below-the-fold drop target needs a drag-time fixed surrogate — remember this pattern for any future DnD landing sections. Gotcha re-confirmed: `position:fixed` elements break under the body-transform screenshot workaround (transformed ancestor becomes containing block) — reset the transform before screenshotting fixed UI.

2026-07-12: `casenova-product-v2.html` added — product detail page template (renders any product via `?p=0..24`, falls back to 0). Implemented by an Opus 4.8 subagent from a full brief (context/non-goals/observable criteria/verification method); reviewed by re-running every scenario in-browser — APPROVED, zero out-of-scope changes. Key pieces: visible model-chip grid replacing the live site's buggy dropdown, gated CTA, Sunday-skipping Albanian delivery-ETA computed from current date, shared `cn_cart` localStorage (cart added on PDP shows on main page), same-category related products, single-product order modal. v2 cards now link to it via media/name click with an `_dragged` flag suppressing navigation after drags. Delegation pattern worked: brief with exact acceptance criteria + reviewer re-runs = clean pass.

2026-07-12: V2 expanded to the FULL 25-product catalog scraped from the live site (real names, prices, compare-at pairs, and badge tiers — 8 Limited, 2 Premium, 1 Bestseller, 6 Ofertë). Every card is drag-and-drop enabled; filter chips show live counts (Dragonj 6, Flutura 3, Pasqyra 2, Art 12, Klasike 2); filtering animates via FLIP (surviving cards glide, newcomers scale in, disabled under prefers-reduced-motion). Real discounted items: Lëkure Deluxe 12.99/14.99, SlimFit 8.99/9.99, Dashuri Abstrakte 4.99/6.99, Ajri i Rrugës 6.99/7.99, Samurai+Kamere and Ujku i Natës 12.99/15.99. Scrape method: JS eval over `a[href^="/products/"]` anchors on /products, walking up 4 parents to find price text.

V2 originally built 2026-07-11 at user request: `casenova-prototype-v2.html` — fully working version adding: HTML5 drag-and-drop bundle builder (drop zone mirrors cart state; −20% auto-applies to 2nd-most-expensive unit via `bundleDiscount()`), working cart drawer with per-item model selects/qty/remove, localStorage persistence (`cn_cart` key), category filter chips (all/sale/dragon/butterfly/art), fly-to-cart ghost animation, action-toast stack, inline form validation with shake + error messages, gold confetti burst on order success, checkout gate that blocks until every cart line has an iPhone model. Modal has 3 modes: 'quick' (direct buy), 'cart' (step 1 adds to cart), 'checkout' (address-only for whole cart). All flows VERIFIED via real DragEvent dispatch + JS state checks; visuals VERIFIED via screenshots.

**Biggest live-site bug found:** product-page model dropdown displays "iPhone 15 Pro Max" as if pre-selected but the buy CTA stays gated on "Zgjidh modelin e telefonit" — users think a model is chosen. Also: dark hero → white body theme break, 4.0/5 shown with 5 full gold stars, no compare-at pricing, no quick-buy from cards.

**Why:** future iterations should keep the COD-market principles: minimum fields, no accounts, pay-on-delivery trust signals everywhere. See [[browser-pane-screenshot-freeze]] for how this was verified.
