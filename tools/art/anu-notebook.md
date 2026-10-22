# Anu's notebook drawing

Created with the built-in Imagegen tool using the imagegen skill, 2026-10-22.

- User-supplied drawing: `game/images/anu/zurag.jpg` (commit `7d01147639e386b7e51ab49d9d0893c16ae31f5f`).
- Prop/material reference: the open notebook at the bottom center of `game/images/inspection/items.png`.
- Runtime asset: `game/images/inspection/anu-notebook.webp`.
- Original generation: 1536 × 1024 RGBA PNG. Encoded as WebP at quality 95 without resizing; alpha preserved exactly.
- Runtime: the `drawing` sprite shown when Anu's notebook opens. Existing rotation, zoom, close/reopen and question behavior are preserved.

## Generation prompt

Use case: compositing. Asset type: transparent PNG game prop sprite, an OPEN worn notebook for the existing Ren'Py Shelter inventory inspection screen.

Input 1 is the EDIT TARGET / shape-and-material reference: extract ONLY the open black-covered notebook near the bottom center of the sheet. Do not include any other object from the atlas. Input 2 is the user's exact supplied DRAWING to integrate into that notebook.

Primary request: replace the old doodles and old rounded door illustration in the open notebook with the supplied drawing, blended naturally into its two facing pages. The entire wide drawing should span the open two-page spread at readable proportions, flowing naturally across a subtle central binding crease. Make this look drawn directly onto aged lined paper with the original black graphite strokes and dark red pencil marks, never a rectangular pasted photo. Match paper grain, warm aged cream tone, uneven worn page edges, gentle center-fold shadow and top-left lighting to the target notebook. Preserve the target black cover, thickness and realistic slightly top-down view; the book is fully in frame, centered, nearly horizontal, with only small transparent margins. The open spread can be slightly wider to fit the original artwork without squashing its geometry.

Preserve the supplied drawing faithfully: a large wide rectangular bunker door, four dark window panels with bars across the upper half, a round locking wheel centered beneath the windows, red lamp at upper left, right-side hinges, graphite crosshatching, red outlines, small childlike doodles around it, and the curved red arrow pointing to the wheel. Keep the handwritten Mongolian word exactly 'Түгжээ' beside that arrow. These are pencil drawings on paper, not a realistic door or glowing objects. Do not redesign the door. Do not carry over the source photo's spiral rings: this is the target's bound notebook. Remove all of the target's old drawing first; no ghost image, no additional second door.

Output ONLY this finished open notebook as one high-resolution cutout with true transparent background and clean soft alpha around its worn edges. No tabletop, no background wash, no other objects, no hands, no UI, no captions, no watermark. This should fit naturally into a dark, warm-lit horror-game inspection desk.
