---
name: native-mode-setters-have-global-side-effects
description: "expo-audio 1.1.1 setAudioModeAsync forces MODE_NORMAL + speakerphone on Android on every call; a \"harmless\" per-foreground setMode could move a live call to the speaker"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-06T19:45:52.926Z
---

E4-2 review, 2026-10-06. The adapter called `setAudioModeAsync` on every warm, which happens on every return to the
foreground, even with no sound files bundled. In expo-audio 1.1.1 on Android, each call runs
`updatePlaySoundThroughEarpiece(false)`, which sets `audioManager.mode = MODE_NORMAL` and calls `setSpeakerphoneOn(true)`
(AudioModule.kt:186, 607-608). On Android 7-11 those settings are global, so the app could move a phone or VoIP call
in progress to the speaker.

The controller's own step-4 reading had cited exactly those lines, but only as the reason MODIFY_AUDIO_SETTINGS stays.
It never asked what the calls DO to the device. Every headless gate, the fake port and the aapt2 audit stayed green.

**Why:** a fake port records that a call happened, not what the call changes on the device. A setter that touches
global OS state is a player-facing bug that no headless check can see.

**How to apply:**
- For every native "mode", "session" or "config" setter, read what it writes to the OS (AudioManager, routing, focus,
  wake locks), not only whether its permission is needed.
- Call such setters once per process, and never when there is nothing to play.
- Add a device protocol that compares OS state before and after (`adb shell dumpsys audio`) during a call and with
  headphones.
- When citing a library line to justify keeping a permission, write down that line's side effect next to it.

Related: [[every-gate-we-write-ships-a-silent-pass]], [[unreachable-usually-means-untested]].
