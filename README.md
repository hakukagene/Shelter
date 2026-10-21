# Shelter — Хорогдох байр

Ren'Py video encounter using the supplied `game/Video/Maral/*.webm` footage.

## Play

Open the project in Ren'Py Launcher and choose Launch Project. **Эхлэх** plays
the opening film, then starts the visitor sequence with Chinbaa.
The game uses a 1920×1080 logical canvas; the original
1672×940 footage fills the screen with near-identical aspect ratio.

## Android APK

The Android build uses Ren'Py **8.5.3** and produces a signed universal APK in
`dist/android/`. Copy the APK to an Android phone and open it to install.
If Android asks, allow installation from the app used to open that file.

The app is named **Хорогдох байр**, with package ID `mn.shelter.game`, version
`1.0`, and landscape orientation. It supports Android 5.0+ with OpenGL ES 3.0;
ARM64, ARMv7, and x86_64 libraries are included. Videos, fonts, and subtitles
are included in the APK; no separate media download is needed.

Rebuild from the project directory in PowerShell:

```powershell
.\tools\build_android.ps1
```

For a fresh toolchain, install the matching Android support in the Ren'Py
Launcher, then run `.\tools\build_android.ps1 -Setup`. This downloads a portable
JDK 21, installs Android SDK dependencies, and accepts their licenses.
Use `-RenpySdk 'C:\path\to\renpy-8.5.3-sdk'` for a different SDK location.
The local JDK and Gradle cache live under `.android-build/`.

Keep a backup of the root `android.keystore` and `bundle.keystore` files.
Future updates must use the same signing key and package ID. RAPT assigns
the build timestamp as the Android version code (or `numeric_version` from
`android.json`, if greater); update `version` for the displayed release number.
Keys, tool caches, tests, and previous packages are excluded from distributions
and Git.

The initial APK passed signature, ZIP integrity, and 16 KB alignment checks.
Start → intro → subtitles → skip → first visitor also passed in Ren'Py's
phone/touch emulation. Installation and playback on physical Android hardware
have not been tested.

## Safari / web

Play: https://shelter-khorogdoh-bair.upbeat-cedar-1751.chatgpt.site

Build the browser edition with `.\tools\build_web.ps1`. The finished static site
is in `dist/web/`, and the portable upload package is `dist/Shelter-1.0-web.zip`.
The script requires the matching Ren'Py web support and FFmpeg on `PATH`.
It caches MP4 conversions in `.web-build/`; changing a source video invalidates
that video's cached derivative.

The browser edition retains the Ren'Py story, menus, choices and save system.
`game/web_video.rpy` and `web/shelter-video.js` connect each clip to a persistent
inline HTML video element. H.264/AAC MP4s use fast-start metadata and load only
when needed. Each clip downloads into a seekable Blob because Sites' static
host does not return partial HTTP byte ranges. Skipping cancels a pending
download, and finishing releases that clip's Blob to bound memory usage.
Intro captions follow `video.currentTime`, stay on one line, and
use the same fonts and metal skip-button artwork as the game. Pause/resume,
muting, retry after a network error, Safari's tap-to-play prompt, and pausing
when switching tabs are handled by the browser player.

Play in landscape on an iPhone. If Safari requests a tap to start sound, press
**Тоглуулах**. A public web host must serve `.wasm` as `application/wasm` and
MP4 as `video/mp4`. Opening `index.html` as a local file is not
supported. For local testing, run `python tools/serve_web.py` and open the
printed URL on this computer.

Hosting is staged separately under `.web-site/` with Sites project ID
`appgprj_6ad758650d2c8191a32d3782a9f37e25`; preserve this identity on updates.
Only the built browser files are published. APKs, signing keys, tool caches,
test scripts and the source project's Git history are excluded.

Validation uses `node tools/web_browser_check.mjs` with
`python tools/serve_web.py --port 8044`. It runs an isolated headless Chrome profile with a phone-sized viewport
and touch events: Start, inline video, captions, pause/resume, skip, first
visitor, questions/player speech, aiming/lowering, and intro completion.
It also checks menu/gameplay/result music, the complete replacement door knock,
the next visitor and replay. `node tools/check_web_host.mjs <site-url>` checks
hosting headers and compares published game data, music and player hashes
against the verified local build.
All 40 MP4s were checked for codecs, fast-start and matching duration (maximum
change 0.008 seconds). Physical iPhone/Safari testing remains outstanding.

## Background music and speech

The start menu loops `game/audio/Audio/menu1.mp3`. The result screen with
**Дахин тоглох / Үндсэн цэс** loops `menu2.mp3`. Both use 50% track volume.
Gameplay loops `shuum.mp3` at 18% so speech remains audible. Starting or
replaying switches tracks with a fade; the opening film stops menu music.
The Music slider adjusts these backgrounds; Voice adjusts dialogue.

