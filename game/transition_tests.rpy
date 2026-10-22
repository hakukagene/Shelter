# Native integration tests: every movie plays to real EOF at normal speed.
default shelter_test_clip_count = 0

label _shelter_test_all_clips:
    $ quick_menu = False
    $ shelter_test_clip_count = 0
    $ shelter_test_visitors = list(SHELTER_VISITOR_ORDER)
    while shelter_test_visitors:
        $ shelter_visitor = shelter_test_visitors.pop(0)
        $ shelter_test_clips = list(shelter_data("clips"))
        while shelter_test_clips:
            $ shelter_test_clip = shelter_test_clips.pop(0)
            call shelter_clip(shelter_test_clip)
            $ shelter_test_clip_count += 1
            $ renpy.log("TRANSITION PASS: %s/%s (%d/44)" % (shelter_visitor, shelter_test_clip, shelter_test_clip_count))
            $ renpy.screenshot(config.basedir + "/tmp/transition-check/%s-%s.png" % (shelter_visitor, shelter_test_clip))
    call screen _shelter_transition_test_done
    return

screen _shelter_transition_test_done():
    modal True
    text "Playback checks complete" align (0.5, 0.5)

testsuite shelter_transition_checks:
    teardown:
        exit

    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10

    testcase all_movie_boundaries:
        assert eval (all(renpy.loadable(shelter_movie_frame(v, c, edge)) for v in SHELTER_VISITOR_ORDER for c in SHELTER_VISITORS[v]["clips"] for edge in ("start", "end")))
        run Show("_shelter_test_driver", target="_shelter_test_all_clips")
        keysym "K_F9"
        pause until screen "_shelter_transition_test_done" timeout 700
        assert eval (shelter_test_clip_count == 44)
        assert eval (renpy.music.get_playing(channel="shelter_video") is None)

    testcase actual_campaign_reaches_anu:
        run Show("_shelter_test_driver", target="shelter_encounter")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 30
        # Keep expectations outside the saved store, so loading cannot roll them back.
        $ renpy.test.shelter_expected_order = tuple(shelter_run_order)
        assert eval (len(renpy.test.shelter_expected_order) == len(set(renpy.test.shelter_expected_order)) == len(SHELTER_VISITOR_ORDER))
        assert eval (set(renpy.test.shelter_expected_order) == set(SHELTER_VISITOR_ORDER))
        $ print("RANDOM CAMPAIGN:", renpy.test.shelter_expected_order)
        run Function(renpy.save, "random-questions")
        # Visitor 1: use the saved permutation, including Anu in any position.
        assert eval (shelter_visitor == renpy.test.shelter_expected_order[0] and shelter_asked == [])
        assert eval (shelter_visitors_seen == 0)
        if eval (shelter_visitor == "anu"):
            click "Цүнхээ нээгээд харуул даа."
            pause until screen "shelter_inspection" timeout 5
            click id "inspection_item_notebook"
            click "Дэвтрийг нээх"
            click "Энэ зургийн тухай асуух"
            pause until screen "shelter_decision" timeout 20
            assert eval (shelter_asked == [2])
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 30
        assert eval (shelter_visitors_seen == 1)
        run Function(renpy.save, "random-clock")
        # Loading the earlier question must restore both order and counters.
        run Function(renpy.load, "random-questions")
        pause until screen "shelter_questions" timeout 5
        assert eval (tuple(shelter_run_order) == renpy.test.shelter_expected_order and shelter_visitor == renpy.test.shelter_expected_order[0])
        assert eval (shelter_visitors_seen == 0 and shelter_outcomes == {})
        run Function(renpy.load, "random-clock")
        pause until screen "shelter_next_visitor_card" timeout 5
        assert eval (tuple(shelter_run_order) == renpy.test.shelter_expected_order and shelter_visitors_seen == 1)
        pause until screen "shelter_questions" timeout 40
        # Visitor 2: use the saved permutation, including Anu in any position.
        assert eval (shelter_visitor == renpy.test.shelter_expected_order[1] and shelter_asked == [])
        assert eval (shelter_visitors_seen == 1)
        if eval (shelter_visitor == "anu"):
            click "Цүнхээ нээгээд харуул даа."
            pause until screen "shelter_inspection" timeout 5
            click id "inspection_item_notebook"
            click "Дэвтрийг нээх"
            click "Энэ зургийн тухай асуух"
            pause until screen "shelter_decision" timeout 20
            assert eval (shelter_asked == [2])
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 30
        assert eval (shelter_visitors_seen == 2)
        pause until screen "shelter_questions" timeout 40
        # Visitor 3: use the saved permutation, including Anu in any position.
        assert eval (shelter_visitor == renpy.test.shelter_expected_order[2] and shelter_asked == [])
        assert eval (shelter_visitors_seen == 2)
        if eval (shelter_visitor == "anu"):
            click "Цүнхээ нээгээд харуул даа."
            pause until screen "shelter_inspection" timeout 5
            click id "inspection_item_notebook"
            click "Дэвтрийг нээх"
            click "Энэ зургийн тухай асуух"
            pause until screen "shelter_decision" timeout 20
            assert eval (shelter_asked == [2])
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 30
        assert eval (shelter_visitors_seen == 3)
        pause until screen "shelter_questions" timeout 40
        # Visitor 4: use the saved permutation, including Anu in any position.
        assert eval (shelter_visitor == renpy.test.shelter_expected_order[3] and shelter_asked == [])
        assert eval (shelter_visitors_seen == 3)
        if eval (shelter_visitor == "anu"):
            click "Цүнхээ нээгээд харуул даа."
            pause until screen "shelter_inspection" timeout 5
            click id "inspection_item_notebook"
            click "Дэвтрийг нээх"
            click "Энэ зургийн тухай асуух"
            pause until screen "shelter_decision" timeout 20
            assert eval (shelter_asked == [2])
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 30
        assert eval (shelter_visitors_seen == 4)
        pause until screen "shelter_questions" timeout 40
        # Visitor 5: use the saved permutation, including Anu in any position.
        assert eval (shelter_visitor == renpy.test.shelter_expected_order[4] and shelter_asked == [])
        assert eval (shelter_visitors_seen == 4)
        if eval (shelter_visitor == "anu"):
            click "Цүнхээ нээгээд харуул даа."
            pause until screen "shelter_inspection" timeout 5
            click id "inspection_item_notebook"
            click "Дэвтрийг нээх"
            click "Энэ зургийн тухай асуух"
            pause until screen "shelter_decision" timeout 20
            assert eval (shelter_asked == [2])
        click "Хөөх"
        pause until screen "shelter_result" timeout 30
        assert eval (renpy.get_screen("shelter_result").scope["title"] == "ТУРШИЛТЫН ХЭСЭГ ДУУСЛАА")
        assert eval (tuple(shelter_outcomes) == renpy.test.shelter_expected_order)
        assert eval (shelter_visitors_seen == 5 and shelter_admitted == 0 and shelter_civilians_killed == 0)
        # Seed only the test: verify replay creates a fresh order and resets progress.
        run Function(renpy.random.seed, 41)
        $ renpy.test.shelter_expected_replay = tuple(shelter_make_visitor_order())
        run Function(renpy.random.seed, 41)
        click "Дахин тоглох"
        pause until screen "shelter_questions" timeout 30
        assert eval (tuple(shelter_run_order) == renpy.test.shelter_expected_replay)
        assert eval (shelter_visitor == renpy.test.shelter_expected_replay[0] and shelter_outcomes == {})
        assert eval (shelter_visitors_seen == 0 and shelter_inspection_progress == {})

    testcase random_roster_and_legacy_saves:
        # Deterministic seeds cover all starting/ending positions without flaky
        # assertions that two genuinely random permutations must always differ.
        python:
            orders = []
            for seed in range(100):
                renpy.random.seed(seed)
                orders.append(tuple(shelter_make_visitor_order()))
        assert eval (all(len(order) == len(set(order)) == len(SHELTER_VISITOR_ORDER) and set(order) == set(SHELTER_VISITOR_ORDER) for order in orders))
        assert eval (set(order[0] for order in orders) == set(SHELTER_VISITOR_ORDER))
        assert eval (set(order[-1] for order in orders) == set(SHELTER_VISITOR_ORDER))
        assert eval (len(set(orders)) > 1)
        run SetVariable("shelter_run_order", None)
        run SetVariable("shelter_visitor", "Bayra")
        run SetVariable("shelter_outcomes", {"Chinba": "reject", "Maral": "reject", "Swat": "reject", "Bayra": "reject"})
        assert eval (shelter_next_visitor_id() == "anu")
        run SetVariable("shelter_visitor", "anu")
        assert eval (shelter_next_visitor_id() is None)
