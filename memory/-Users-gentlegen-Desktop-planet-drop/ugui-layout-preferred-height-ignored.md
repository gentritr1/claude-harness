---
name: ugui-layout-preferred-height-ignored
description: "UIKit.CreateVerticalGroup uses childControlHeight=false, so SetPreferredHeight (LayoutElement) is silently ignored — children lay out at their own sizeDelta (default 100)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ca4b8c-50e0-4c85-b08e-3d5ab5bedf39
---

`UIKit.CreateVerticalGroup` sets `childControlHeight = false` on the VerticalLayoutGroup. With control off, Unity's `HorizontalOrVerticalLayoutGroup.GetChildSizes` reads `child.sizeDelta[axis]` and **ignores LayoutElement min/preferred heights entirely**. So every `UIKit.SetPreferredHeight(button, …)` call across the screens does nothing — buttons actually render at the script-created RectTransform default height (100), not the UITheme heights (78/92).

**Why:** silent layout drift — panels are sized assuming theme heights but children occupy 100px each; anything taller than its rect (like a GridLayoutGroup child) overflows the panel without any error.

**How to apply:** when adding a child to a UIKit vertical/horizontal group, set the child's `sizeDelta` height explicitly (see HomeScreen play button / tile grid, 2026-07-02). A systemic fix (childControlHeight=true, or SetPreferredHeight also writing sizeDelta) changes the look of every shipped screen at once — do it only with visual verification in Unity. Related: [[unity6-urp-ui-gotchas]].
