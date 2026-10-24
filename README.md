# Shelter — Хорогдох байр

Ren'Py video encounter using the supplied `game/Video/Maral/*.webm` footage.

## Play

Open the project in Ren'Py Launcher and choose Launch Project. **Эхлэх** plays
the opening film, then starts the visitors in a random order.
The game uses a 1920×1080 logical canvas; the original
1672×940 footage fills the screen with near-identical aspect ratio.

## Desktop icon

The red-lit steel bunker door is the game's desktop icon. The transparent
256×256 `game/gui/window_icon.png` is used by the running game's window and
taskbar through the existing `config.window_icon` setting. Restart the game
after updating to see it.

The root `icon.ico` contains 16, 24, 32, 48, 64, 128, and 256 pixel versions
of the same artwork. Ren'Py embeds it in Windows executables when choosing
**Build Distributions**; rebuild an existing Windows release to update its
executable icon.

## Android APK

Android uses the author's supplied bunker-door `icon.ico` artwork through the
root `android-icon_foreground.png` (transparent 432×432) and
`android-icon_background.png` (opaque 432×432). The foreground is inset so
launcher masks can crop the surrounding background without cutting off the door.
Ren'Py generates the launcher icon sizes, including older non-adaptive icons.

The root `android-presplash.jpg` is the 1920×1080 **АЧААЛЖ БАЙНА...** startup
screen. RAPT displays it while the native app starts, before the main menu; it
does not add an artificial delay or replace the story intro. Its black border
fills extra space on wider/taller phones without stretching the artwork.
`android.json` already enables `update_icons` and `update_always`, so both icon
and startup art are picked up by the next build. Rebuild and install the updated
APK to see them; existing installed APKs do not update their bundled images.

The assets are ready to package without Python/Pillow on the build machine.
To regenerate them after editing the source art, use
`python tools/prepare_android_branding.py --presplash path/to/loading-art.png`.
Omit `--presplash` to regenerate just the icon layers. See
`tools/art/android-branding.md` for the image-generation prompt and provenance.

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

Visitor transitions play `game/audio/Audio/door .wav`
once on the sound-effects channel. The transition waits for the full 2.20-second
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

The playable roster is Chinba, Maral, Swat (Orgil), Bayra and Anu.
New games and **Дахин тоглох** shuffle all available visitors once, with no repeats.
The first visitor is random too. The order is saved with the game and stays fixed
when loading or rolling back. Older saves without a shuffled order continue their
original remaining sequence; starting again enables random order.
Each visitor has three questions plus an aim button. Asked dialogue questions are
disabled; the bag question stays available for repeat inspection. Aiming offers
shoot or lower. Unarmed players can admit or reject the visitor.
A black clock/count screen and metal door knock separate visitors.

Bayra's updated footage combines arrival with introduction, entry with admission,
and departure with rejection. These clips play once, without the old extra segments.
His three supplied question recordings play before their matching answers.
His idle pose uses the exact first frame of the corrected answer-1 playback clip;
the former 0.08s still was a blended frame that made his face appear doubled.

Anu follows the updated story's monster encounter. Rejecting or shooting her proceeds
to the next visitor without a civilian death (or ends the preview if she is last).
Admitting her loses the game.
Anu's supplied admission movie now plays in full: the door opens and she attacks,
then the monster-ending result appears. The still-image placeholder is no longer
used during new admissions.
Her player question voice recordings are also not supplied yet.

### Interactive belongings inspection

The third question opens a tabletop inspection for visitors with supplied bags:

| Visitor | Container and available objects | Story behavior |
| --- | --- | --- |
| Chinba | Yellow delivery backpack; meal, charger, delivery schedule | His answer plays once, then the contents can be inspected. |
| Anu | Pink school backpack; notebook, rabbit placed alongside it | Open the notebook to reveal the bunker-door drawing, then ask her about it to play answer 3. Closing early does not consume that answer. |
| Bayra | Closed black business bag | His refusal plays once. Only the outside can be inspected; no contents are invented. |

