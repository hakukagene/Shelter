# These fixtures simulate the unreleased campaign; production never fabricates visitors.
label _shelter_test_midpoint_start:
    $ quick_menu = False
    $ shelter_visitor = "ganba"
    $ shelter_run_order = ["Chinba", "ganba", "Maral"]
    $ shelter_outcomes = {"Chinba": "admit"}
    $ shelter_deeremchin_outcomes = {}
    $ shelter_visitors_seen = 19
    $ shelter_admitted = 19
    $ shelter_civilians_saved = 19
    $ shelter_civilians_killed = 0
    $ shelter_story_minutes = 25 * 60
    $ shelter_checkpoint_created = False
    $ shelter_checkpoint_written = False
    $ shelter_still = "intro"
    $ shelter_asked = []
    jump shelter_question_phase

label _shelter_test_below_midpoint:
    $ shelter_civilians_saved = 19
    $ shelter_checkpoint_created = False
    call shelter_save_midpoint from _call_shelter_save_midpoint_1
    jump shelter_question_phase

testsuite shelter_protocol_checks:
    teardown:
        exit
    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        run Function(renpy.unlink_save, SHELTER_CHECKPOINT_SLOT)

    testcase intro_then_instructions_and_movie_pause:
        assert not "Үргэлжлүүлэх"
        click "Эхлэх"
        pause until screen "shelter_intro_playback" timeout 10
        click "Алгасах"
        pause until screen "shelter_protocol" timeout 5
        assert not screen "shelter_playback"
        keysym "K_ESCAPE"
        keysym "K_SPACE"
        assert screen "shelter_protocol"
        pause 0.4
        screenshot "../../tmp/protocol/instructions.png"
        click id "protocol_close"
        pause until screen "shelter_playback" timeout 10
        pause until eval ((renpy.music.get_pos(channel="shelter_video") or 0) > 1.0) timeout 8
        click id "protocol_open"
        pause until screen "shelter_protocol" timeout 3
        $ renpy.test.protocol_position = renpy.music.get_pos(channel="shelter_video")
        pause 1.0
        assert eval (abs(renpy.music.get_pos(channel="shelter_video") - renpy.test.protocol_position) < 0.15)
        assert eval (renpy.music.get_pause(channel="shelter_video"))
        click id "protocol_close"
        pause until eval ((renpy.music.get_pos(channel="shelter_video") or 0) > renpy.test.protocol_position + 0.4) timeout 4
        assert eval (not renpy.music.get_pause(channel="shelter_video"))

    testcase continue_ignores_manual_saves_below_twenty:
        run Show("_shelter_test_driver", target="_shelter_test_below_midpoint")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 5
        assert eval (not shelter_has_checkpoint() and not shelter_checkpoint_created)
        run Function(renpy.save, "manual-before-twenty")
        run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 5
        assert not "Үргэлжлүүлэх"

    testcase twentieth_save_load_skips_completed_encounters:
        run Show("_shelter_test_driver", target="_shelter_test_midpoint_start")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 5
        click "Оруулах"
        pause until screen "shelter_midpoint_checkpoint" timeout 20
        pause until eval (shelter_has_checkpoint()) timeout 4
        assert eval (shelter_civilians_saved == 20 and shelter_visitors_seen == 20)
        $ renpy.test.checkpoint_metadata = renpy.slot_json(SHELTER_CHECKPOINT_SLOT)
        $ renpy.test.checkpoint_clock = shelter_story_minutes
        pause until screen "shelter_next_visitor_card" timeout 5
        run Function(renpy.save, "newer-manual-save")
        run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 5
        assert "Үргэлжлүүлэх"
        screenshot "../../tmp/protocol/menu-with-checkpoint.png"
        click "Үргэлжлүүлэх"
        pause until screen "shelter_midpoint_checkpoint" timeout 8
        assert eval (shelter_checkpoint_created and shelter_checkpoint_written)
        assert eval (shelter_civilians_saved == 20 and shelter_visitors_seen == 20 and shelter_outcomes["ganba"] == "admit")
        assert eval (shelter_run_order == ["Chinba", "ganba", "Maral"] and shelter_story_minutes == renpy.test.checkpoint_clock)
        assert not screen "shelter_intro_playback"
        assert not screen "shelter_protocol"
        pause until screen "shelter_playback" timeout 15
        assert eval (shelter_visitor == "Maral")
        assert eval (renpy.slot_json(SHELTER_CHECKPOINT_SLOT) == renpy.test.checkpoint_metadata)

    testcase combined_mistakes_third_loses:
        run Show("_shelter_test_driver", target="_shelter_test_midpoint_start")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 5
        run SetVariable("shelter_outcomes", {})
        run Function(shelter_record_outcome, "Chinba", "reject")
        run Function(shelter_record_outcome, "Bayra", "shoot")
        assert eval (shelter_civilian_mistakes() == 2 and shelter_campaign_status() == "continue")
        run Function(shelter_record_outcome, "ganba", "reject")
        assert eval (shelter_civilian_mistakes() == 3 and shelter_campaign_status() == "casualties")
        assert eval (shelter_civilians_killed == 1)
        run Function(shelter_record_outcome, "ganba", "reject")
        assert eval (shelter_civilian_mistakes() == 3)
