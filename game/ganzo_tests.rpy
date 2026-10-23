label _shelter_test_ganzo_start:
    $ quick_menu = False
    $ shelter_visitor = "ganzo"
    $ shelter_run_order = ["ganzo"]
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

testsuite shelter_ganzo_checks:
    teardown:
        run Function(shelter_test_stop_watching)
        exit
    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        run Show("_shelter_test_driver", target="_shelter_test_ganzo_start")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 5

    testcase questions_aim_lower_and_admit:
        run Function(shelter_test_watch_frames)
        $ renpy.test.shelter_capture_frames = True
        run Show("_shelter_test_driver", target="shelter_visit_start")
        keysym "K_F10"
        pause until screen "shelter_questions" timeout 35
        assert eval ("ganzo" in SHELTER_VISITOR_ORDER and SHELTER_CIVILIANS["ganzo"])
        click expression GANZO_QUESTIONS[0]
        pause until screen "shelter_player_speech" timeout 3
        assert eval (renpy.music.get_playing(channel="shelter_player") == "audio/ganzo/ganzo asuult1.wav")
        pause until screen "shelter_decision" timeout 35
        click expression GANZO_QUESTIONS[1]
        pause until screen "shelter_decision" timeout 35
        click expression GANZO_QUESTIONS[2]
        pause until screen "shelter_decision" timeout 35
        assert eval (shelter_asked == [0, 1, 2])
        click "Буу онилох"
        pause until eval (shelter_still == "aim") timeout 15
        pause until screen "shelter_decision" timeout 3
        screenshot "../../tmp/ganzo/armed.png"
        click "Буугаа буулгах"
        pause until screen "shelter_decision" timeout 10
        assert eval (shelter_wait_image(shelter_still) == "images/transitions/ganzo/answer1-start.jpg")
        click "Оруулах"
        pause until screen "shelter_result" timeout 20
        assert eval (shelter_outcomes == {"ganzo": "admit"} and shelter_civilians_saved == 1)
        run Function(shelter_test_stop_watching)
        assert eval (not renpy.test.shelter_dark_frames)

    testcase rejection_and_shooting:
        parameter (choice, button) = [("reject", "Хөөх"), ("shoot", "Буудах")]
        if eval (choice == "shoot"):
            click "Буу онилох"
            pause until screen "shelter_decision" timeout 15
        click expression button
        pause until screen "shelter_result" timeout 20
        assert eval (shelter_outcomes == {"ganzo": choice} and shelter_visitors_seen == 1)
        assert eval (shelter_civilian_mistakes() == 1 and shelter_civilians_killed == int(choice == "shoot"))
