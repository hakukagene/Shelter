label _shelter_test_naraa_start:
    $ quick_menu = False
    $ shelter_visitor = "naraa"
    $ shelter_run_order = ["naraa"]
    $ shelter_outcomes = {}
    $ shelter_deeremchin_outcomes = {}
    $ shelter_visitors_seen = 0
    $ shelter_admitted = 0
    $ shelter_civilians_saved = 0
    $ shelter_civilians_killed = 0
    $ shelter_story_minutes = SHELTER_CLOCK_START
    $ shelter_inspection_progress = {}
    $ shelter_checkpoint_created = False
    $ shelter_still = "intro"
    $ shelter_asked = []
    jump shelter_decision_phase

testsuite shelter_naraa_transition_checks:
    teardown:
        run Function(shelter_test_stop_watching)
        exit
    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        run Show("_shelter_test_driver", target="_shelter_test_naraa_start")
        keysym "K_F9"
        pause until screen "shelter_decision" timeout 5

    testcase exact_posters_aim_lower_and_admit:
        run Function(shelter_test_watch_frames)
        $ renpy.test.shelter_capture_frames = True
        assert eval ("naraa" in SHELTER_VISITOR_ORDER and SHELTER_CIVILIANS["naraa"])
        assert eval (all(renpy.loadable(shelter_movie_frame("naraa", clip, edge)) for clip in NARAA_CLIPS for edge in ("start", "end")))
        click "Буу онилох"
        pause until screen "shelter_decision" timeout 20
        assert eval (shelter_still == "aim" and shelter_wait_image("aim") == "images/transitions/naraa/aim-end.jpg")
        screenshot "../../tmp/naraa/armed.png"
        click "Буугаа буулгах"
        pause until screen "shelter_decision" timeout 10
        assert eval (shelter_wait_image(shelter_still) == "images/transitions/naraa/answer1-start.jpg")
        screenshot "../../tmp/naraa/lowered.png"
        click "Оруулах"
        pause until screen "shelter_result" timeout 25
        assert eval (shelter_outcomes == {"naraa": "admit"} and shelter_civilians_saved == 1)
        run Function(shelter_test_stop_watching)
        assert eval (not renpy.test.shelter_dark_frames)

    testcase rejection_and_shooting:
        parameter (choice, button) = [("reject", "Хөөх"), ("shoot", "Буудах")]
        if eval (choice == "shoot"):
            click "Буу онилох"
            pause until screen "shelter_decision" timeout 20
        click expression button
        pause until screen "shelter_result" timeout 25
        assert eval (shelter_outcomes == {"naraa": choice} and shelter_visitors_seen == 1)
        assert eval (shelter_civilian_mistakes() == 1 and shelter_civilians_killed == int(choice == "shoot"))
