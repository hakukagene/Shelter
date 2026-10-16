# Shelter — Хорогдох байр

Ren'Py video encounter using the original `game/Video/Maral/*.webm` footage.

## Play

Open the project in Ren'Py Launcher and choose Launch Project. New Game starts
Maral's encounter. The game uses a 1920×1080 logical canvas; the original
1672×940 footage fills the screen with near-identical aspect ratio.

## Encounter flow

1. Maral's introduction plays with Mongolian story text. Clicking does not skip it.
2. Questions appear at the lower left. No final decisions appear yet.
3. Choose a question; its matching answer video plays.
4. Decisions appear at the lower right: aim, reject, or admit. You may return to
   the remaining questions. Asked questions are marked and disabled.
5. Aiming plays its own clip, then offers shoot or lower the weapon. Lowering
   returns to the decision phase. Shooting plays the existing shooting clip.
6. The encounter ends with a replay/main-menu choice.

Rejection and admission currently have **text-only outcomes** based on the
supplied story: the repository has no corresponding departure/admission/attack
clips. Chinbaa is not implemented because his video assets are not present.
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
