# Ren'Py 8.5 tests: run with "renpy.exe <project> test shelter_intro_flow".
# Screenshots and isolated test saves belong under tmp/, outside release assets.
testsuite shelter_intro_flow:
    teardown:
        exit

    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10

    after testcase:
        run Function(preferences.set_mute, "voice", False)

    testcase skip_button:
        assert eval ("menu1.mp3" in (renpy.music.get_playing() or ""))
        click "Эхлэх"
        pause until screen "shelter_intro_playback" timeout 10
        assert eval (renpy.music.get_playing() is None)
        pause until eval ((renpy.music.get_pos(channel="shelter_intro_video") or 0) > 2.0) timeout 15
        assert id "intro_subtitle"
        # Accidental clicks and normal dialogue shortcuts must not dismiss it.
        click pos (0.5, 0.4)
        keysym "K_SPACE"
        keysym "K_TAB"
        assert screen "shelter_intro_playback"
        screenshot "../../tmp/intro-tests/narration.png"
        move "Алгасах"
        screenshot "../../tmp/intro-tests/skip-hover.png"
        click "Алгасах"
        pause until screen "shelter_playback" timeout 10
        assert not screen "shelter_intro_playback"
        pause until eval (renpy.music.get_playing(channel="shelter_intro_video") is None) timeout 2
        assert eval (renpy.music.get_playing(channel="shelter_intro_video") is None)
        assert eval (shelter_visitor == "Chinba")
        assert eval (not _skipping)
        assert eval ("shuum.mp3" in (renpy.music.get_playing() or ""))
        run Show("shelter_result", title="ТЕСТ", description="")
        pause until eval ("menu2.mp3" in (renpy.music.get_playing() or "")) timeout 3
        assert eval ("menu2.mp3" in (renpy.music.get_playing() or ""))
        run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        assert eval ("menu1.mp3" in (renpy.music.get_playing() or ""))

    testcase muted_escape_and_restart:
        run Function(preferences.set_mute, "voice", True)
        click "Эхлэх"
        pause until screen "shelter_intro_playback" timeout 10
        pause until eval ((renpy.music.get_pos(channel="shelter_intro_video") or 0) > 2.0) timeout 15
        assert id "intro_subtitle"
        keysym "K_ESCAPE"
        pause until screen "shelter_playback" timeout 10
        pause until eval (renpy.music.get_playing(channel="shelter_intro_video") is None) timeout 2
        assert eval (renpy.music.get_playing(channel="shelter_intro_video") is None)
        run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        click "Эхлэх"
        pause until screen "shelter_intro_playback" timeout 10
        pause 0.5
        assert eval ((renpy.music.get_pos(channel="shelter_intro_video") or 0) < 2.0)
        keysym "K_ESCAPE"
        pause until screen "shelter_playback" timeout 10

    testcase full_playback:
        click "Эхлэх"
        pause until screen "shelter_intro_playback" timeout 10
        pause until eval ((renpy.music.get_pos(channel="shelter_intro_video") or 0) > 75.0) timeout 90
        screenshot "../../tmp/intro-tests/radio.png"
        pause until screen "shelter_playback" timeout 40
        assert not screen "shelter_intro_playback"
        pause until eval (renpy.music.get_playing(channel="shelter_intro_video") is None) timeout 2
        assert eval (renpy.music.get_playing(channel="shelter_intro_video") is None)
        assert eval (shelter_visitor == "Chinba")
        pause until screen "shelter_questions" timeout 25

testsuite shelter_maral_framing:
    teardown:
        exit

    testcase questions_and_lower:
        run Start("shelter_visit_start")
        pause until screen "shelter_questions" timeout 25
        assert eval (shelter_visitor == "Maral")
        screenshot "../../tmp/frame-tests/before.png"
        click "Чи ямар тайван байна аа. Айхгүй байгаа юм уу?"
        pause until screen "shelter_decision" timeout 20
        assert eval (shelter_still == "answer1" and shelter_asked == [0])
        assert eval (shelter_wait_image(shelter_still) == "images/Maral/frames/intro.jpg")
        screenshot "../../tmp/frame-tests/after-answer1.png"
        click "Манай хорогдох байрыг хаанаас сонссон бэ?"
        pause until eval (shelter_still == "answer2") timeout 20
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_wait_image(shelter_still) == "images/Maral/frames/intro.jpg")
        click "Надад худлаа яривал оруулахгүй гэдгийг мэдэж байгаа биз дээ?"
        pause until eval (shelter_still == "answer3") timeout 20
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_wait_image(shelter_still) == "images/Maral/frames/intro.jpg")
        click "Буу онилох"
        pause until eval (shelter_still == "aim") timeout 20
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_wait_image(shelter_still) == "images/Maral/frames/aim.jpg")
        click "Буугаа буулгах"
        pause until eval (shelter_still == "lower") timeout 10
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_wait_image(shelter_still) == "images/Maral/frames/intro.jpg")
        screenshot "../../tmp/frame-tests/after-lower.png"
