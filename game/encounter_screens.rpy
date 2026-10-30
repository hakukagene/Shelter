# Shared encounter UI: styles, the hold-to-skip control and every screen
# the encounter labels in shelter.rpy call.
define SHELTER_FONT = "fonts/RobotoCondensed-Regular.ttf"
define SHELTER_BOLD = "fonts/RobotoCondensed-Bold.ttf"

init 1 python:
    import math

    class ShelterSkipMouseArea(renpy.Displayable):
        """Handle hold events only inside Skip; never install global mouse keys."""
        def __init__(self, hovered, unhovered, pressed, released,
                    inside=False, active=False, **kwargs):
            super(ShelterSkipMouseArea, self).__init__(**kwargs)
            self.on_hover = hovered
            self.on_leave = unhovered
            self.on_press = pressed
            self.on_release = released
            self.inside = inside
            self.active = active

        def render(self, width, height, st, at):
            return renpy.Render(96, 96)

        def event(self, ev, x, y, st):
            import pygame
            if ev.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                return None
            inside = (x - 48) ** 2 + (y - 48) ** 2 <= 44 ** 2
            if not inside:
                if self.inside or self.active:
                    self.inside = False
                    self.active = False
                    renpy.run(self.on_leave)
                # Outside presses/releases belong to the other screen controls.
                return None
            if not self.inside:
                self.inside = True
                renpy.run(self.on_hover)
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.active = True
                renpy.run(self.on_press)
                raise renpy.IgnoreEvent()
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.active:
                self.active = False
                renpy.run(self.on_release)
                raise renpy.IgnoreEvent()
            return None

    class ShelterSkipRing(renpy.Displayable):
        """Clockwise hold progress and chevrons, drawn without raster assets."""
        def __init__(self, progress=0.0, **kwargs):
            super(ShelterSkipRing, self).__init__(**kwargs)
            self.progress = max(0.0, min(1.0, progress))

        def render(self, width, height, st, at):
            result = renpy.Render(64, 64)
            canvas = result.canvas()
            canvas.circle("#100e0de6", (32, 32), 29)
            canvas.circle("#514c3f", (32, 32), 27, 4)
            if self.progress > 0.0:
                steps = max(1, int(96 * self.progress))
                points = [(32 + 27 * math.cos(-math.pi / 2 + 2 * math.pi * self.progress * i / steps),
                        32 + 27 * math.sin(-math.pi / 2 + 2 * math.pi * self.progress * i / steps))
                        for i in range(steps + 1)]
                canvas.lines("#ffd38c", False, points, 4)
            canvas.lines("#e8dfca", False, [(22, 24), (30, 32), (22, 40)], 3)
            canvas.lines("#e8dfca", False, [(33, 24), (41, 32), (33, 40)], 3)
            return result

transform shelter_fade:
    alpha 0.0
    linear 0.2 alpha 1.0

transform shelter_tail_to_idle:
    alpha 1.0
    pause 0.07
    linear 0.18 alpha 0.0

style shelter_text is default:
    font SHELTER_FONT
    size 30
    color "#f2e9d9"
    outlines [(1, "#0009", 0, 1)]

style shelter_button is button:
    background Frame("gui/shelter/idle.png", 16, 16)
    hover_background Frame("gui/shelter/hover.png", 16, 16)
    insensitive_background Transform(Frame("gui/shelter/disabled.png", 16, 16), matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.15))
    padding (24, 16)

style shelter_button_text is shelter_text:
    hover_color "#ffd38c"
    insensitive_color "#777777"
    xalign 0.5
    yalign 0.5
    text_align 0.5

screen shelter_backdrop():
    add shelter_video_end(shelter_still) xysize (1920, 1080)


