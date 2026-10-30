# Validation

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
