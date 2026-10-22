# Deeremchin encounter

Integrated from the final two-person section of the supplied `Хорогдох байр(1).docx` and the assets in user commit `e7ad94d`.

- One civilian man and one monster woman share a single encounter. New runs shuffle six encounters containing seven people. Existing shuffled saves keep their stored roster; start a new game to include the new encounter.
- All three distinct questions must finish before aiming unlocks. The armed decision offers only male/female targets, with no lower-gun option.
- Shooting either person leaves only admit/reject for the survivor. The shot is saved immediately and is never counted twice after loading.
- Admitting the woman, alone or with the man, triggers the monster ending. Admitting the man alone rescues one civilian. Rejecting both follows the authored attack; the man's death in that movie is not a shot by the player.
- Checked count increases by two when the encounter resolves, admitted count uses actual entrants, and the clock advances once. Shooting the man adds one civilian death; the fourth such death ends the game immediately.
- All 13 original WebMs and all four supplied player voice recordings are used without re-encoding. Subtitles follow audio cues. First/last decoded posters and fixed conversational/armed/survivor poses preserve the existing no-black handoff.
- Web export discovers the new clip map and converts the same sources; playback overlays receive the correct target button captions.

## Maintenance

After changing the WebMs, run `python tools/prepare_transition_frames.py --audit`. The media workflow also watches this encounter. The source files stay in Git LFS; posters and the source-hash manifest are committed normally.

Native tests: `renpy.sh . test shelter_deeremchin_checks`. The updated `shelter_transition_checks::actual_campaign_includes_all_encounters` covers the shuffled full preview, ledger counts, save/load and replay. `node tools/test_video_bridge.mjs` covers web handoff and target captions. These tests do not constitute physical Android, Windows or Safari validation.
