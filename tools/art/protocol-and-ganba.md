# Protocol screen, checkpoint and Ganbaa

## Behavior

The approved classified-dossier screen appears after the opening film, including after Skip. A top-right document icon opens it over decisions, inspection, player speech and response videos. Native channels pause with their previous pause state restored on close. The HTML bridge hides the paused video overlay while Ren’Py shows the guide, then resumes the same decoder/time. The guide does not dismiss the underlying decision.

Main-menu Continue is conditional on a loadable dedicated `shelter-midpoint-v1` slot with checkpoint metadata. It never selects the latest manual/auto save. The twentieth civilian rescue saves once per run, after the visitor resolves and before the next arrival. The save retains the already-completed outcome, random roster, clock, counters, inspected clues and once-per-run flags. Loading resumes the transition to the next visitor without the opening film, briefing or completed encounter. A new run keeps the previous valid checkpoint until reaching its own twentieth rescue.

The reference’s rules now apply: rescue 40 civilians; any admitted monster loses; at most two civilian mistakes, with the third fatal. Mistakes combine fatal civilian shots and civilian rejections. Orgil’s nonlethal shot still sends a civilian away and counts as a mistake; his death counter stays zero. Rejecting the pair counts the man as a lost civilian, not a player kill. Existing saves derive rejection counts from their recorded outcomes.

Current authored content has seven encounters/eight people, including five civilians. It cannot naturally unlock twenty yet. Tests seed nineteen earlier rescues to exercise the actual twentieth admission, native save and main-menu reload; no fake or repeated visitors are added to production.

## Ganbaa

All nine supplied `game/Video/ganba/*.webm` files are connected without re-encoding. He is a civilian and is shuffled with existing encounters. Questions use the supplied `audio/ganba` recordings; missing admit/reject lines use the existing shared recordings. The third response opens the common inspection UI with his actual plastic bag and three bottles. The question waiting frame is extracted from the start of answer 1; armed waiting uses the end of aim. All first/last transition posters are generated from the actual decoder frames, preserving no-black handoffs.

Story text comes from the updated author DOCX `Хорогдох байр(1).docx`. Question 3’s script describes a visual reveal, so no invented spoken caption is added over that clip. Speech windows follow the source audio clock. All nine sources were fully decoded and scanned for black sections.

The author’s door-knock change used `door.wav`, while the supplied filename is `door .wav`. The path now matches the actual file, and the between-visitor interval accommodates its 2.202-second duration.

## Art provenance

Built-in imagegen, 2026-10-22. Source reference: the attached `Shelter_ Classified Bunker Protocol.png`. Output: `game/gui/shelter/protocol/dossier.jpg` (RGB JPEG quality 94), with live Mongolian text and a real button in `game/protocol.rpy`. The original reference is not modified.

Prompt:

> Use case: precise-object-edit. Asset type: reusable background plate for a 1920x1080 Ren'Py horror game's instructions screen. Edit the supplied approved design with extremely high fidelity. Preserve EXACT framing and layout: dark bunker tabletop, SHELTER logo at top, red lamp upper right, worn large paper dossier, paperclips, black-and-white photo on the right, red НУУЦ stamp, small English microprinting, circular defense seal and all peripheral objects. REMOVE ONLY the main Mongolian title 'ХОРОГДОХ БАЙРНЫ ПРОТОКОЛ', the five Mongolian instruction paragraphs to the right of the numbered icons, the writing inside the upper red title strip, the writing to the right of the warning triangle in the lower red warning strip, and ALL text and the arrow INSIDE the red bottom button. Fill removed text naturally with same paper/red surfaces. KEEP the numbered 01–05 blocks, their five icons, horizontal row separators, warning triangle, red button border/rivets and red empty button surface. Do not move or resize anything. Keep paper texture light and quiet where live text will be overlaid. Do not add any new text. Output a single full-width 16:9 background image, opaque, no mockup border or device.

Ganbaa reference: author-supplied `game/images/ganba/Snowbound Industrial Standoff.png`. Output: `game/images/inspection/ganba-bag.webp` (WebP quality 94, preserved alpha). This is a 2D prop, not a modeled 3D backside. `rules.svg` is an original code-drawn icon matching existing UI icons.

Prompt:

> Use case: background-extraction. Asset type: transparent game inspection prop. Extract/recreate ONLY the translucent thin plastic shopping bag containing the three liquor bottles held at the LEFT side of the supplied reference image. Preserve their specific shapes and appearance: two amber/brown liquor bottles with dark/cream rectangular labels and one clear pale bottle between them, black caps, loosely stretched translucent plastic bag handles. Show the COMPLETE bag and the entire bottles upright, plausible lower ends reconstructed where obscured by the door frame, as one isolated prop ready to place on a workbench. Keep photographic material detail and subtle warm highlights but enough neutral lighting to see bottle glass. Remove the man's hand, ALL person/body/clothing, bars, gun, door, background, table and text. NO extra items or extra bottles. One prop, centered, generous transparent margin on every edge, true alpha background, no floor or cast shadow. Match the reference rather than inventing a different shopping bag. High-resolution game cutout.

## Verification

Ren’Py 8.5.3 native tests cover intro/briefing order, clickable guide, movie/player-voice pause and resume, hidden Continue below twenty despite a manual save, actual twentieth admission/checkpoint, reload past completed visitors, combined mistake boundary, all Ganbaa choices and all nine playback clips. Native rendered screenshots were reviewed for the instructions, checkpoint menu, armed pose and bag inspection. Browser bridge tests check guide pause/resume and all existing frame-handoff cases. Physical Windows/Android/iOS testing remains separate.

