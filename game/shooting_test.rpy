# Isolated first-person animation sandbox. Launch with the menu entry or
# Start("shelter_shooting_test"); the story's start label is unchanged.
init python:
    import pygame
    import math

    SHOOTING_TEST_CAPACITY = 8
    SHOOTING_TEST_TARGETS = ((520, 420), (960, 360), (1370, 430))
    # Individual transparent PNGs, split before packaging; no runtime cropping.
    SHOOTING_TEST_FRAMES = [
        renpy.displayable("images/shooting_test/frames/handgun-%02d.png" % index)
        for index in range(20)
    ]
    renpy.music.register_channel("shooting_test_sfx", mixer="sfx", loop=False)

    class ShelterShootingSandbox(renpy.Displayable):
        shot_duration = 0.40
        reload_duration = 1.4

        def __init__(self, **kwargs):
            super(ShelterShootingSandbox, self).__init__(**kwargs)
            self.background = renpy.displayable("images/shooting_test/door.png")
            self.ammo = SHOOTING_TEST_CAPACITY
            self.shots = 0
            self.hits = 0
            self.target_index = 0
            self.aim = (960.0, 420.0)
            self.mode = "idle"
            self.started = 0.0
            self.next_shot = 0.0
            self.hit_until = 0.0
            self.empty_until = 0.0

        def visit(self):
            return [self.background] + SHOOTING_TEST_FRAMES

        def now(self):
            return renpy.get_game_runtime()

        def tick(self):
            if self.mode != "idle":
                elapsed = self.now() - self.started
                if self.mode == "fire" and elapsed >= self.shot_duration:
                    self.mode = "idle"
                elif self.mode == "reload" and elapsed >= self.reload_duration:
                    self.ammo = SHOOTING_TEST_CAPACITY
                    self.mode = "idle"
            renpy.redraw(self, 0)

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
            if (self.aim[0]-tx)**2 + (self.aim[1]-ty)**2 <= 39**2:
                self.hits += 1
                self.target_index = (self.target_index + 1) % len(SHOOTING_TEST_TARGETS)
                self.hit_until = now + .22
            renpy.music.play("audio/shooting_test/shot.wav", channel="shooting_test_sfx")
            renpy.redraw(self, 0)

        def reload(self):
            if self.mode != "idle" or self.ammo == SHOOTING_TEST_CAPACITY:
                return
            self.mode, self.started = "reload", self.now()
            self.empty_until = 0
            renpy.music.play("audio/shooting_test/reload.wav", channel="shooting_test_sfx")
            renpy.redraw(self, 0)

        def caption(self):
            if self.mode == "reload":
                return "Сум цэнэглэж байна…"
            if self.ammo == 0 or self.now() < self.empty_until:
                return "Сум дууслаа — R эсвэл «Цэнэглэх»"
            return "Цаасан байг онилоод дарж буудаарай"

        def render(self, width, height, st, at):
            result = renpy.Render(1920, 1080)
            result.blit(renpy.render(Transform(self.background, xysize=(1920,1080)),1920,1080,st,at),(0,0))
            canvas = result.canvas()
            tx, ty = SHOOTING_TEST_TARGETS[self.target_index]
            canvas.line((120,100,76,255),(tx,160),(tx,ty-58),2)
            canvas.rect((214,201,169,255),(tx-47,ty-58,94,116))
            for radius, color in ((39,(120,35,28,255)),(31,(220,207,176,255)),(23,(120,35,28,255)),(15,(220,207,176,255)),(7,(115,27,23,255))):
                canvas.circle(color,(tx,ty),radius)
            now = self.now()
            elapsed = max(0.0, now-self.started)
            frame = 0
            if self.mode == "fire":
                sequence = (2,3,4,5,6,7,8,9,0)
                frame = sequence[min(len(sequence)-1,int(elapsed/self.shot_duration*len(sequence)))]
            elif self.mode == "reload":
                sequence = (11,12,13,14,15,16,17,18,19)
                frame = sequence[min(len(sequence)-1,int(elapsed/self.reload_duration*len(sequence)))]
            gun = renpy.render(Transform(SHOOTING_TEST_FRAMES[frame], zoom=2.65),1920,1080,st,at)
            gw, gh = gun.get_size()
            # Align the idle sprite's muzzle horizontally with the aim point.
            gun_x = self.aim[0] - gw/2 - 50
            bob = math.sin(now*1.8)*2 if self.mode == "idle" else 0
            result.blit(gun,(gun_x,1080-gh+bob))
            reticle = renpy.Render(1920,1080)
            canvas = reticle.canvas()
            ax, ay = int(self.aim[0]), int(self.aim[1])
            color = (241,210,137,255) if now < self.hit_until else (236,226,202,255)
            for x1,y1,x2,y2 in ((ax-19,ay,ax-7,ay),(ax+7,ay,ax+19,ay),(ax,ay-19,ax,ay-7),(ax,ay+7,ax,ay+19)):
                canvas.line(color,(x1,y1),(x2,y2),2)
            canvas.circle((196,50,38,255),(ax,ay),2)
            if now < self.hit_until:
                for dx,dy in ((-1,-1),(-1,1),(1,-1),(1,1)):
                    canvas.line((236,185,88,255),(ax+dx*24,ay+dy*24),(ax+dx*32,ay+dy*32),3)
            result.blit(reticle,(0,0))
            renpy.redraw(self, 1.0/30.0)
            return result

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEMOTION and 110 < y < 860:
                self.aim = (min(1660,max(260,x)),min(670,max(170,y)))
                renpy.redraw(self,0)
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and 110 < y < 860:
                self.aim = (min(1660,max(260,x)),min(670,max(170,y)))
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
    add sandbox
    timer .03 repeat True action Function(sandbox.tick)
    add Solid("#080706bd") xysize (1920,112)
    text "БУУДЛАГЫН ТУРШИЛТ" font SHELTER_BOLD size 35 color "#e8dfca" xpos 64 ypos 22
    text "Оносон: [sandbox.hits]  ·  Буудсан: [sandbox.shots]" font SHELTER_FONT size 24 color "#cabb9d" xpos 65 ypos 68
    text "СУМ  [sandbox.ammo] / [SHOOTING_TEST_CAPACITY]" font SHELTER_BOLD size 38 color "#e8dfca" xanchor 1.0 xpos 1856 ypos 28
    text sandbox.caption() font SHELTER_FONT size 24 color "#e8dfca" xalign .5 ypos 127 outlines [(2,"#000c",0,1)]
    textbutton "Буцах":
        id "shooting_test_back"
        style "shooting_test_button"
        xpos 64 ypos 922 xsize 250
        action Return("exit")
    textbutton "Цэнэглэх · R":
        id "shooting_test_reload"
        style "shooting_test_button"
        xpos 1070 ypos 922
        action Function(sandbox.reload)
    textbutton "Буудах · Space":
        id "shooting_test_fire"
        style "shooting_test_button"
        xpos 1450 ypos 922
        action Function(sandbox.fire)
    text "Дэлгэц дээр дарж буудах · R — цэнэглэх · Esc — буцах" font SHELTER_FONT size 23 color "#dfd0b1" xalign .5 ypos 1036 outlines [(2,"#000c",0,1)]
    key "K_SPACE" action Function(sandbox.fire)
    key "K_r" action Function(sandbox.reload)
    key "game_menu" action Return("exit")
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    on "hide" action Stop("shooting_test_sfx")

label shelter_shooting_test:
    window hide None
    $ quick_menu = False
    $ _skipping = False
    $ renpy.block_rollback()
    stop music fadeout .25
    call screen shelter_shooting_sandbox
    $ renpy.music.stop(channel="shooting_test_sfx")
    return
