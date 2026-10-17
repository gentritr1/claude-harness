---
name: audio-system
description: "How music/SFX are wired in Lucky Shelf — gateway, prefs, per-screen beds, and how to verify audio on web."
metadata: 
  node_type: memory
  type: project
  originSessionId: 20ac0a0c-8bf3-4a85-8236-545a804b58ac
---

Audio landed 2026-07-07. Source mp3s came from `~/Desktop/lucky-shelf-music/` (Suno), copied to `assets/audio/{title,main,rent-week,cascade}.mp3`.

**Architecture** — `src/juice/audio.ts` is the single audio gateway (mirrors `haptics.ts`): screens NEVER touch expo-audio directly. Exports `setMusicTrack(track|null)`, `primeAudio()`, `playCascadeSting()`. Long-lived players via `createAudioPlayer` (not the hooks), lazily created, crossfaded (650ms linear volume ramp on a 40ms interval). Two prefs in `src/ui/prefs.ts`: `musicEnabled` + `sfxEnabled` (both default true); the gateway `usePrefs.subscribe`s so toggling Music live pauses/resumes. Settings SOUND panel wired with the shared `Row`/`Toggle` pattern; settings screen made a `ScrollView` (3 panels now).

**Per-screen beds** (via `useFocusEffect`): index→`title`, draft→`main`, restock→`main`, run→`main` unless `rent.dueInDays <= 1` then `rentWeek` (RENT_PERIOD_DAYS=3, so tension = final morning before rent, matching the DuskAmbience ember). Cascade sting fires in run.tsx `onPrimaryAction` right when `setCascadeMount` runs. `playsInSilentMode:true` is a deliberate choice (music-forward cozy game + in-app mute).

**Autoplay**: first `play()` is gesture-gated (web + iOS). Title buttons call `primeAudio()`; every screen re-asserts its bed on focus, so the bed starts by the first tap at latest.

**Verifying audio on web** (extends [[lane-b-web-verification]]): you CANNOT prove audibility on web — autoplay policy blocks playback for *synthetic* clicks too. What IS provable: (1) network shows `assets/audio/<track>.mp3 → 206 Partial Content` when a bed's player is created (proves require() bundled + track selected); (2) monkeypatch `HTMLMediaElement.prototype.play` to log `currentSrc` → confirms the gateway calls play() on the right source in the right order. expo-audio web uses a **detached** media element (not in DOM) + a module `activePlayers` Set, so `document.querySelectorAll('audio')` finds nothing. OPEN GAP: actual audibility, crossfade feel, and mix levels (MUSIC_VOLUME 0.55 / STING 0.85) are device-only — needs a real-device pass, ideally folded into the fun-gate recording.
