# Inspection bench, concept 01

Applied to every existing belongings screen: Chinba's delivery bag, Anu's school bag/notebook/rabbit, and Bayra's closed black bag. The single large central prop replaces the duplicate large preview. A left item tray, paper evidence tag, right information plate and five circular controls share the same layout.

The viewer remains a draggable **2D** illustration with zoom and in-plane rotation. This change does not invent a 3D backside or reveal Bayra's bag contents. Anu's supplied notebook drawing remains the existing `anu-notebook.webp` asset. Runtime text is rendered by Ren'Py, not baked into generated art.

## Asset provenance

Created with the built-in image generator using the author's approved first inspection mockup as reference (2026-10-22):

- `game/images/inspection/bench-v2.jpg`: clean empty rusty workbench, warm lamp upper left and red emergency light upper right. Source generated PNG converted to RGB JPEG, quality 94.
- `game/images/inspection/evidence-tag.webp`: blank horizontal aged ivory paper tag, clipped left corners, reinforced hole and short string. Source generated RGBA PNG converted to WebP, quality 95, alpha retained.
- `game/gui/shelter/inspection/*.svg`: original code-drawn simple icons, circular rim and soft shadow. Existing metal button frames are reused.

Background edit prompt:

> Use case: precise-object-edit. The supplied image is the approved design for a horror game's inspection screen. Produce the clean reusable background plate from this exact image in the SAME 16:9 framing, 1920x1080-style landscape. Preserve the hanging warm lamp at upper left, the photoreal rusty steel workbench, distant blurred bunker room and red emergency light at upper right, the color grading, perspective and gritty premium material detail. REMOVE the entire black bag including straps and its shadow; fill its former area naturally with the same uninterrupted empty workbench. REMOVE all interface elements: all title text, owner text, numbering, divider lines, the paper tag and string on lower left, the black information box on right including its lock icon, and ALL buttons, icons, labels, dark UI footer and horizontal divider. The bottom of the frame should be an uninterrupted dark steel bench front with subtle wear, no interface. Center tabletop must be uncluttered and ready for separate movable 2D props. Keep atmospheric peripheral bunker fixtures but don't add characters, hands, weapons or new props. Output one seamless full-screen background only, absolutely no text or UI, no bag or container, no paper.

Tag edit prompt:

> Use case: precise-object-edit. Extract/recreate ONLY the aged warm ivory paper evidence tag from the lower-left area of the reference, as a reusable transparent game UI asset. One large horizontal tag, width approximately three times its height, slight worn edges and restrained brown paper grain, left clipped corners and a dark reinforced punched hole near left edge, short dark string only on left. Make the tag face straight-on, perfectly horizontal, not angled. Delete ALL writing, rules and labels, leave generous clean pale paper across the center/right for dynamic readable text. Preserve the subtle realistic antique paper/material character seen in the reference. Center this ONE tag in the image with close transparent margins, high resolution, clean true alpha outside its edge and string, no colored background, no tabletop, no other objects, no typography, no watermarks. Soft minimal contact shadow close to tag edge only.

## Voice routing

`game/player_voices.rpy` maps supplied filenames to visitor IDs and individual choices. Subtitle windows use the audio decoder's clock; leading/trailing silence was measured with FFmpeg `silencedetect=noise=-32dB:d=0.10`. Playback still waits for audio EOF before starting the answer/action video. Original audio files are unchanged.

| Visitor | Supplied cues connected |
| --- | --- |
| Swat | Questions 1–3 and dedicated admission |
| anu | Questions 1–2; bag request on first inspection; separate drawing question only after opening the notebook |
| Chinba | Corrected question 2 subtitle window to 0.686–1.889 seconds |
| Existing visitors | Preserve dedicated recordings; missing rejection uses `audio/Chingune/MaralHuuh.wav`, missing admission uses `audio/Chingune/ChinbaOruulah.wav` |
| deeremchin survivor | Singular fallback for either surviving person; retain the dedicated plural rejection when both are present |

Audio-only IDs `baatra`, `hulan`, `tsermaa`, `tuguldur`, `undral` are registered for future encounters. No missing character/video/story was fabricated. Margad's three-part first question and Naraa's split second question use explicit cue keys in their branching encounter scripts; they are not blindly concatenated.

Anu's bag request is tracked independently of answered question 3. Closing/reopening inspection does not repeat that request or consume the drawing response. Starting a new run resets this state. Existing saved inspection progress is retained.

## Verification

Native Ren'Py 8.5.3 suites: `shelter_inspection_checks`, `shelter_player_voice_checks`, and the two-person survivor endings. The inspection cases cover selecting, zooming, dragging, reopening and save/load; the audio cases check the actual playing file and that player audio finishes before the response decoder starts. Native screenshots were reviewed for Chinba's bag/schedule, Anu's drawing and Bayra's closed bag. Windows/Android device testing is still separate.
