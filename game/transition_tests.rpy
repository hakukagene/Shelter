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
        pause until screen "shelter_questions" timeout 25
        assert eval (shelter_visitor == "Chinba")
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 25
        assert eval (shelter_visitors_seen == 1)
        pause until screen "shelter_questions" timeout 30
        assert eval (shelter_visitor == "Maral")
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 15
        screenshot "../../tmp/transition-check/after-maral.png"
        assert eval (shelter_visitors_seen == 2 and shelter_outcomes["Maral"] == "reject")
        pause until screen "shelter_questions" timeout 35
        assert eval (shelter_visitor == "Swat")
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 20
        pause until screen "shelter_questions" timeout 35
        assert eval (shelter_visitor == "Bayra")
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 20
        assert eval (shelter_visitors_seen == 4)
        pause until screen "shelter_questions" timeout 35
        assert eval (shelter_visitor == "anu" and shelter_asked == [])
        screenshot "../../tmp/transition-check/anu-in-campaign.png"
        click "Цүнхээ нээгээд харуул даа."
        pause until screen "shelter_inspection" timeout 5
        click id "inspection_item_notebook"
        click "Дэвтрийг нээх"
        click "Энэ зургийн тухай асуух"
        pause until screen "shelter_decision" timeout 20
        assert eval (shelter_asked == [2])
        click "Хөөх"
        pause until screen "shelter_result" timeout 30
        assert eval (shelter_visitors_seen == 5 and shelter_admitted == 0 and shelter_civilians_killed == 0)
        assert eval (list(shelter_outcomes) == list(SHELTER_VISITOR_ORDER))
