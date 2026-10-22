# Run with Ren'Py 8.5: renpy.exe <project> test shelter_updated_encounters
screen _shelter_test_driver(target):
    zorder 10000
    key "K_F9" action [Hide("_shelter_test_driver"), Start(target)]
    key "K_F10" action [Hide("_shelter_test_driver"), Jump(target)]

testsuite shelter_updated_encounters:
    teardown:
        exit

    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        run Show("_shelter_test_driver", target="shelter_question_phase")
        keysym "K_F9"
        pause until screen "shelter_questions" timeout 10
        run SetVariable("shelter_outcomes", {})
        run SetVariable("shelter_visitors_seen", 0)
        run SetVariable("shelter_admitted", 0)
        run SetVariable("shelter_civilians_saved", 0)
        run SetVariable("shelter_civilians_killed", 0)

    testcase bayra_questions_and_reject_to_anu:
        run SetVariable("shelter_visitor", "Bayra")
        run Show("_shelter_test_driver", target="shelter_visit_start")
        keysym "K_F10"
        pause until screen "shelter_playback" timeout 5
        pause until eval ((renpy.music.get_pos(channel="shelter_video") or 0) > 1.0) timeout 10
        pause until screen "shelter_questions" timeout 25
        click "Та хэн бэ?"
        pause until screen "shelter_player_speech" timeout 5
        pause until screen "shelter_decision" timeout 45
        click "Та энэ хорогдох байрыг хаанаас мэдэж ирэв?"
        pause until eval (shelter_still == "answer2") timeout 25
        pause until screen "shelter_decision" timeout 5
        click "Наад цүнхэн доторхоо харуулаач"
        pause until eval (shelter_still == "answer3") timeout 30
        pause until screen "shelter_inspection" timeout 5
        click "ҮЗЛЭГ ДУУСГАХ"
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_asked == [0, 1, 2])
        assert eval (shelter_wait_image(shelter_still) == "images/Bayra/frames/idle.jpg")
        click "Буу онилох"
        pause until eval (shelter_still == "aim") timeout 20
        pause until screen "shelter_decision" timeout 5
        click "Буугаа буулгах"
        pause until eval (shelter_still == "lower") timeout 10
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_wait_image(shelter_still) == "images/Bayra/frames/idle.jpg")
        click "Хөөх"
        pause until screen "shelter_next_visitor_card" timeout 20
        assert eval (shelter_visitors_seen == 1 and shelter_admitted == 0)
        pause until eval (shelter_visitor == "anu") timeout 15
        pause until screen "shelter_questions" timeout 25
        assert eval (shelter_asked == [])
        click "Хөөх"
        pause until screen "shelter_result" timeout 30
        assert eval (shelter_outcomes == {"Bayra": "reject", "anu": "reject"})
        assert eval (shelter_visitors_seen == 2 and shelter_civilians_killed == 0)

    testcase bayra_admit_and_anu_monster_ending:
        run SetVariable("shelter_visitor", "Bayra")
        click "Оруулах"
        pause until screen "shelter_next_visitor_card" timeout 20
        assert eval (shelter_admitted == 1 and shelter_civilians_saved == 1)
        pause until eval (shelter_visitor == "anu") timeout 15
        pause until screen "shelter_questions" timeout 25
        click "Оруулах"
        pause until screen "shelter_anu_admission" timeout 5
        pause until screen "shelter_result" timeout 5
        assert eval (shelter_outcomes == {"Bayra": "admit", "anu": "admit"})
        assert eval (shelter_admitted == 2 and shelter_civilians_saved == 1)
        assert eval (shelter_monster_ending.startswith("Ану"))

    testcase anu_questions_lower_and_shoot:
        run SetVariable("shelter_visitor", "anu")
        run SetVariable("shelter_still", "intro")
        run SetVariable("shelter_asked", [])
        click "Ээжийг чинь хамгийн сүүлд хаана харсан бэ?"
        pause until screen "shelter_decision" timeout 25
        click "Замд чинь том хүн тааралдаагүй гэж үү?"
        pause until eval (shelter_still == "answer2") timeout 30
        pause until screen "shelter_decision" timeout 5
        click "Цүнхээ нээгээд харуул даа."
        pause until screen "shelter_inspection" timeout 5
        click id "inspection_item_notebook"
        click "Дэвтрийг нээх"
        click "Энэ зургийн тухай асуух"
        pause until eval (shelter_still == "answer3") timeout 20
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_asked == [0, 1, 2])
        click "Буу онилох"
        pause until eval (shelter_still == "aim") timeout 20
        pause until screen "shelter_decision" timeout 5
        click "Буугаа буулгах"
        pause until eval (shelter_still == "lower") timeout 10
        pause until screen "shelter_decision" timeout 5
        assert eval (shelter_wait_image(shelter_still) == "images/anu/frames/idle.jpg")
        click "Буу онилох"
        pause until eval (shelter_still == "aim") timeout 20
        pause until screen "shelter_decision" timeout 5
        click "Буудах"
        pause until screen "shelter_result" timeout 15
        assert eval (shelter_outcomes == {"anu": "shoot"})
        assert eval (shelter_visitors_seen == 1 and shelter_civilians_killed == 0)