# Dialogue only skips after a deliberate one-second hold. Releasing or moving
# away early resets the progress, preventing accidental taps on mobile.
screen shelter_hold_skip(complete_action):
    default hold_hovered = False
    default hold_active = False
    default hold_progress = 0.0

    # The local displayable hit-tests every press/release. No global mouse
    # key bindings can remain active after the pointer leaves this control.
    timer 0.04 repeat True action If(
        hold_active,
        If(
            hold_progress >= 1.0,
            complete_action,
            SetLocalVariable("hold_progress", hold_progress + 0.04)),
        NullAction())

    fixed:
        id "shelter_hold_skip"
        xalign 0.975
        yalign 0.965
        xysize (96, 96)

        add Transform(ShelterSkipRing(hold_progress), zoom=1.5)
        add ShelterSkipMouseArea(
            inside=hold_hovered,
            active=hold_active,
            hovered=SetLocalVariable("hold_hovered", True),
            pressed=[SetLocalVariable("hold_hovered", True), SetLocalVariable("hold_active", True)],
            released=[SetLocalVariable("hold_active", False), SetLocalVariable("hold_progress", 0.0)],
            unhovered=[
                SetLocalVariable("hold_hovered", False),
                SetLocalVariable("hold_active", False),
                SetLocalVariable("hold_progress", 0.0)]) xysize (96, 96)



screen shelter_followup_question(caption):
    modal True
    use shelter_backdrop
    use shelter_actions(enabled=False)
    textbutton caption:
        style "shelter_button"
        text_style "shelter_button_text"
        text_size 27
        xalign 0.5
        ypos 670
        xysize (850, 112)
        action Return(True)
    use shelter_hold_skip(Return("skipped"))

screen shelter_playback(clip):
    modal True
    default elapsed = 0.0
    # Movie can briefly render transparent while its decoder changes state.
    # Keep a full-size poster underneath it, including during Dissolve.
    add shelter_movie_start_image(shelter_visitor, clip) xysize (1920, 1080)
    add shelter_movie_for(shelter_visitor, clip) xysize (1920, 1080)
    use shelter_actions(enabled=False, armed=shelter_clip_is_armed(clip))
    # Block click-to-dismiss and keyboard skipping while the clip plays.
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    $ speech_position = shelter_speech_position(clip)
    $ speech_window = shelter_data("windows").get(clip)
    if speech_window and speech_position is not None and speech_window[0] <= speech_position < speech_window[1]:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos shelter_data("subtitle_y")
            xsize 1344
            padding (35, 22)
            text shelter_data("lines")[clip] style "shelter_text" size shelter_data("subtitle_size") xalign 0.5 text_align 0.5
    # A short startup grace avoids interpreting a not-yet-started decoder as EOF.
    # Actual playback completion, rather than a fixed timer, drives progression.
    timer 0.03 repeat True action If(renpy.get_screen("shelter_protocol"), NullAction(), If(
        elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_video"),
        Return(True), SetScreenVariable("elapsed", elapsed + 0.03)))
    use shelter_hold_skip([Stop("shelter_video"), Return("skipped")])
    use shelter_protocol_button

# Both native and HTML playback land on the same decoded end frame first.
# Then only conversational/armed clips blend to their stable waiting pose.
screen shelter_clip_handoff(clip):
    modal True
    $ terminal = shelter_clip_is_terminal(clip)
    use shelter_backdrop
    if not terminal:
        add shelter_movie_frame(shelter_visitor, clip, "end") xysize (1920, 1080) at shelter_tail_to_idle
    use shelter_actions(enabled=False, armed=shelter_clip_is_armed(clip))
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    key "game_menu" action NullAction()
    if renpy.emscripten:
        # Paint this canvas before hiding the HTML video overlay.
        timer 0.03 action Function(shelter_web_close)
    timer (0.12 if terminal else 0.26) action Return(True)

# Armed mode offers exactly two actions; aiming lives in the question row.
screen shelter_actions(enabled=True, armed=False):
    hbox:
        xalign 0.5
        ypos 880
        spacing 24
        $ choices = shelter_action_choices(armed)
        for caption, result, icon in choices:
            button:
                xysize (180, 180)
                padding (0, 0)
                # Dim the complete action (icon and caption) while playback
                # keeps it visible but unavailable.
                at Transform(alpha=(1.0 if enabled else 0.5))
                background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180))
                hover_background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180), matrixcolor=BrightnessMatrix(0.14))
                insensitive_background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180), matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.22))
                focus_mask True
                sensitive enabled
                action [Function(shelter_hold_current_frame), Return(result)]
                text caption:
                    font SHELTER_BOLD
                    size 15
                    color "#f4dfaf"
                    hover_color "#ffffff"
                    insensitive_color "#777777"
                    xalign 0.5
                    ypos 107
                    xsize 118
                    text_align 0.5
                    outlines [(1, "#000b", 0, 1)]

