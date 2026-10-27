label _shelter_test_undral_start:
    $ quick_menu = False
    $ shelter_visitor = "undral"
    $ shelter_run_order = ["undral"]
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

testsuite shelter_undral_checks:
    teardown:
        exit
    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        run Show("_shelter_test_driver", target="_shelter_test_undral_start")
        keysym "K_F9"
        pause until screen "shelter_decision" timeout 5

    testcase questions_aim_lower_and_shoot:
        parameter question = [0, 1, 2]
        assert eval ("undral" in SHELTER_VISITOR_ORDER and not SHELTER_CIVILIANS["undral"])
        assert eval (all(renpy.loadable("Video/undral/" + filename) for filename, duration in UNDRAL_CLIPS.values()))
        assert eval (all(renpy.loadable(path) for path in UNDRAL_POSTERS.values()))
        click expression UNDRAL_QUESTIONS[question]
        pause until screen "shelter_player_speech" timeout 5
        assert eval (shelter_player_voice("question%d" % (question + 1), "undral") is not None)
        pause until screen "shelter_decision" timeout 120
        assert eval (question in shelter_asked)
        click "Буу онилох"
        pause until screen "shelter_decision" timeout 120
        assert eval (shelter_wait_image("aim", "undral") == UNDRAL_POSTERS["aim"])
        click "Буугаа буулгах"
        pause until screen "shelter_decision" timeout 30
        assert eval (shelter_wait_image("lower", "undral") == UNDRAL_POSTERS["idle"])
        click "Буу онилох"
        pause until screen "shelter_decision" timeout 120
        click "Буудах"
        pause until screen "shelter_result" timeout 120
        assert eval (shelter_outcomes == {"undral": "shoot"} and shelter_civilian_mistakes() == 0)

    testcase rejection_or_monster_admission:
        parameter (choice, button) = [("reject", "Хөөх"), ("admit", "Оруулах")]
        click expression button
        pause until screen "shelter_result" timeout 120
        assert eval (shelter_outcomes == {"undral": choice} and shelter_civilian_mistakes() == 0)
        if eval (choice == "admit"):
            assert eval (shelter_admitted_monster())
            assert eval (renpy.get_screen("shelter_result").scope["title"] == "ТА АЮУЛЫГ ДОТОГШ ОРУУЛЛАА")
