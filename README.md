# Shelter — Хорогдох байр

Ren'Py 8.5 horror game: the player screens visitors at a bunker door through
full-screen video encounters and decides whether to admit, reject or shoot them.

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

## Project structure

| Path | Contents |
| --- | --- |
| `game/script.rpy` | Entry point: opening film, protocol, then the encounter loop. |
| `game/shelter.rpy` | Encounter flow labels (visit, questions, decisions, results). |
| `game/campaign.rpy` | Campaign totals, story clock and outcome bookkeeping. |
| `game/encounter_registry.rpy` | `shelter_register_visitor()` and the tables derived from it. |
| `game/encounter_media.rpy` | Movie/still lookup, clip trims and audio channels. |
| `game/encounter_screens.rpy` | Shared encounter screens, styles and hold-to-skip control. |
| `game/<visitor>.rpy` | One file per visitor: clips, dialogue, voices and registration. |
| `game/inspection.rpy`, `protocol.rpy`, `intermission.rpy`, `checkpoint.rpy`, `intro.rpy` | Bag inspection, rules dossier, ledger between visitors, midpoint save, opening film. |
| `game/web_video.rpy`, `web/` | HTML video bridge for the web build. |
| `game/shooting_*.rpy` | Shooting prototype (developer builds only). |
| `game/*_tests.rpy` | Ren'Py test suites, excluded from release builds. |
| `game/images/`, `game/gui/`, `game/fonts/` | Stills and posters, UI artwork, Roboto Condensed (OFL) and ledger fonts. |
| `tools/` | Media, art and build scripts; `tools/art/` holds asset provenance. |
| `docs/` | Detailed notes, listed below. |

Keep encounter **labels** in the file where they already live. Ren'Py saves
remember statements per file, so moving a label to another file breaks saves
made inside it. Screens and `init python` code can move freely.

## Adding a visitor

1. Put the footage in `game/Video/<visitor>/` and stills in `game/images/<visitor>/`
   (or extract transition frames with `tools/prepare_transition_frames.py`).
2. Create `game/<visitor>.rpy` with `define <VISITOR>_CLIPS`, `_QUESTIONS`,
   `_LINES` and `_SPEECH_WINDOWS`. Media tools parse these defines, so keep that
   naming and flat dictionary format.
3. Register it from the same file:

   ```renpy
   init 1 python:
       shelter_register_visitor("visitor", roster_position=11, civilian=True,
           clips=VISITOR_CLIPS, questions=VISITOR_QUESTIONS, lines=VISITOR_LINES,
           windows=VISITOR_SPEECH_WINDOWS, idle_still=("answer1", "start"))
   ```

   Monsters pass `civilian=False` and a `monster_ending`. Stills, subtitle
   placement, paused conversations and pair rules are optional registry fields;
   see the docstring in `game/encounter_registry.rpy`. Use the next unused
   `roster_position`; existing positions keep the order of older saves.
4. Add the visitor to `CONSTANTS` in `tools/prepare_transition_frames.py` and,
   if a bag can be inspected, to `SHELTER_INSPECTIONS` in `game/inspection.rpy`.

## Documentation

- [Encounters](docs/encounters.md): flow, inspection, ledger, media rebuilds, checkpoint and per-visitor notes.
- [Audio and opening film](docs/audio-and-intro.md)
- [Validation](docs/testing.md): lint and Ren'Py test suites.
- [Android APK](docs/android.md)
- [Safari / web](docs/web.md)
- [Shooting prototype](docs/shooting-prototype.md)