# Player speaks over the waiting portrait; the visitor responds only after EOF.
screen shelter_player_speech(voice_key, caption=None):
    modal True
    default elapsed = 0.0
    use shelter_backdrop
    use shelter_actions(enabled=False)
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    on "hide" action Stop("shelter_player")
    $ position = renpy.music.get_pos(channel="shelter_player")
    $ cue = shelter_player_voice(voice_key)
    if caption and position is not None and cue[1] <= position < cue[2]:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos 710
            xsize 1344
            padding (35, 22)
            text caption style "shelter_text" text_align 0.5 xalign 0.5
    timer 0.03 repeat True action If(renpy.get_screen("shelter_protocol"), NullAction(), If(
        elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_player"),
        Return(True), SetScreenVariable("elapsed", elapsed + 0.03)))
    use shelter_hold_skip([Stop("shelter_player"), Return("skipped")])
    use shelter_protocol_button

screen shelter_question_choices():
    hbox:
        xalign 0.5
        ypos 655
        spacing 16
        for index, question in enumerate(shelter_data("questions")):
            textbutton question:
                style "shelter_button"
                text_style "shelter_button_text"
                text_size (30 if renpy.variant("web") else 26)
                text_text_align 0.5
                xysize (330, 170)
                sensitive index not in shelter_asked or shelter_has_inspection(shelter_visitor, index)
                action [Function(shelter_hold_current_frame), Return(index)]
        textbutton "Буу онилох":
            style "shelter_button"
            text_style "shelter_button_text"
            text_size (30 if renpy.variant("web") else 26)
            xysize (330, 170)
            sensitive shelter_can_aim()
            action [Function(shelter_hold_current_frame), Return("aim")]

screen shelter_questions():
    modal True
    use shelter_backdrop
    use shelter_actions
    use shelter_question_choices
    use shelter_protocol_button


screen shelter_decision(armed=False):
    modal True
    use shelter_backdrop
    use shelter_actions(armed=armed)
    if not armed and shelter_can_ask_questions():
        use shelter_question_choices
    use shelter_protocol_button


screen shelter_anu_admission():
    # Compatibility for saves made while the old admission placeholder was open.
    modal True
    add shelter_movie_frame("anu", "admit", "end") xysize (1920, 1080)
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    timer 1.2 action Return(True)

# Concept 01: live text and actions over the text-free lockdown artwork.
screen shelter_result(title, description):
    modal True
    on "show" action Play("music", "<volume 0.50>audio/Audio/menu2.mp3", loop=True, fadeout=0.6, fadein=0.8)
    add "gui/shelter/ending/lockdown.jpg" xysize (1920, 1080)
    text title:
        style "shelter_text"
        font SHELTER_BOLD
        size 54
        xalign 0.5
        ypos 393
        xsize 1160
        text_align 0.5
    # Hit areas match the two physical plates in the background.
    for caption, result, left in [("Дахин тоглох", "replay", 580), ("Үндсэн цэс", "menu", 1025)]:
        button:
            xpos left
            ypos 645
            xysize (384, 145)
            padding (0, 0)
            background None
            hover_background Solid("#ffd6a01c")
            action Return(result)
            text caption:
                font SHELTER_FONT
                size 34
                color "#f2e9d9"
                hover_color "#ffffff"
                outlines [(1, "#0009", 0, 1)]
                xpos 120
                yalign 0.5

# Unskippable story-time card, followed by the supplied metal-door recording.
screen shelter_next_visitor_card():
    modal True
    use shelter_transition_status
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    on "hide" action Stop("shelter_knock")
    timer 2.0 action Play("shelter_knock", "audio/Audio/door .wav", loop=False)
    # Allow the full supplied 2.20-second knock before the visitor fades in.
    timer 4.5 action Return(True)
