# Real decoder/UI integration for the two-person encounter and all six endings.
label _shelter_test_deeremchin_start:
    $ quick_menu = False
    $ shelter_visitor = "deeremchin"
    $ shelter_run_order = ["deeremchin"]
    $ shelter_outcomes = {}
    $ shelter_deeremchin_outcomes = {}
    $ shelter_visitors_seen = 0
    $ shelter_admitted = 0
    $ shelter_civilians_saved = 0
    $ shelter_civilians_killed = 0
    $ shelter_story_minutes = SHELTER_CLOCK_START
    $ shelter_still = "intro"
    $ shelter_asked = []
    jump shelter_question_phase

label _shelter_test_deeremchin_armed:
    $ shelter_asked = [0, 1, 2]
    $ shelter_still = "aim"
    call screen shelter_decision(armed=True)
    $ shelter_choice = _return
    jump shelter_handle_choice

testsuite shelter_deeremchin_checks:
    teardown:
        run Function(shelter_test_stop_watching)
        exit

    before testcase:
        run Function(shelter_test_stop_watching)
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        run Show("_shelter_test_driver", target="_shelter_test_deeremchin_start")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 10

    testcase questions_survivor_save_load_and_handoffs:
        run Function(shelter_test_watch_frames)
        $ renpy.test.shelter_capture_frames = True
        run Show("_shelter_test_driver", target="shelter_visit_start")
        keysym "K_F10"
        pause until screen "shelter_playback" timeout 5
        pause until screen "shelter_questions" timeout 15
        assert eval (not shelter_can_aim())
        click pos (0.77, 0.68) always
        pause 0.2
        assert screen "shelter_questions"
        screenshot "../../tmp/deeremchin/questions.png"
        click expression DEEREMCHIN_QUESTIONS[2]
        pause until screen "shelter_player_speech" timeout 5
        pause until screen "shelter_decision" timeout 20
        assert eval (not shelter_can_aim())
        click expression DEEREMCHIN_QUESTIONS[0]
        pause until eval (shelter_still == "answer1") timeout 20
        pause until screen "shelter_decision" timeout 5
        assert eval (not shelter_can_aim())
        click expression DEEREMCHIN_QUESTIONS[1]
        pause until eval (shelter_still == "answer2") timeout 25
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_asked == [2, 0, 1] and shelter_can_aim())
        click "Буу онилох"
        pause until eval (shelter_still == "aim") timeout 25
        pause until screen "shelter_decision" timeout 5
        assert "Эрэгтэйг буудах"
        assert "Эмэгтэйг буудах"
        assert not "Буугаа буулгах"
        screenshot "../../tmp/deeremchin/armed.png"
        click "Эмэгтэйг буудах"
        pause until eval (shelter_still == "shoot_woman") timeout 15
        pause until screen "shelter_decision" timeout 5
        assert not "Буу онилох"
        assert eval (shelter_deeremchin_survivor() == "man" and shelter_killed_total() == 1 and shelter_civilians_killed == 0)
        screenshot "../../tmp/deeremchin/man-survivor.png"
        run Function(shelter_test_stop_watching)
        assert eval (renpy.test.shelter_frame_count > 100 and not renpy.test.shelter_dark_frames)
        $ print("DEEREMCHIN FRAMES:", renpy.test.shelter_frame_count, "BLACK:", renpy.test.shelter_dark_frames)
        run Function(renpy.save, "deeremchin-survivor")
        click "Оруулах"
        pause until screen "shelter_result" timeout 20
        assert eval (shelter_deeremchin_outcomes == {"woman": "shoot", "man": "admit"})
        assert eval (shelter_visitors_seen == 2 and shelter_admitted == 1 and shelter_civilians_saved == 1)
        assert eval (shelter_clock_text() == "23:17")
        run Function(renpy.load, "deeremchin-survivor")
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_still == "shoot_woman" and shelter_deeremchin_outcomes == {"woman": "shoot"})
        assert eval (shelter_visitors_seen == 0 and shelter_civilians_saved == 0 and shelter_killed_total() == 1)
        click "Хөөх"
        pause until screen "shelter_result" timeout 15
        assert eval (shelter_deeremchin_outcomes == {"woman": "shoot", "man": "reject"})
        assert eval (shelter_visitors_seen == 2 and shelter_admitted == 0 and shelter_civilians_killed == 0 and shelter_killed_total() == 1)

    testcase survivor_endings:
        parameter (target, caption, survivor, civilian_deaths) = [("man", "Эрэгтэйг буудах", "woman", 1), ("woman", "Эмэгтэйг буудах", "man", 0)]
        parameter (choice, button) = [("admit", "Оруулах"), ("reject", "Хөөх")]
        run Show("_shelter_test_driver", target="_shelter_test_deeremchin_armed")
        keysym "K_F10"
        pause until screen "shelter_decision" timeout 5
        click expression caption
        pause until eval (shelter_still == "shoot_" + target) timeout 15
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_civilians_killed == civilian_deaths and shelter_killed_total() == 1)
        assert not "Буугаа буулгах"
        assert not "Буу онилох"
        click expression button
        pause until screen "shelter_playback" timeout 5
        assert eval (renpy.get_screen("shelter_playback").scope["clip"] == survivor + "_" + choice)
        pause until screen "shelter_result" timeout 20
        assert eval (shelter_visitors_seen == 2 and shelter_admitted == int(choice == "admit"))
        assert eval (shelter_civilians_saved == int(survivor == "man" and choice == "admit"))
        assert eval (shelter_deeremchin_outcomes == {target: "shoot", survivor: choice})
        assert eval ((renpy.get_screen("shelter_result").scope["title"] == "ТА АЮУЛЫГ ДОТОГШ ОРУУЛЛАА") == (survivor == "woman" and choice == "admit"))
        run Function(shelter_record_outcome, "deeremchin", choice)
        assert eval (shelter_visitors_seen == 2 and shelter_killed_total() == 1 and shelter_clock_text() == "23:17")

    testcase both_endings:
        parameter (choice, button) = [("admit", "Оруулах"), ("reject", "Хөөх")]
        click expression button
        pause until screen "shelter_result" timeout 20
        assert eval (shelter_visitors_seen == 2 and shelter_killed_total() == 0 and shelter_civilians_killed == 0)
        assert eval (shelter_admitted == (2 if choice == "admit" else 0))
        assert eval ((renpy.get_screen("shelter_result").scope["title"] == "ТА АЮУЛЫГ ДОТОГШ ОРУУЛЛАА") == (choice == "admit"))

    testcase civilian_death_boundary:
        parameter existing_deaths = [2, 3]
        run SetVariable("shelter_civilians_killed", existing_deaths)
        run Show("_shelter_test_driver", target="_shelter_test_deeremchin_armed")
        keysym "K_F10"
        pause until screen "shelter_decision" timeout 5
        click "Эрэгтэйг буудах"
        if eval (existing_deaths == 3):
            pause until screen "shelter_result" timeout 10
            assert eval (shelter_civilians_killed == 4 and shelter_campaign_status() == "casualties")
            assert eval (shelter_deeremchin_outcomes == {"man": "shoot"} and shelter_admitted == 0)
            assert eval (renpy.get_screen("shelter_result").scope["title"] == "ТА ХОЖИГДЛОО")
        else:
            pause until eval (shelter_still == "shoot_man") timeout 10
            pause until screen "shelter_decision" timeout 5
            assert eval (shelter_civilians_killed == 3 and shelter_campaign_status() == "continue")
            assert "Хөөх"
            assert "Оруулах"
