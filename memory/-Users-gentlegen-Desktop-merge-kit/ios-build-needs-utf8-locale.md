---
name: ios-build-needs-utf8-locale
description: "On this Mac, pod install fails with Encoding::CompatibilityError unless LANG/LC_ALL are UTF-8; expo run:ios then fails with a misleading sandbox error"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:10:04.451Z
---

On this machine (rbenv Ruby 2.7.4, CocoaPods 1.16.2), `pod install` dies with:

```
Unicode Normalization not appropriate for ASCII-8BIT (Encoding::CompatibilityError)
```

CocoaPods warns about it at gem-install time ("requires your terminal to be using UTF-8 encoding")
and then the failure surfaces much later and misleadingly: `expo run:ios` reports
**"The sandbox is not in sync with the Podfile.lock"** and `xcodebuild` error 65, which looks like a
stale-pods problem rather than a locale problem.

Fix — prefix the command:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 pod install
```

Two related gotchas from the same build:

- `expo run:ios` needs port 8081 for Metro and refuses non-interactively if another project holds it
  (lucky-shelf's dev server did). Building `--configuration Release` sidesteps it entirely — a Release
  build bundles the JS and needs no dev server.
- Piping a background build through `| tail` makes the reported exit code `tail`'s, not the build's.
  A "completed exit 0" notification meant nothing; the log showed the real failure. Don't trust a
  piped exit status.
