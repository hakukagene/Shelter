# Exercise the real question/action flow, including decoder handoff.
testsuite shelter_player_voice_checks:
    teardown:
        exit

    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        run Show("_shelter_test_driver", target="shelter_question_phase")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 10
        run SetVariable("shelter_asked", [])
        run SetVariable("shelter_outcomes", {})
        run SetVariable("shelter_visitors_seen", 0)
        run SetVariable("shelter_admitted", 0)
        run SetVariable("shelter_civilians_saved", 0)
        run SetVariable("shelter_civilians_killed", 0)

    testcase supplied_questions_precede_response:
        parameter (visitor, index) = [("Swat", 0), ("Swat", 1), ("Swat", 2), ("anu", 0), ("anu", 1)]
        run SetVariable("shelter_visitor", visitor)
        click expression SHELTER_VISITORS[visitor]["questions"][index]
        pause until screen "shelter_player_speech" timeout 3
        assert eval (renpy.music.get_playing(channel="shelter_player") == SHELTER_SUPPLIED_PLAYER_VOICES[visitor]["question%d" % (index + 1)][0])
        assert not screen "shelter_playback"
        pause until screen "shelter_playback" timeout 10
        assert eval (not renpy.music.get_playing(channel="shelter_player"))
        pause until screen "shelter_decision" timeout 30
        assert eval (shelter_still == "answer%d" % (index + 1) and shelter_asked == [index])

    testcase missing_actions_reuse_previous_recording:
        parameter (choice, caption, expected) = [("admit", "Оруулах", "audio/Chingune/ChinbaOruulah.wav"), ("reject", "Хөөх", "audio/Chingune/MaralHuuh.wav")]
        run SetVariable("shelter_visitor", "anu")
        run SetVariable("shelter_run_order", ["anu"])
        click expression caption
        pause until screen "shelter_player_speech" timeout 3
        assert eval (renpy.music.get_playing(channel="shelter_player") == expected)
        assert not screen "shelter_playback"
        pause until screen "shelter_playback" timeout 8
        assert eval (not renpy.music.get_playing(channel="shelter_player"))
        pause until screen "shelter_result" timeout 30
        assert eval (shelter_outcomes == {"anu": choice} and shelter_visitors_seen == 1)

    testcase complete_paths_and_preserved_dedicated_voices:
        assert eval (all(renpy.loadable(cue[0]) and 0 <= cue[1] < cue[2] for cues in SHELTER_SUPPLIED_PLAYER_VOICES.values() for cue in cues.values()))
        assert eval (all(shelter_player_voice(key, visitor) and renpy.loadable(shelter_player_voice(key, visitor)[0]) for visitor in SHELTER_VISITOR_ORDER for key in ("admit", "reject")))
        assert eval (shelter_player_voice("admit", "Swat")[0] == "audio/SwatQuestion/oruulah.wav")
        assert eval (shelter_player_voice("reject", "deeremchin")[0] == "audio/deeremchin/CHinguun 2uulang ni hoov.mp3")
        assert eval (shelter_player_voice("survivor_reject", "deeremchin")[0] == "audio/Chingune/MaralHuuh.wav")
        assert eval (shelter_player_voice("survivor_admit", "deeremchin")[0] == "audio/Chingune/ChinbaOruulah.wav")
        assert eval (shelter_player_voice("missing_question", "anu") is None)
