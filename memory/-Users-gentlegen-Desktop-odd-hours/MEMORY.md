# Odd Hours Gamehouse — memory index

- [PORT env collision](port-env-collision.md) — harness injects PORT; server must use ODD_PORT (8787)
- [Browser pane stale screenshots](browser-pane-stale-screenshots.md) — verify via read_page/JS, not screenshots
- [Parallel lane CSS collision](parallel-lane-css-collision.md) — file ownership ≠ namespace ownership; assign class prefixes
- [Flex-basis column leak](flex-basis-column-leak.md) — width basis becomes height when media query flips to column; fired 2×
- [Lane WIP lives in main checkout](lane-wip-lives-in-main-checkout.md) — worktrees can't see other lanes' uncommitted files; reconcile in the main checkout
