# Run with Ren'Py 8.5: test shelter_shooting_checks
init python:
    def _shelter_check_monster_zigzags(monster):
        polygon = SHOOTING_MONSTER_ROAD
        for route in range(3):
            for changes in (2,3):
                plan = monster.lane_plan(route,changes)
                assert len(plan)-1 == changes
                assert plan[-1][1] == route
                assert all(abs(a[1]-b[1]) == 1 for a,b in zip(plan,plan[1:]))
                previous_foot = -1
                for index in range(101):
                    x,foot,size = monster.geometry_at_progress(index/100.0,route,changes)
                    assert foot >= previous_foot
                    previous_foot = foot
                    assert 316-1e-6 <= foot-size <= 448+1e-6
                    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
                        assert (b[0]-a[0])*(foot-a[1])-(b[1]-a[1])*(x-a[0]) >= -1e-6
                x,foot,size = monster.geometry_at_progress(1,route,changes)
                assert x == SHOOTING_MONSTER_LANES_NEAR[route]
                assert foot == polygon[2][1] == polygon[3][1]
                assert foot-size == SHOOTING_MONSTER_NEAR_HEAD
                for phase,lane in plan[1:]:
                    before = monster.geometry_at_progress(phase-.00001,route,changes)
                    after = monster.geometry_at_progress(phase+.00001,route,changes)
                    assert max(abs(a-b) for a,b in zip(before,after)) < .2
        return True

    def _shelter_check_monster_arrival():
        monster = ShelterDoorMonster()
        monster.restart(route=1,changes=3)
        start = monster.approach_started
        monster.advance(start+monster.approach_duration-.001)
        assert monster.state == "approach" and monster.impacts == 0
        monster.advance(start+monster.approach_duration+.001)
        assert monster.state == "windup" and monster.impacts == 0
        assert monster.frame_at(start+monster.approach_duration+.01) == 8
        assert monster.geometry(start+monster.approach_duration)[1] == SHOOTING_MONSTER_ROAD[2][1]
        monster.advance(start+monster.approach_duration+monster.windup_duration+.001)
        assert monster.state == "strike" and monster.completed_changes == 3 and monster.impacts == 0
        return True

    def _shelter_check_alternating_strikes():
        monster = ShelterDoorMonster()
        monster.restart(route=1)
        monster.state = "strike"
        start = time.perf_counter()
        monster.strike_started = start
        monster.next_impact = start+.24
        assert monster.frame_at(start+.24) == 10
        assert monster.frame_at(start+.72) == 13
        assert monster.frame_at(start+1.20) == 10
        monster.advance(start+.239)
        assert monster.impacts == 0
        monster.advance(start+.241)
        assert monster.impacts == 1 and monster.last_impact_hand == "left"
        monster.advance(start+.721)
        assert monster.impacts == 2 and monster.last_impact_hand == "right"
        monster.advance(start+1.201)
        assert monster.impacts == 3 and monster.last_impact_hand == "left"
        renpy.music.stop(channel="shooting_test_monster")
        return True

    def _shelter_check_uninterrupted_hits():
        monster = ShelterDoorMonster()
        monster.restart(route=1,changes=3)
        monster.state = "approach"
        now = monster.approach_started+1.5
        before = monster.geometry(now)
        gait = monster.frame_at(now)
        start = monster.approach_started
        point = (before[0],before[1]-.6*before[2])
        monster.take_hit(now,point)
        assert monster.hp == 2 and monster.state == "approach"
        assert monster.approach_started == start and monster.geometry(now) == before
        assert monster.frame_at(now) == gait
        assert monster.geometry(now+.1)[1] > before[1]
        assert monster.blood_events[-1][1:3] == point
        monster.advance(now+SHOOTING_MONSTER_BLOOD_DURATION+.01)
        assert not monster.blood_events
        monster.restart(route=1)
        monster.state = "strike"
        monster.strike_started = now
        monster.next_impact = now+.24
        monster.take_hit(now+.10,point)
        assert monster.state == "strike" and monster.strike_started == now
        assert monster.next_impact == now+.24
        return True

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
        assert eval (len(SHOOTING_MONSTER_FRAMES) == 16)
        assert eval (_shelter_check_uninterrupted_hits())
        assert eval (len(SHOOTING_MONSTER_BLOOD_FRAMES) == 8 and all(renpy.loadable("images/shooting_test/blood/blood-%02d.png" % index) for index in range(8)))
        assert eval (_shelter_check_alternating_strikes())
        assert eval (all(renpy.loadable("images/shooting_test/monster/strike-%02d.png" % index) for index in range(8)))
        assert eval (not any(renpy.loadable("images/shooting_test/monster/monster-%02d.png" % index) for index in range(8,12)))
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
        pause .04
        assert eval (bool(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.blood_events))
        screenshot "../../tmp/shooting-tests/monster-blood.png"
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
        assert eval (_shelter_check_monster_zigzags(renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster))
        assert eval (_shelter_check_monster_arrival())
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
        assert eval (not renpy.get_screen("shelter_shooting_sandbox").scope["sandbox"].monster.hit_test((1100,420),time.perf_counter()))
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
