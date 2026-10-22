# Civilian ledger update

The three live rows are checked people, expelled civilians, and civilians killed
by the player. Monster outcomes do not contribute to the latter two. Expelled
civilians are derived from saved outcomes, including armored Orgil leaving after
a nonlethal shot and the civilian man lost when both Deeremchin visitors are
expelled. The existing combined-mistake rule is unchanged.

Digits use 92px (70% of the former 132px, rounded to a pixel), no synthetic italic,
and a -4 degree baseline. Their centers progress down the notebook's sloped
column: (1260, 444), (1284, 622), (1308, 804), in the 1920x1080 game canvas.
Labels use a renamed DejaVu Serif subset under the existing DejaVu license;
`tools/build_ledger_fonts.py` accepts its regular font as the second argument.

## Background edit

- Method: built-in ImageGen, precise-object-edit.
- Edit target: the existing `game/gui/shelter/intermission/ledger.jpg`.
- User reference: `image(20261022-123556).png`, showing the same ledger in game.
- Output: `game/gui/shelter/intermission/ledger.jpg`, converted to JPEG quality 94.
- Native screenshot: `tools/previews/civilian-ledger.jpg`.

Prompt:

> Use case: precise-object-edit. Asset: existing horror game ledger background,
> exact 16:9 composition. Edit target is the attached ledger image. Remove ONLY
> the three row labels inside the notebook: 'Шалгасан хүн', 'Оруулсан хүн', and
> 'Алсан хүн'. Seamlessly reconstruct the worn amber paper texture in those letter
> areas. Leave the three table rows and all dividing lines fully intact and in
> exactly the same positions. Preserve the heading 'ХОРОГДОХ БАЙР' exactly, the
> empty digital clock face, notebook outline, camera perspective and tilt, lamp,
> pen, cup, radio, light and shadows, colors and all other details. Keep the right
> numeric cells blank. No added text, no numbers, no design changes, no cropping
> or reframing. Output a clean blank-row plate, matching the input 16:9 aspect ratio.

## Verification

The native ledger clock/save-load test exercises civilian rejection, monster
shooting and rejection, civilian admission, Orgil's nonlethal departure, civilian
killing, pair rejection, and repeated outcomes. A native screenshot verifies the
labels and perspective. Original media and encounter transitions are unchanged.
