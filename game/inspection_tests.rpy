# Run with Ren'Py 8.5: renpy.sh <project> test shelter_inspection_checks
testsuite shelter_inspection_checks:
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
        run SetVariable("shelter_inspection_progress", {})
        run SetVariable("shelter_inspection_requests", [])
        run SetVariable("shelter_inspection_views", {})
        run SetVariable("shelter_outcomes", {})
        run SetVariable("shelter_visitors_seen", 0)
        run SetVariable("shelter_admitted", 0)
        run SetVariable("shelter_civilians_killed", 0)
        run SetVariable("quick_menu", False)

    testcase original_art_assets:
        assert eval (all(renpy.loadable("images/inspection/" + spec[0]) for spec in SHELTER_INSPECTION_SPRITES.values()))

    testcase chinba_inspect_reopen_save_load:
        run SetVariable("shelter_visitor", "Chinba")
        click "Үүргэвч дотрохоо харуул."
        pause until screen "shelter_inspection" timeout 20
        assert eval (shelter_asked == [2])
        pause 0.3
        screenshot "../../tmp/inspection-tests/chinba-desk.png"
        click id "inspection_item_meal"
        click "Савлагааг шалгах"
        assert eval (shelter_inspection_done("Chinba", "meal"))
        click "Тавих"
        click id "inspection_item_charger"
        click "Ойроос шалгах"
        assert eval (shelter_inspection_done("Chinba", "charger"))
        click id "inspection_item_schedule"
        click "Хуваарийг унших"
        click id "inspection_plus"
        assert eval (renpy.get_screen("shelter_inspection").scope["viewer"].magnification > 1.0)
        drag pos (900, 420) to pos (1030, 420) steps 8
        assert eval (renpy.get_screen("shelter_inspection").scope["viewer"].angle != 0)
        screenshot "../../tmp/inspection-tests/chinba-schedule.png"
        run Function(renpy.save, "inspection-test")
        click "ҮЗЛЭГ ДУУСГАХ"
        pause until screen "shelter_decision" timeout 5
        run Function(renpy.load, "inspection-test")
        pause until screen "shelter_inspection" timeout 5
        assert eval (len(shelter_inspection_progress["Chinba"]) == 3)
        assert eval (renpy.get_screen("shelter_inspection").scope["viewer"].angle != 0)
        assert eval (renpy.get_screen("shelter_inspection").scope["selected_item"] == "schedule")
        click "ҮЗЛЭГ ДУУСГАХ"
        pause until screen "shelter_decision" timeout 5
        click "Үүргэвч дотрохоо харуул."
        pause until screen "shelter_inspection" timeout 2
        assert eval (shelter_asked == [2])
        keysym "K_ESCAPE"
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_visitors_seen == 0 and shelter_admitted == 0 and shelter_civilians_killed == 0)

    testcase anu_find_drawing_before_answer:
        run SetVariable("shelter_visitor", "anu")
        click "Цүнхээ нээгээд харуул даа."
        pause until screen "shelter_player_speech" timeout 3
        assert eval (renpy.music.get_playing(channel="shelter_player") == "audio/anu/anu asuult3.wav")
        pause until screen "shelter_inspection" timeout 5
        assert eval (shelter_inspection_requests == ["anu"])
        assert eval (shelter_asked == [])
        assert not "Энэ зургийн тухай асуух"
        click id "inspection_item_rabbit"
        click "Ойроос шалгах"
        click id "inspection_item_notebook"
        click "Дэвтрийг нээх"
        screenshot "../../tmp/inspection-tests/anu-drawing.png"
        run Function(renpy.save, "inspection-test")
        click "ҮЗЛЭГ ДУУСГАХ"
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_asked == [])
        click "Цүнхээ нээгээд харуул даа."
        pause until screen "shelter_inspection" timeout 2
        assert eval (shelter_inspection_done("anu", "notebook"))
        click id "inspection_item_notebook"
        click "Дэвтрийг нээх"
        click "Энэ зургийн тухай асуух"
        pause until screen "shelter_player_speech" timeout 3
        assert eval (renpy.music.get_playing(channel="shelter_player") == "audio/anu/anu zurag asuuh.wav")
        pause until screen "shelter_decision" timeout 20
        assert eval (shelter_still == "answer3" and shelter_asked == [2])
        click "Цүнхээ нээгээд харуул даа."
        pause until screen "shelter_inspection" timeout 2
        click id "inspection_item_notebook"
        click "Дэвтрийг нээх"
        assert not "Энэ зургийн тухай асуух"
        click "Дэвтрийг хаах"
        assert "Дэвтрийг нээх"
        click "ҮЗЛЭГ ДУУСГАХ"
        assert eval (shelter_visitors_seen == 0 and shelter_outcomes == {})

    testcase bayra_closed_bag_and_no_other_bags:
        run SetVariable("shelter_visitor", "Bayra")
        click "Наад цүнхэн доторхоо харуулаач"
        pause until screen "shelter_inspection" timeout 30
        click id "inspection_item_business_bag"
        click "Гаднаас нь шалгах"
        screenshot "../../tmp/inspection-tests/bayra-closed.png"
        assert eval (shelter_inspection_progress == {"Bayra": ("business_bag",)})
        assert eval (SHELTER_INSPECTIONS["Bayra"]["items"] == ("business_bag",))
        assert eval (not shelter_has_inspection("Maral", 2) and not shelter_has_inspection("Swat", 2))
        keysym "K_ESCAPE"
        pause until screen "shelter_decision" timeout 5
        click "Наад цүнхэн доторхоо харуулаач"
        pause until screen "shelter_inspection" timeout 2
        assert eval (shelter_asked == [2] and shelter_visitors_seen == 0)
        click "ҮЗЛЭГ ДУУСГАХ"