Maral has no supplied bag and Orgil says he lost his. Their questions stay unchanged.
Click an object to enlarge it; drag to rotate the **2D illustration**, use the
mouse wheel or +/− buttons to zoom, and use its action to inspect/read it.
Left/right arrow keys also rotate; =/− keys zoom. Touch users can tap the same
large buttons. This does not reveal a modeled 3D reverse side.
“Тавих” puts the selected item down; “ҮЗЛЭГ ДУУСГАХ” or Escape closes inspection.
Checked-item progress survives reopening and save/load, and resets for a new game.
Inspection does not change admissions, deaths, visitor counts, or classifications.

The new text-free workbench and transparent prop atlases are generated assets,
matched to the supplied character appearance and updated script. Their runtime
crop rectangles, per-visitor inventory, and interactions live in
`game/inspection.rpy`; extend its data tables when future visitors arrive.

Anu's open notebook uses `game/images/inspection/anu-notebook.webp`, a standalone
transparent prop made from the supplied `game/images/anu/zurag.jpg`. The drawing
is blended across the aged pages and center fold, including its red lock arrow
and handwritten “Түгжээ”. The closed notebook and other atlas objects are unchanged.
The source and generation prompt are documented in `tools/art/anu-notebook.md`.

The campaign counters retain 43 civilians, 30 monsters, a target of 40 rescued
civilians and at most two civilian mistakes (killing or rejecting). The third
mistake ends the run. Ten encounters containing eleven people are playable;
finishing them is a preview ending, not a campaign win.

Between visitors, `game/intermission.rpy` uses the selected guard's ledger artwork
with the **ХОРОГДОХ БАЙР** heading and three live totals: **Шалгасан хүн**,
**Оруулсан хүн**, and **Алсан хүн**. The last counts all fatal shootings, including
monsters, but excludes Orgil's nonlethal armor hit. The separate civilian rescue
and death-limit rules still govern campaign results.

The physical alarm clock starts at 23:10; the first completed visitor advances it
to 23:17, and later visitors add a random 4–9 minutes. The saved story time changes
only when a new outcome is recorded, remains stable through redraws and loading,
wraps correctly past midnight, and resets on replay. Older saves derive a stable
fallback time from their completed-visitor count until their next decision.
The original knock at 2 seconds and automatic transition at 8.1 seconds remain
in `shelter_next_visitor_card`. See the [in-game preview](tools/previews/intermission.jpg).

`game/gui/shelter/intermission/ledger.jpg` has blank number cells and clock glass;
the numbers are rendered by Ren'Py. The small clock font uses original geometric
seven-segment glyphs. The ledger numerals use a renamed DejaVu Serif subset with
its license in `game/fonts/DejaVu-LICENSE.txt`. Both can be rebuilt using fonttools
and `python tools/build_ledger_fonts.py /path/to/DejaVuSerif-Bold.ttf`.

Neutral waiting and armed frames are extracted from the corresponding videos.
Dialogue captions use measured speech windows on the video decoder clock.

Playback now holds its decoded last frame at EOF, then uses the matching end
poster before returning to a stable waiting pose. Conversational clips blend
back over 0.18 seconds; final actions keep their own last frame until the clock
or result transition. Maral's rejection/shooting no longer flashes the lockdown
ending artwork. All 97 logical encounter clips have individual start/end posters.
The supplied Bayra aim clip's trailing black frame is excluded at 13.11 seconds
in both native playback and web MP4 conversion; speech has already finished.
Maral's third-answer caption now follows the updated recording through 7.332s.
The browser bridge uncovers Ren'Py only after its replacement canvas is painted.

### Rebuilding the updated encounter media

The source-to-playback map is `tools/encounter_media.json`. With FFmpeg, Python
and Git LFS installed, run from the repository root:

```text
git lfs pull
python tools/prepare_encounter_media.py
python tools/prepare_transition_frames.py --audit
```

