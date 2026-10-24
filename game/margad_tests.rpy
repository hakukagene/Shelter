label _shelter_test_margad_start:
    $ quick_menu = False
    $ shelter_visitor = "margad"
    $ shelter_run_order = ["margad"]
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
    jump shelter_question_phase

testsuite shelter_margad_checks:
    teardown:
        run Function(shelter_test_stop_watching)
        exit
    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        run Show("_shelter_test_driver", target="_shelter_test_margad_start")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 5

    testcase split_question_aim_lower_and_shoot:
        run Function(shelter_test_watch_frames)
        $ renpy.test.shelter_capture_frames = True
        assert eval ("margad" in SHELTER_VISITOR_ORDER and not SHELTER_CIVILIANS["margad"])
        assert eval (all(renpy.loadable(shelter_movie_frame("margad", clip, edge)) for clip in MARGAD_CLIPS for edge in ("start", "end")))
        click expression MARGAD_QUESTIONS[0]
        pause until screen "shelter_player_speech" timeout 3
        assert eval (renpy.music.get_playing(channel="shelter_player") == "audio/margad/margad asuult1 1heseg.wav")
        pause until screen "shelter_margad_answer1_playback" timeout 8
        pause until eval (renpy.get_screen("shelter_margad_answer1_playback").scope["stage"] == 1) timeout 20
        assert eval (renpy.music.get_pause(channel="shelter_video"))
        click expression MARGAD_QUESTION1_PART2
        assert eval (renpy.music.get_pause(channel="shelter_video"))
        pause until eval (renpy.get_screen("shelter_margad_answer1_playback").scope["stage"] == 4) timeout 12
        click expression MARGAD_QUESTION1_PART3
        pause until screen "shelter_decision" timeout 45
        assert eval (shelter_asked == [0] and shelter_still == "answer1_part3")
        click "Буу онилох"
        pause until screen "shelter_decision" timeout 12
        screenshot "../../tmp/margad/armed.png"
        click "Буугаа буулгах"
        pause until screen "shelter_decision" timeout 10
        assert eval (shelter_wait_image(shelter_still) == "images/transitions/margad/answer1-start.jpg")
        click "Буу онилох"
        pause until screen "shelter_decision" timeout 12
        click "Буудах"
        pause until screen "shelter_result" timeout 15
        assert eval (shelter_outcomes == {"margad": "shoot"} and shelter_civilian_mistakes() == 0)
        run Function(shelter_test_stop_watching)
        assert eval (not renpy.test.shelter_dark_frames)

    testcase rejection_and_admission:
        parameter (choice, button) = [("reject", "Хөөх"), ("admit", "Оруулах")]
        click expression button
        pause until screen "shelter_result" timeout 15
        assert eval (shelter_outcomes == {"margad": choice} and shelter_visitors_seen == 1)
        assert eval (shelter_civilian_mistakes() == 0 and shelter_civilians_killed == 0)
        if eval (choice == "admit"):
            assert eval (renpy.get_screen("shelter_result").scope["title"] == "ТА АЮУЛЫГ ДОТОГШ ОРУУЛЛАА")
