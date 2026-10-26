# Run with Ren'Py 8.5: test shelter_shooting_checks
testsuite shelter_shooting_checks:
    teardown:
        exit

    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        click "Буудлагын туршилт"
        pause until screen "shelter_shooting_sandbox" timeout 10

    testcase hit_animation_reload_and_exit:
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == 8)
        screenshot "../../tmp/shooting-tests/idle.png"
        click pos (520, 420)
        pause .08
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == 1)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].hits == 1)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == 7)
        screenshot "../../tmp/shooting-tests/firing.png"
        click id "shooting_test_fire"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == 1)
        pause .5
        keysym "K_r"
        pause .4
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "reload")
        screenshot "../../tmp/shooting-tests/reloading.png"
        click id "shooting_test_fire"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == 1)
        pause until eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "idle") timeout 3
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == 8)
        keysym "K_SPACE"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == 7)
        keysym "K_ESCAPE"
        pause until screen "main_menu" timeout 5
        assert eval (renpy.music.get_playing(channel="shooting_test_sfx") is None)

    testcase empty_magazine_and_touch_controls:
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_fire"
        pause .46
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == 0)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == 8)
        click id "shooting_test_fire"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == 8)
        click id "shooting_test_reload"
        pause until eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "idle") timeout 3
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == 8)
        click id "shooting_test_back"
        pause until screen "main_menu" timeout 5
