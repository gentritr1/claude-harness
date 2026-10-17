---
name: css-var-url-resolves-against-stylesheet
description: "A relative url() inside a CSS custom property resolves against the consuming stylesheet, not the document — broke every masked asset path in Secret Dictator."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9d90e3f0-7698-483d-a615-b31b363ed1c5
  modified: 2026-08-07T22:53:30.110Z
---

Declaring `--ico: url(assets/icons/x.png)` in an inline `style` attribute and then
consuming it via `mask-image: var(--ico)` inside `css/style.css` made the browser
request `/css/assets/icons/x.png`. The URL resolved against the **consuming
stylesheet**, not the document that declared it. Every Kenney mask 404'd while the
page still rendered, so it looked like a styling bug rather than a path bug.

**Why:** relative URLs in custom properties are resolved at substitution time
against the stylesheet where `var()` is used. Declaring the value in HTML does not
re-base it to the document.

**How to apply:** when a design system passes asset URLs through custom properties,
keep the stylesheet in the same directory as the document (Secret Dictator moved
`css/style.css` → `style.css` at the root, with a comment saying why). Otherwise use
root-relative paths. Detection rule: masked/background assets silently missing while
CSS otherwise applies → check the *resolved* request path in the network panel
before touching the CSS.

Related: [[grid-center-degrades-to-start-on-overflow]]
