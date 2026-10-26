# Run with Ren'Py 8.5: test shelter_shooting_checks
testsuite shelter_shooting_checks:
    teardown:
        exit

    before testcase:
        if not screen "main_menu":
            run MainMenu(confirm=False)
        pause until screen "main_menu" timeout 10
        pause .3
        click "Буудлагын туршилт"
        pause until screen "shelter_shooting_sandbox" timeout 10

    testcase hit_animation_reload_and_exit:
        assert eval (len(SHOOTING_TEST_FRAMES) == 56)
        assert eval (all(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].frame_at(index/25.0+.00001, "reload") == 11+index for index in range(45)))
        assert eval (SHOOTING_TEST_RELOAD_FPS == 25 and len(SHOOTING_TEST_RELOAD_FRAMES) == 45)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].frame_at(.20,"reload") == renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].frame_at(.23999,"reload"))
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].frame_at(.23999,"reload") != renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].frame_at(.24,"reload"))
        assert eval (all(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].reload_frame_index(index/25.0+.00001) == index for index in range(45)))
        assert eval ((800-656)*math.cos(math.radians(14)) - 400*math.sin(math.radians(14)) > 0)
        assert eval (all(renpy.loadable("images/shooting_test/sequence/%s.png" % pose) for pose in SHOOTING_TEST_POSES))
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].frame_at(.03, "fire") == 1)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].frame_at(.10, "fire") == 3)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].frame_at(.30, "fire") == 8)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY)
        screenshot "../../tmp/shooting-tests/idle.png"
        click pos (520, 420)
        click id "shooting_test_fire"
        pause .025
        screenshot "../../tmp/shooting-tests/firing.png"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == 1)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].hits == 1)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY-1)
        pause .5
        keysym "K_r"
        pause .4
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "reload")
        screenshot "../../tmp/shooting-tests/reloading.png"
        click id "shooting_test_fire"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == 1)
        pause until eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "idle") timeout 3
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY)
        keysym "K_SPACE"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY-1)
        keysym "K_ESCAPE"
        pause until screen "main_menu" timeout 5
        pause until eval (renpy.music.get_playing(channel="shooting_test_sfx") is None) timeout 1
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
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == SHOOTING_TEST_CAPACITY)
        click id "shooting_test_fire"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].shots == SHOOTING_TEST_CAPACITY)
        click id "shooting_test_reload"
        pause until eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "idle") timeout 3
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY)
        click id "shooting_test_back"
        pause until screen "main_menu" timeout 5

    testcase repaired_rack_sleeve:
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_reload"
        pause 1.30
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "reload")
        screenshot "../../tmp/shooting-tests/repaired-rack.png"
        pause until eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "idle") timeout 3
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY)
        click id "shooting_test_back"
        pause until screen "main_menu" timeout 5

    testcase monster_approach_strike_and_hits:
        assert eval (len(SHOOTING_MONSTER_FRAMES) == 12)
        click id "shooting_test_monster_restart"
        run Function(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.restart,route=1)
        pause .5
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.state == "approach")
        screenshot "../../tmp/shooting-tests/monster-approach.png"
        run Function(setattr,renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster,"approach_started",time.perf_counter()-4.1)
        pause until eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.impacts >= 1) timeout 2
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.state == "strike")
        run Function(renpy.render_to_file,renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster,"tmp/shooting-tests/monster-layer.png",width=1920,height=1080,resize=True)
        screenshot "../../tmp/shooting-tests/monster-strike.png"
        click pos (970,420)
        pause .46
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.hp == 2)
        click pos (970,420)
        pause .46
        click pos (970,420)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.state == "gone")
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.kills == 1)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY-3)
        pause until eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.hp == 3) timeout 4
        click id "shooting_test_back"
        pause until screen "main_menu" timeout 5
        pause until eval (renpy.music.get_playing(channel="shooting_test_monster") is None) timeout 1

    testcase monster_three_road_lanes:
        assert eval (all(530+(855-530)*(1-p**1.25) <= renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.geometry_at_progress(p,route)[0] <= 1510+(1060-1510)*(1-p**1.25) for route in range(3) for p in [index/40.0 for index in range(41)]))
        assert eval (all(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.geometry_at_progress(1,route) == (SHOOTING_MONSTER_LANES_NEAR[route],604,288) for route in range(3)))
        assert eval (all(316 <= renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.geometry_at_progress(p,route)[1]-renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.geometry_at_progress(p,route)[2] <= 448 for route in range(3) for p in [index/40.0 for index in range(41)]))
        run Function(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.restart,route=0)
        run Function(setattr,renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster,"approach_started",time.perf_counter()-4.1)
        pause .15
        screenshot "../../tmp/shooting-tests/monster-lane-left.png"
        run Function(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.restart,route=1)
        run Function(setattr,renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster,"approach_started",time.perf_counter()-4.1)
        pause .15
        screenshot "../../tmp/shooting-tests/monster-lane-center.png"
        run Function(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.restart,route=2)
        run Function(setattr,renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster,"approach_started",time.perf_counter()-4.1)
        pause .15
        screenshot "../../tmp/shooting-tests/monster-lane-right.png"
        click id "shooting_test_back"
        pause until screen "main_menu" timeout 5

    testcase monster_debug_overlay:
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].debug_enabled)
        run Function(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.restart,route=2)
        run Function(setattr,renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster,"approach_started",time.perf_counter()-4.1)
        pause .15
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.hit_test((1420,420),time.perf_counter()))
        assert eval (not renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.hit_test((1494,420),time.perf_counter()))
        assert eval (not renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.hit_test((1300,420),time.perf_counter()))
        screenshot "../../tmp/shooting-tests/monster-debug.png"
        keysym "K_d"
        assert eval (not renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].debug_enabled)
        click id "shooting_test_debug"
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].debug_enabled)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY)
        click id "shooting_test_back"
        pause until screen "main_menu" timeout 5

    testcase cached_animation_render_cadence:
        # Keep the one-time spawn/HUD interaction restart away from the two
        # synthetic mouse-motion events, then benchmark with the attack active.
        run Function(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.restart,delay=10)
        pause .6
        move pos (260,420)
        pause .3
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].gun_origin == (960,1080))
        assert eval (-12 <= renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].angle_to < -11.8)
        screenshot "../../tmp/shooting-tests/lean-left.png"
        move pos (1660,420)
        pause until eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].angle_to > 11.8) timeout 2
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].gun_origin == (960,1080))
        assert eval (11.8 < renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].angle_to <= 12)
        screenshot "../../tmp/shooting-tests/lean-right.png"
        move pos (960,420)
        pause .3
        run Function(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.restart)
        run setattr(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"], "profile_active", True)
        pause 1.0
        click id "shooting_test_fire"
        pause .46
        click id "shooting_test_reload"
        pause 2.0
        run setattr(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"], "profile_active", False)
        assert eval (len(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].profile_samples) >= 30)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].ammo == SHOOTING_TEST_CAPACITY)
        assert eval (renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].mode == "idle")
        run print(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].profile_report())
        click id "shooting_test_back"
        pause until screen "main_menu" timeout 5
