# Handgun v2 source

Generated using the built-in imagegen tool, with actual alpha transparency.
Source: `handgun-v2-sheet.png`, 1774x887, four columns by two rows.
Export with `python tools/split_shooting_test_frames.py`.

Prompt: Create a production photoreal first-person handgun animation sprite
atlas for a dark bunker videogame. Four equal columns by two equal rows,
eight separate square cells on transparent background. Same realistic adult
hands, black tactical jacket sleeves, and unbranded compact matte black
semiautomatic pistol throughout. Restrained red rim light and neutral key.
Reading order: two-handed idle aim; muzzle flash and recoil; settling;
reload starts with tilted pistol; magazine removed; magazine inserted;
slide racked; completed reload returning to idle. Consistent scale,
same sleeve baseline, no camera movement, labels, scenery, or grid lines.

The exported runtime images have a shared 444x444 canvas. Source pixels are
preserved during splitting; shorter cells receive transparent top padding.
The original user-provided sheet remains archived as `handgun-sheet.png`.