This builds Bayra and Anu VP9/Opus WebMs and stable JPEG frames, preserving source
resolution and audio. Commit the derivatives through Git LFS before pushing.
The **Build encounter playback media** GitHub Actions workflow builds and commits
media when Bayra/Anu source MP4s or the converter/manifest change. It can also be
run manually through Actions on a selected branch. Removed MP4s are supported:
the converter preserves their existing WebMs, and extracts stills from the actual
playback files. Hashes in `game/images/encounter-media-manifest.json` prevent
unchanged clips/stills from being rebuilt. Keep the WebMs when retiring originals.

After replacing any playable WebM, regenerate the transition posters with
`tools/prepare_transition_frames.py`. It reads the live clip tables and playback
limits in `game/shelter.rpy`, preserves resolution, and records source/poster
hashes in `game/images/transitions/manifest.json`. Use `--check` to detect stale
or missing posters; add `--audit` to decode all video/audio streams completely.
The media workflow runs both conversion and poster extraction before committing.

## Implementation

- `game/shelter.rpy`: stages, clip map, story text and UI.
- `game/inspection.rpy`: interactive belongings and saved inspection progress.
- `game/script.rpy`: entry point.
- `game/images/<visitor>/frames`: stills extracted from the original videos,
  providing startup and choice-screen images without looping spoken dialogue.
- `game/gui/shelter`: scalable outlined button backgrounds.
- `game/fonts`: Roboto Condensed regular/bold (Cyrillic extended), with OFL license.

Movie completion is detected on the dedicated `shelter_video` channel after a
short startup grace period. Menus and choices use real Ren'Py controls and text;
no generated mockup is baked into the game.

Encounter playback keeps an opaque poster on the master layer as well as under
the movie. The decoded end poster stays visible through the waiting-pose handoff,
including when resuming an older save. Departures dissolve straight to the ledger;
its live clock and counters remain behind the card until the next visitor starts.
This prevents transient screen removal or decoder startup from exposing black.
Question/action buttons retain the current still before returning their choice.
The first-frame poster finishes its dissolve before native movie playback starts;
no live Movie is rendered inside that startup transition. Window hiding during
questions and inspections also avoids an unrelated dialogue-window transition.
The web overlay remains transparent while downloading or awaiting autoplay and
reveals the video only after its first frame reaches the compositor (with a
loaded-data/paint fallback for older browsers).

## Validation

Full transition and sequence checks (normal playback, about 12 minutes):

```text
python tools/prepare_transition_frames.py --check --audit
renpy.exe <project-path> test shelter_transition_checks --savedir <project-path>/tmp/transition-saves --overwrite-screenshots
node tools/test_video_bridge.mjs
```

For the black-flash regression alone, run:

```text
renpy.exe <project-path> test shelter_transition_checks::no_black_transition_frames --savedir <project-path>/tmp/transition-saves
renpy.exe <project-path> test shelter_transition_checks::no_black_after_button_clicks --savedir <project-path>/tmp/transition-saves
```

It samples rendered pixels through an old-save-style still, two movies, Maral's
departure, the ledger and Chinba's arrival, and rejects black frames in that
sequence. This test uses the real decoder and normal playback speed.
The button case clicks a question, aim, lower and reject from an old-save-style
screen, capturing the player-voice and video-start intervals as well.

The native suite plays all 45 clips to EOF, then rejects all five visitors in their
shuffled order, opening Anu's notebook and playing her answer wherever she appears.
It verifies no duplicates or missing visitors, question/clock save-load recovery,
replay reset, legacy-save progression and seeded coverage of every first/last visitor.
To run only the order checks without replaying all 45 movies:

```text
renpy.exe <project-path> test shelter_transition_checks::random_roster_and_legacy_saves --savedir <project-path>/tmp/order-saves
renpy.exe <project-path> test shelter_transition_checks::actual_campaign_reaches_anu --savedir <project-path>/tmp/order-saves
renpy.exe <project-path> test shelter_transition_checks::ledger_clock_and_totals --savedir <project-path>/tmp/ledger-saves
```