Visitor transitions play `ES_Doors, Knock, Metal Door, Knock With Fist - Epidemic Sound.mp3`
once on the sound-effects channel. The transition waits for the full 5.93-second
recording; this short effect is bundled in the web edition to avoid download delays.

The ten `game/audio/Chingune/*.wav` clips are matched to approximately
−16 LUFS with peaks limited to −1.5 dBTP. Original sample counts, sample rates,
and subtitle timing are preserved. Original files and the measurement report
are stored locally in `.audio-originals/`, excluded from builds and Git.
`python tools/normalize_voices.py` processes new/replaced clips and skips
unchanged files that have already been normalized.

## Opening film

- `game/intro.rpy` plays the 100-second opening on its own voice/movie channel.
  The existing metal control artwork is used for **Алгасах** at the upper right.
  Click it or press **Esc** to go straight to the first encounter. Normal clicks,
  Space, Tab, and rollback do not dismiss the film.
- `game/Video/Introvideo/Intro.webm` is the VP9/Opus playback copy of the supplied
  H.264/AAC `Intro.mp4`. Ren'Py desktop cannot decode the original codecs.
  Web builds generate an H.264/AAC MP4 copy from this playback asset.
- `game/Video/Introvideo/Intro.mn.srt` contains 40 editable Mongolian subtitle
  cues. Boundaries were aligned locally against the supplied text and audio,
  including the radio exchange. Small spelling corrections preserve the script.
  Timestamps are measured from the beginning of this specific video.
- Captions use the decoder position, so they stay with the video instead of
  accumulating timer drift. The voice volume control also controls the film;
  muting does not stop playback. Completing or skipping stops its audio before
  the encounter. Loading a gameplay save does not replay the opening.

To rebuild the playback asset after replacing the source:

```powershell
ffmpeg -i game/Video/Introvideo/Intro.mp4 -c:v libvpx-vp9 -crf 25 -b:v 0 -row-mt 1 -threads 8 -cpu-used 4 -pix_fmt yuv420p -c:a libopus -b:a 160k game/Video/Introvideo/Intro.webm
```

Re-align the SRT if the video's edit or narration timing changes.

## Encounter flow

1. Maral's introduction plays with Mongolian story text. Clicking does not skip it.
2. Three equal-width question cards appear horizontally across the bottom. No final decisions appear yet.
3. Choose a question; its matching answer video plays.
4. Decisions appear at the lower right: aim, reject, or admit. You may return to
   the remaining questions. Asked questions are marked and disabled.
5. Aiming plays its own clip, then offers shoot or lower the weapon. Lowering
   returns to the decision phase. Shooting plays the existing shooting clip.
6. The encounter ends with a replay/main-menu choice.

Rejection and admission play their new departure/admission videos before the
result screen. The game plays the supplied VP9/Opus WebM files directly from
`game/Video/Maral/`. Admission uses `Maral oruulah B huvilbar.webm`.
The supplied corrected idle image is used between neutral dialogue clips.
Chinbaa is not implemented because his video assets are not present.
Dialogue text follows the supplied story; it is not a word-timed transcription.

## Implementation

- `game/shelter.rpy`: stages, clip map, story text and UI.
- `game/script.rpy`: entry point.
- `game/images/stills`: first/last frames extracted from the original videos,
  providing startup and choice-screen images without looping spoken dialogue.
- `game/gui/shelter`: scalable outlined button backgrounds.
- `game/fonts`: Roboto Condensed regular/bold (Cyrillic extended), with OFL license.

Movie completion is detected on the dedicated `shelter_video` channel after a
short startup grace period. Menus and choices use real Ren'Py controls and text;
no generated mockup is baked into the game.

## Validation

The opening has native Ren'Py **8.5.3** tests in `game/intro_tests.rpy`:
Start → film, caption display, accidental-click/Space/Tab protection, metal
skip button, muted playback, Esc, restarting a new game, and full playback
through the first visitor's questions. Run them with isolated saves:

```text
renpy.exe <project-path> test shelter_intro_flow --savedir <project-path>/tmp/intro-saves --overwrite-screenshots
```

Tests write screenshots under `tmp/intro-tests` and close the test instance on
completion. The test scripts and `tmp/` are excluded from distributions.

Validated with Ren'Py 8.4.1 lint and two runtime tests, covering playback,
question gating, three answers, aim/lower/shoot, reject/admit, and replay.
These tests used Ren'Py 8.4's test language, which is incompatible with 8.5.3.
They are archived as `tests/renpy-8.4/shelter_tests.rpy.txt` outside the game
loader. Do not copy them into `game/` when using Ren'Py 8.5.x.
`game/shelter_tests.rpy` is an empty compatibility placeholder so pulling this
fix replaces previously compiled test code as well.

After updating, use Launcher → Force Recompile, then Launch Project. The main
game scripts are independent of the archived tests. Release builds should be
validated in the exact Ren'Py version used to ship them.
