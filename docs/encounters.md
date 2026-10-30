# Encounters

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

## Interactive belongings inspection

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
large buttons. The center viewer uses the original artwork, with in-plane rotation.
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
and handwritten “Түгжээ”. The original atlas artwork supplies the other enlarged
props and small inventory thumbnails.
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
in `shelter_next_visitor_card`. See the [in-game preview](../tools/previews/intermission.jpg).

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

## Rebuilding the updated encounter media

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
limits in `game/encounter_media.rpy`, preserves resolution, and records source/poster
hashes in `game/images/transitions/manifest.json`. Use `--check` to detect stale
or missing posters; add `--audit` to decode all video/audio streams completely.
The media workflow runs both conversion and poster extraction before committing.

## Playback handoff

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