The bridge test covers first-frame reveal, slow downloads, autoplay permission,
old-browser fallback, EOF holding, deferred canvas handoff, stale callbacks,
trimmed playback and intro skipping.
The Node bridge test uses a simulated DOM; it is not physical Safari validation.

Inspection regression scenarios (Ren'Py 8.5.3):

```text
renpy.exe <project-path> test shelter_inspection_checks --savedir <project-path>/tmp/inspection-saves --overwrite-screenshots
```

They cover all three bag-question paths, item actions, actual mouse dragging,
zoom, save/load, reopening without repeated audio, Anu's drawing/answer gating,
Bayra's refusal, and unchanged encounter counters. Screenshots go to
`tmp/inspection-tests`; test scripts are excluded from distributions.

Bayra/Anu regression scenarios are in `game/encounter_tests.rpy` (Ren'Py 8.5):

```text
renpy.exe <project-path> test shelter_updated_encounters --savedir <project-path>/tmp/encounter-saves
```

They cover Bayra's question voices/answers and aim/lower, reject/admit transitions
to Anu, Anu's three answers and aim/lower/shoot, and her admission loss/counters.


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

## Protocol and midpoint continuation

The approved classified-dossier instructions appear after the intro (including
when it is skipped). A document icon at the top right opens them again during
questions, inspection and response videos. Opening the guide pauses the current
voice/video; closing it resumes the same position, including the HTML player.

The main menu shows **Үргэлжлүүлэх** only when the dedicated
`shelter-midpoint-v1` save exists with valid checkpoint metadata. After rescuing
the twentieth civilian, the game saves once per run at a stable interaction
between visitors. Continue restores the saved random order, outcomes, counters,
clock and inspection progress, then proceeds to the next visitor. Newer manual
saves do not replace this destination. A new game keeps the old checkpoint until
its own twentieth rescue replaces it.

Only seven civilians are currently supplied (including the man in the pair), so
the current content preview cannot naturally reach twenty. The checkpoint is
implemented and integration-tested with a nineteen-rescue fixture; production
does not repeat or fabricate visitors to unlock it.

Ganbaa is the seventh encounter: all nine supplied clips, questions, civilian
classification, bag inspection, aiming/lowering and three endings are connected.
See `tools/art/protocol-and-ganba.md` for asset provenance and validation.

Ganzorig (`ganzo`), 43, is a civilian from the latest author DOCX. New runs
include him in the shuffled roster. His nine supplied VP9/Opus clips retain
their original framing and sound; questions use the three existing `audio/ganzo`
recordings and decisions reuse the existing admit/reject voices. Waiting poses
come from the actual video frames, with start/end posters for every clip to
cover decoder handoffs. No carried bag is specified for this character.
Existing saves with a stored roster keep that roster. Native flow checks are in
`game/ganzo_tests.rpy` (excluded from release builds).

Naraa is a civilian in the shuffled roster. Her ten supplied clips now use 20
exact first/last video frames during decoder handoffs. The separate `Nara ok.jpg`
and stand-off artwork are no longer inserted between clips, preventing the brief
wrong-frame flash while preserving the supplied footage and sound unchanged.

Margad, 18, is the third monster in the author DOCX. His nine supplied WebMs
are connected as eleven logical clips, including three exact ranges from the
first-answer movie so the player's three recordings alternate with Margad's
responses. Native and web playback share the same source-time ranges and 22
transition posters. His dedicated `ChotgorHuuh.webm` now plays in full when
the player rejects him.

Encounter dialogue has a bottom-right hold-to-skip control on native and web
builds. It must be held continuously for one second; releasing early resets the
progress so an accidental tap cannot skip player audio or character video.

Margad's first question now stays on one continuous response movie. After the
first selected question, the movie pauses at two conversation points and shows
the next player line as a centered button. Selecting it plays the matching
player recording, then resumes the same movie decoder on native and web builds.
