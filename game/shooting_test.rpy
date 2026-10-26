# Isolated first-person animation sandbox. Launch with the menu entry or
# Start("shelter_shooting_test"); the story's start label is unchanged.
init python:
    import pygame
    import math
    import time

    SHOOTING_TEST_CAPACITY = 7
    SHOOTING_TEST_RELOAD_FPS = 25
    SHOOTING_TEST_RELOAD_DURATION = 1.8
    SHOOTING_TEST_RELOAD_FRAME_COUNT = 45
    SHOOTING_TEST_RELOAD_FRAMES = tuple("reload-%02d" % index for index in range(45))
    SHOOTING_TEST_POSES = ("idle",) + tuple("fire-%02d" % index for index in range(10)) + SHOOTING_TEST_RELOAD_FRAMES
    SHOOTING_TEST_GUN_CANVAS = (1200,1000)
    SHOOTING_TEST_GUN_ANCHOR = .656
    SHOOTING_TEST_TARGETS = ((520, 420), (960, 360), (1370, 430))
    # The legacy eight-pose folder is no longer a runtime asset source.
    SHOOTING_TEST_FRAMES = [
        Transform("images/shooting_test/sequence/%s.png" % pose, xysize=SHOOTING_TEST_GUN_CANVAS)
        for pose in SHOOTING_TEST_POSES
    ]
    SHOOTING_TEST_BACKGROUND = Transform("images/shooting_test/door.png", xysize=(1920, 1080))
    renpy.music.register_channel("shooting_test_sfx", mixer="sfx", loop=False)

    class ShelterShootingMark(renpy.Displayable):
        """Small static textures, cached by Ren'Py instead of full-screen canvases."""
        def __init__(self, kind, **kwargs):
            super(ShelterShootingMark, self).__init__(**kwargs)
            self.kind = kind

        def render(self, width, height, st, at):
            result = renpy.Render(128, 128)
            canvas = result.canvas()
            if self.kind == "target":
                canvas.rect((214,201,169,255),(17,6,94,116))
                for radius, color in ((39,(120,35,28,255)),(31,(220,207,176,255)),(23,(120,35,28,255)),(15,(220,207,176,255)),(7,(115,27,23,255))):
                    canvas.circle(color,(64,64),radius)
            else:
                color = (241,210,137,255) if self.kind == "hit" else (236,226,202,255)
                for x1,y1,x2,y2 in ((45,64,57,64),(71,64,83,64),(64,45,64,57),(64,71,64,83)):
                    canvas.line(color,(x1,y1),(x2,y2),2)
                canvas.circle((196,50,38,255),(64,64),2)
                if self.kind == "hit":
                    for dx,dy in ((-1,-1),(-1,1),(1,-1),(1,1)):
                        canvas.line((236,185,88,255),(64+dx*24,64+dy*24),(64+dx*32,64+dy*32),3)
            return result

    class ShelterShootingGun(renpy.Displayable):
        def __init__(self,owner):
            super(ShelterShootingGun,self).__init__()
            self.owner = owner

        def visit(self):
            return SHOOTING_TEST_FRAMES

        def render(self,width,height,st,at):
            elapsed = max(0,self.owner.now()-self.owner.started)
            w,h = SHOOTING_TEST_GUN_CANVAS
            result = renpy.Render(w,h)
            result.blit(renpy.render(SHOOTING_TEST_FRAMES[self.owner.frame_at(elapsed)],w,h,st,at),(0,0))
            renpy.redraw(self,self.owner.animation_redraw_delay(elapsed))
            return result

    class ShelterShootingSandbox(renpy.Displayable):
        shot_duration = 0.40
        reload_duration = SHOOTING_TEST_RELOAD_DURATION

        def __init__(self, **kwargs):
            super(ShelterShootingSandbox, self).__init__(**kwargs)
            self.background = SHOOTING_TEST_BACKGROUND
            self.monster = ShelterDoorMonster()
            self.monster_window = AlphaMask(self.monster,ShelterMonsterPaneMask())
            self.debug_enabled = True
            self.debug_road = ShelterMonsterDebugRoad(self.monster)
            self.target_art = ShelterShootingMark("target")
            self.crosshair = ShelterShootingMark("crosshair")
            self.hit_mark = ShelterShootingMark("hit")
            self.wires = [Solid("#78644c", xysize=(2, ty-218)) for tx, ty in SHOOTING_TEST_TARGETS]
            self.ammo = SHOOTING_TEST_CAPACITY
            self.shots = 0
            self.hits = 0
            self.target_index = 0
            self.aim = (960.0, 420.0)
            self.angle_from = self.angle_to = 0.0
            self.angle_started = 0.0
            self.gun_origin = (960,1080)
            self.gun = Transform(ShelterShootingGun(self),xpos=960,ypos=1080,
                                xanchor=.5,yanchor=SHOOTING_TEST_GUN_ANCHOR,
                                transform_anchor=True,function=self.gun_transform)
            self.mode = "idle"
            self.started = 0.0
            self.next_shot = 0.0
            self.hit_until = 0.0
            self.empty_until = 0.0
            # Enabled only by the diagnostic test; no sampling in normal play.
            self.profile_active = False
            self.profile_samples = []

        def visit(self):
            return [self.background,self.monster_window,self.debug_road,self.target_art,self.crosshair,self.hit_mark,self.gun] + self.wires

        def now(self):
            # get_game_runtime only advances when an interaction ends; a custom
            # displayable needs a continuously advancing clock within it.
            return time.perf_counter()

        def toggle_debug(self):
            self.debug_enabled = not self.debug_enabled
            renpy.redraw(self,0)

        def angle_at(self,now):
            return self.angle_to+(self.angle_from-self.angle_to)*math.exp(-18*max(0,now-self.angle_started))

        def set_aim(self,x,y):
            now = self.now()
            self.angle_from = self.angle_at(now)
            self.aim = (min(1660,max(260,x)),min(670,max(170,y)))
            self.angle_to = (self.aim[0]-960)/700.0*12
            self.angle_started = now
            renpy.redraw(self.gun,0)
            renpy.redraw(self,0)

        def gun_transform(self,transform,st,at):
            now = self.now()
            elapsed = max(0,now-self.started)
            if self.mode in ("reload","fire"):
                now = self.started+self.reload_frame_index(elapsed)/25.0
            transform.rotate = self.angle_at(now)
            return self.animation_redraw_delay(elapsed)

        def reload_frame_index(self,elapsed):
            return max(0,min(44,int(math.floor(max(0,elapsed)*25+1e-8))))

        def animation_redraw_delay(self,elapsed):
            duration = self.reload_duration if self.mode == "reload" else self.shot_duration
            if self.mode in ("reload","fire") and elapsed < duration:
                return max(.001,(self.reload_frame_index(elapsed)+1)/25.0-elapsed)
            return 1.0/60.0

        def tick(self):
            if self.monster.advance(self.now()):
                renpy.restart_interaction()
            renpy.timeout(.04)
            if self.mode != "idle":
                elapsed = self.now() - self.started
                if self.mode == "fire" and elapsed >= self.shot_duration:
                    self.mode = "idle"
                    renpy.restart_interaction()
                elif self.mode == "reload" and elapsed >= self.reload_duration:
                    self.ammo = SHOOTING_TEST_CAPACITY
                    self.mode = "idle"
                    renpy.restart_interaction()
                else:
                    duration = self.shot_duration if self.mode == "fire" else self.reload_duration
                    renpy.timeout(max(.001, duration-elapsed))

        def fire(self):
            now = self.now()
            if self.mode != "idle" or now < self.next_shot:
                return
            if self.ammo == 0:
                self.next_shot = now + .25
                self.empty_until = now + 1.0
                renpy.music.play("audio/shooting_test/empty.wav", channel="shooting_test_sfx")
                return
            self.ammo -= 1
            self.shots += 1
            self.mode, self.started = "fire", now
            self.next_shot = now + .43
            self.empty_until = 0
            tx, ty = SHOOTING_TEST_TARGETS[self.target_index]
            if self.monster.hit_test(self.aim,now):
                self.monster.take_hit(now)
                self.hits += 1
                self.hit_until = now+.22
            elif (self.aim[0]-tx)**2 + (self.aim[1]-ty)**2 <= 39**2:
                self.hits += 1
                self.target_index = (self.target_index + 1) % len(SHOOTING_TEST_TARGETS)
                self.hit_until = now + .22
            renpy.music.play("audio/shooting_test/shot.wav", channel="shooting_test_sfx")
            renpy.timeout(self.shot_duration)
            renpy.restart_interaction()
            renpy.redraw(self, 0)

        def reload(self):
            if self.mode != "idle" or self.ammo == SHOOTING_TEST_CAPACITY:
                return
            self.mode, self.started = "reload", self.now()
            self.empty_until = 0
            renpy.music.play("audio/shooting_test/reload.wav", channel="shooting_test_sfx")
            renpy.timeout(self.reload_duration)
            renpy.restart_interaction()
            renpy.redraw(self, 0)

        def frame_at(self, elapsed, mode=None):
            mode = self.mode if mode is None else mode
            if mode == "fire":
                return 1+min(9,max(0,int(math.floor(max(0,elapsed)*25+1e-8)))) if elapsed < self.shot_duration else 0
            if mode == "reload":
                return 11+self.reload_frame_index(elapsed) if elapsed < self.reload_duration else 0
            return 0

        def profile_report(self):
            samples = self.profile_samples[5:]
            intervals = sorted(b[0]-a[0] for a, b in zip(samples, samples[1:]) if b[0]-a[0] > .001)
            if not intervals:
                return "No render samples"
            return "Shooting render cadence: %.1f Hz; p95 interval %.2f ms; mean CPU render %.3f ms (%d frames)" % (
                len(intervals)/sum(intervals), intervals[int((len(intervals)-1)*.95)]*1000,
                sum(s[1] for s in samples)/len(samples)*1000, len(samples))

        def caption(self):
            if self.mode == "reload":
                return "Сум цэнэглэж байна…"
            if self.ammo == 0 or self.now() < self.empty_until:
                return "Сум дууслаа — R эсвэл «Цэнэглэх»"
            if self.monster.state == "strike":
                return "Мангас хаалга цохиж байна — онилоод буудаарай!"
            if self.monster.state == "approach":
                return "Мангас ойртож байна!"
            return "Цаасан байг онилоод дарж буудаарай"

        def render(self, width, height, st, at):
            render_started = time.perf_counter() if self.profile_active else 0
            result = renpy.Render(1920, 1080)
            world = renpy.Render(1920,1080)
            background = renpy.render(self.background,1920,1080,st,at)
            world.blit(background,(0,0))
            world.blit(renpy.render(self.monster_window,1920,1080,st,at),(0,0))
            tx, ty = SHOOTING_TEST_TARGETS[self.target_index]
            world.blit(renpy.render(self.wires[self.target_index],2,500,st,at),(tx,160))
            world.blit(renpy.render(self.target_art,128,128,st,at),(tx-64,ty-64))
            now = self.now()
            if self.debug_enabled:
                world.blit(renpy.render(self.debug_road,1920,1080,st,at),(0,0))
                debug_hitbox = self.monster.debug_render(now)
                if debug_hitbox:
                    world.blit(*debug_hitbox)
            if now < self.monster.impact_until:
                force = (self.monster.impact_until-now)/.16
                offset = (math.sin(now*95)*5*force,math.cos(now*110)*3*force)
                result.blit(background,(0,0))
                result.blit(world,offset)
            else:
                result.blit(world,(0,0))
            result.place(self.gun,st=st,at=at)
            ax, ay = int(self.aim[0]), int(self.aim[1])
            mark = self.hit_mark if now < self.hit_until else self.crosshair
            result.blit(renpy.render(mark,128,128,st,at),(ax-64,ay-64))
            renpy.redraw(self, 1.0/60.0)
            if self.profile_active:
                self.profile_samples.append((render_started, time.perf_counter()-render_started))
            return result

        def event(self, ev, x, y, st):
            # Finish state transitions at their deadline, without a repeating
            # screen timer/restart 33 times a second. Animation uses elapsed time.
            if ev.type == pygame.MOUSEMOTION and 110 < y < 860:
                self.set_aim(x,y)
            self.tick()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and 110 < y < 860:
                self.set_aim(x,y)
                self.fire()
                raise renpy.IgnoreEvent()

style shooting_test_button is button:
    background Frame("gui/shelter/metal/button.png",28,18)
    hover_background Frame("gui/shelter/metal/selected.png",28,18)
    padding (20,12)
    xysize (340,80)

style shooting_test_button_text is shelter_text:
    font SHELTER_BOLD
    size 28
    xalign 0.5
    yalign 0.5

screen shelter_shooting_sandbox():
    modal True
    default sandbox = ShelterShootingSandbox()
    on "show" action Function(sandbox.tick,_update_screens=False)
    add sandbox
    add Solid("#080706bd") xysize (1920,112)
    text "БУУДЛАГЫН ТУРШИЛТ" font SHELTER_BOLD size 35 color "#e8dfca" xpos 64 ypos 22
    text "Оносон: [sandbox.hits]  ·  Буудсан: [sandbox.shots]" font SHELTER_FONT size 24 color "#cabb9d" xpos 65 ypos 68
    text "Мангас: [sandbox.monster.hp]/3 · Хаалга цохисон: [sandbox.monster.impacts] · Устгасан: [sandbox.monster.kills]" font SHELTER_FONT size 24 color "#cabb9d" xpos 700 ypos 68
    text "СУМ  [sandbox.ammo] / [SHOOTING_TEST_CAPACITY]" font SHELTER_BOLD size 38 color "#e8dfca" xanchor 1.0 xpos 1856 ypos 28
    text sandbox.caption() font SHELTER_FONT size 24 color "#e8dfca" xalign .5 ypos 127 outlines [(2,"#000c",0,1)]
    textbutton ("Debug: АСААЛТТАЙ · D" if sandbox.debug_enabled else "Debug: УНТРААЛТТАЙ · D"):
        id "shooting_test_debug"
        style "shooting_test_button"
        xpos 1530 ypos 610 ysize 60
        action Function(sandbox.toggle_debug)
    if sandbox.debug_enabled:
        text "DEBUG · D\nНогоон: явах хүрээ\nЦэнхэр: 3 чиглэл\nШар: оногдох талбай\nУлаан: нийт hitbox" font SHELTER_FONT size 23 color "#e8dfca" xpos 64 ypos 732 outlines [(2,"#000c",0,1)]
    textbutton "Буцах":
        id "shooting_test_back"
        style "shooting_test_button"
        xpos 64 ypos 922 xsize 250
        action [Stop("shooting_test_sfx"),Stop("shooting_test_monster"),Return("exit")]
    textbutton "Дахин дайруулах · T":
        id "shooting_test_monster_restart"
        style "shooting_test_button"
        xpos 1530 ypos 730
        action Function(sandbox.monster.restart)
    text "Чиглэл: [SHOOTING_MONSTER_ROUTE_NAMES[sandbox.monster.route_index]]" font SHELTER_FONT size 24 color "#cabb9d" xpos 1530 ypos 684
    textbutton "Цэнэглэх · R":
        id "shooting_test_reload"
        style "shooting_test_button"
        xpos 1530 ypos 830
        action Function(sandbox.reload)
    textbutton "Буудах · Space":
        id "shooting_test_fire"
        style "shooting_test_button"
        xpos 1530 ypos 930
        action Function(sandbox.fire)
    text "Дэлгэц дээр дарж буудах · R — цэнэглэх · Esc — буцах" font SHELTER_FONT size 23 color "#dfd0b1" xalign .5 ypos 1036 outlines [(2,"#000c",0,1)]
    key "K_SPACE" action Function(sandbox.fire)
    key "K_r" action Function(sandbox.reload)
    key "K_t" action Function(sandbox.monster.restart)
    key "K_d" action Function(sandbox.toggle_debug)
    key "game_menu" action [Stop("shooting_test_sfx"),Stop("shooting_test_monster"),Return("exit")]
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    on "hide" action [Stop("shooting_test_sfx"),Stop("shooting_test_monster")]

label shelter_shooting_test:
    window hide None
    $ quick_menu = False
    $ _skipping = False
    $ renpy.block_rollback()
    stop music fadeout .25
    $ renpy.start_predict(*SHOOTING_TEST_FRAMES)
    $ renpy.start_predict(*SHOOTING_MONSTER_FRAMES)
    $ renpy.start_predict(SHOOTING_TEST_BACKGROUND)
    $ renpy.pause(predict=True)
    call screen shelter_shooting_sandbox
    $ renpy.stop_predict(*SHOOTING_TEST_FRAMES)
    $ renpy.stop_predict(*SHOOTING_MONSTER_FRAMES)
    $ renpy.stop_predict(SHOOTING_TEST_BACKGROUND)
    $ renpy.music.stop(channel="shooting_test_sfx")
    $ renpy.music.stop(channel="shooting_test_monster")
    return
