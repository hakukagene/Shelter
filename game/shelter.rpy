# Video-driven encounter using the supplied VP9/Opus WebM assets.
define SHELTER_FONT = "fonts/RobotoCondensed-Regular.ttf"
define SHELTER_BOLD = "fonts/RobotoCondensed-Bold.ttf"

default shelter_still = "intro"
default shelter_asked = []
default shelter_choice = None
# Keep Maral as the default for saves made before the two-visitor sequence.
default shelter_visitor = "Maral"
default shelter_chinba_outcome = None
# The supplied Bayra aim movie ends with one black frame after speech.
# Stop before that frame; keep the original source and audio untouched.
define SHELTER_CLIP_STARTS = {
    "margad/answer1_part2": 13.140,
    "margad/answer1_part3": 17.740,
}
define SHELTER_CLIP_ENDS = {
    "Bayra/aim": 13.11,
    "margad/answer1": 11.525,
    "margad/answer1_part2": 16.414,
    "margad/answer1_part3": 22.040,
}

# Append unique IDs and civilian classifications as new visitors are added.
define SHELTER_CIVILIAN_COUNT = 43
define SHELTER_MONSTER_COUNT = 30
define SHELTER_TOTAL_VISITORS = SHELTER_CIVILIAN_COUNT + SHELTER_MONSTER_COUNT
define SHELTER_CIVILIAN_TARGET = 40
define SHELTER_MAX_CIVILIAN_DEATHS = 2
define SHELTER_MAX_CIVILIAN_MISTAKES = 2
# Available roster, also the original sequence for saves predating random order.
define SHELTER_VISITOR_ORDER = ("Chinba", "Maral", "Swat", "Bayra", "anu", "deeremchin", "ganba", "ganzo", "naraa", "margad", "undral")
default shelter_run_order = None
define SHELTER_CIVILIANS = {"Chinba": True, "Maral": False, "Swat": True, "Bayra": True, "anu": False, "ganba": True, "ganzo": True, "naraa": True, "margad": False, "undral": False}
# Armor stops the bullet: Orgil leaves alive after being shot.
define SHELTER_NONLETHAL_SHOOT = ("Swat",)
default shelter_outcomes = {}
default shelter_admitted = 0
default shelter_civilians_saved = 0
default shelter_civilians_killed = 0
default shelter_visitors_seen = 0
# None gives older saves a stable time derived from their completed visits.
default shelter_story_minutes = None

define SHELTER_CLOCK_START = 23 * 60 + 10

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

    renpy.music.register_channel("shelter_knock", mixer="sfx", loop=False, stop_on_mute=False)

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

    SHELTER_VISITORS = {
        "undral": {"clips": UNDRAL_CLIPS, "questions": UNDRAL_QUESTIONS,
                "lines": UNDRAL_LINES, "windows": UNDRAL_SPEECH_WINDOWS, "voices": {}},
        "margad": {"clips": MARGAD_CLIPS, "questions": MARGAD_QUESTIONS,
                "lines": MARGAD_LINES, "windows": MARGAD_SPEECH_WINDOWS,
                "voices": MARGAD_SUPPLIED_PLAYER_VOICES},
        "naraa": {"clips": NARAA_CLIPS, "questions": NARAA_QUESTIONS,
                "lines": NARAA_LINES, "windows": NARAA_SPEECH_WINDOWS, "voices": {}},
        "ganzo": {"clips": GANZO_CLIPS, "questions": GANZO_QUESTIONS,
                "lines": GANZO_LINES, "windows": GANZO_SPEECH_WINDOWS, "voices": {}},
        "ganba": {"clips": GANBA_CLIPS, "questions": GANBA_QUESTIONS,
                "lines": GANBA_LINES, "windows": GANBA_SPEECH_WINDOWS, "voices": {}},
        "deeremchin": {"clips": DEEREMCHIN_CLIPS, "questions": DEEREMCHIN_QUESTIONS,
                "lines": DEEREMCHIN_LINES, "windows": DEEREMCHIN_SPEECH_WINDOWS,
                "voices": DEEREMCHIN_PLAYER_VOICES},
        "anu": {"clips": ANU_CLIPS, "questions": ANU_QUESTIONS,
                "lines": ANU_LINES, "windows": ANU_SPEECH_WINDOWS, "voices": {}},
        "Bayra": {"clips": BAYRA_CLIPS, "questions": BAYRA_QUESTIONS,
                "lines": BAYRA_LINES, "windows": BAYRA_SPEECH_WINDOWS, "voices": BAYRA_PLAYER_VOICES},
        "Swat": {"clips": SWAT_CLIPS, "questions": SWAT_QUESTIONS,
                "lines": SWAT_LINES, "windows": SWAT_SPEECH_WINDOWS, "voices": {}},
        "Maral": {"clips": SHELTER_CLIPS, "questions": SHELTER_QUESTIONS,
                "lines": SHELTER_LINES, "windows": SHELTER_SPEECH_WINDOWS,
                "voices": SHELTER_PLAYER_VOICES},
        "Chinba": {"clips": CHINBA_CLIPS, "questions": CHINBA_QUESTIONS,
                "lines": CHINBA_LINES, "windows": CHINBA_SPEECH_WINDOWS,
                "voices": CHINBA_PLAYER_VOICES},
    }

    def shelter_make_visitor_order():
        # Shuffle once per new game/replay, using Ren'Py's rollback-aware RNG.
        order = list(SHELTER_VISITOR_ORDER)
        renpy.random.shuffle(order)
        return order

    def shelter_next_visitor_id():
        # Old saves keep their original remaining sequence. Never reshuffle on
        # load, during a movie, or while displaying the clock between visitors.
        order = shelter_run_order or SHELTER_VISITOR_ORDER
        remaining = order[order.index(shelter_visitor) + 1:]
        return next((visitor for visitor in remaining if visitor not in shelter_outcomes), None)

    def shelter_clock_minutes():
        if shelter_story_minutes is None:
            return SHELTER_CLOCK_START + 7 * shelter_visitors_seen
        return shelter_story_minutes

    def shelter_clock_text():
        minutes = shelter_clock_minutes() % (24 * 60)
        return "%02d:%02d" % (minutes // 60, minutes % 60)

    def shelter_killed_total():
        # Total fatal shots, including monsters, for encounter bookkeeping.
        # The ledger displays shelter_civilians_killed instead. Orgil survives.
        return sum(choice == "shoot" and visitor not in SHELTER_NONLETHAL_SHOOT
                for visitor, choice in shelter_outcomes.items()) + sum(
                    choice == "shoot" for choice in shelter_deeremchin_outcomes.values())

    def shelter_record_outcome(visitor, choice):
        # Copy-on-write supports saves/rollback; one outcome per visitor.
        global shelter_outcomes, shelter_admitted, shelter_civilians_saved
        global shelter_civilians_killed, shelter_visitors_seen, shelter_story_minutes
        if visitor in shelter_outcomes:
            return
        allowed = ("admit", "reject", "shoot_man", "shoot_woman") if visitor == "deeremchin" else ("admit", "reject", "shoot")
        if choice not in allowed:
            raise ValueError("Not a final decision: " + str(choice))
        # Advance once per resolved visitor, never during screen prediction or
        # redraw. Ren'Py saves/rolls back both this value and its random state.
        elapsed = 7 if shelter_visitors_seen == 0 else renpy.random.randint(4, 9)
        shelter_story_minutes = shelter_clock_minutes() + elapsed
        shelter_outcomes = dict(shelter_outcomes, **{visitor: choice})
        if visitor == "deeremchin":
            shelter_visitors_seen += 2
            shelter_finish_deeremchin(choice)
            return
        civilian = SHELTER_CIVILIANS[visitor]
        shelter_visitors_seen += 1
        if choice == "admit":
            shelter_admitted += 1
            if civilian:
                shelter_civilians_saved += 1
        elif choice == "shoot" and civilian and visitor not in SHELTER_NONLETHAL_SHOOT:
            shelter_civilians_killed += 1

    def shelter_civilians_rejected():
        # Derive from saved outcomes: includes armored Orgil leaving after a
        # nonlethal shot and the civilian man lost when the pair is expelled.
        # Monsters and admitted civilians never enter this count.
        rejected = sum(SHELTER_CIVILIANS.get(visitor, False) and
            (choice == "reject" or (choice == "shoot" and visitor in SHELTER_NONLETHAL_SHOOT))
            for visitor, choice in shelter_outcomes.items())
        rejected += shelter_deeremchin_outcomes.get("man") in ("reject", "lost")
        return rejected

    def shelter_civilian_mistakes():
        return shelter_civilians_killed + shelter_civilians_rejected()

    def shelter_campaign_status():
        if shelter_civilian_mistakes() > SHELTER_MAX_CIVILIAN_MISTAKES:
            return "casualties"
        if shelter_civilians_saved >= SHELTER_CIVILIAN_TARGET:
            return "win"
        if shelter_visitors_seen >= SHELTER_TOTAL_VISITORS:
            return "shortfall"
        return "continue"

    def shelter_data(key):
        return SHELTER_VISITORS[shelter_visitor][key]

    renpy.music.register_channel("shelter_player", mixer="voice", loop=False, stop_on_mute=False)
    # Muting dialogue must silence the soundtrack, not stop/skip the movie.
    # Movie channels must not pre-buffer the next file like audio-only channels.
    renpy.music.register_channel(
        "shelter_video", mixer="voice", loop=False, movie=True,
        stop_on_mute=False, buffer_queue=False)
    def shelter_wait_image(clip, visitor=None):
        visitor = visitor or shelter_visitor
        if visitor == "margad":
            # Preserve the exact pose across the two player interjections.
            if clip in ("answer1", "answer1_part2"):
                return shelter_movie_frame(visitor, clip, "end")
            if clip in ("intro", "answer1_part3", "answer2", "answer3", "lower"):
                return shelter_movie_frame(visitor, "answer1", "start")
            return shelter_movie_frame(visitor, clip, "end")
        if visitor == "undral":
            return shelter_undral_poster(clip)
        if visitor == "naraa":
            return shelter_naraa_poster(clip)
        if visitor in ("ganba", "ganzo"):
            if clip in ("intro", "answer1", "answer2", "answer3", "lower"):
                return shelter_movie_frame(visitor, "answer1", "start")
            return shelter_movie_frame(visitor, clip, "end")
        if visitor == "deeremchin":
            # Match the actual video framing; never reintroduce a shot person.
            if clip in ("aim", "shoot_man", "shoot_woman") or shelter_clip_is_terminal(clip):
                return shelter_movie_frame(visitor, clip, "end")
            return shelter_movie_frame(visitor, "answer3", "start")
        # Maral's answer1 still is a close-up. Keep the doorway framing fixed
        # between questions, including old saves that stopped on that answer.
        if visitor == "Maral" and clip in ("intro", "answer1", "answer2", "answer3", "lower"):
            return "images/Maral/frames/intro.jpg"
        if visitor in ("Bayra", "anu"):
            if clip in ("intro", "answer1", "answer2", "answer3", "lower"):
                clip = "idle"
            # Old Bayra saves can still contain split-clip still names.
            clip = {"arrival": "arrival_start", "enter": "admit", "leave": "reject"}.get(clip, clip)
            return "images/" + visitor + "/frames/" + clip + ".jpg"
        if visitor == "Swat":
            if clip in ("intro", "answer1", "answer2", "answer3", "lower"):
                clip = "idle"
            return "images/Swat/frames/" + clip + ".jpg"
        # Reference-matched frames extracted from the source videos (not the supplied PNGs).
        # idle: Chinbaa hariult 3, first frame; aim: Chinbaa buuduulah, first frame.
        # Keep the same neutral pose for every unarmed question/waiting state.
        if visitor == "Chinba" and clip in ("intro", "answer1", "answer2", "answer3", "lower"):
            return "images/Chinba/frames/idle.jpg"
        allowed = ("intro", "answer1", "answer2", "answer3", "aim", "lower")
        if visitor == "Chinba":
            allowed += ("arrival", "shoot", "admit", "reject")
        if clip not in allowed:
            clip = "intro"
        return "images/" + visitor + "/frames/" + clip + ".jpg"

    def shelter_video_end(clip, visitor=None):
        visitor = visitor or shelter_visitor
        if shelter_clip_is_terminal(clip) and clip in SHELTER_VISITORS[visitor]["clips"]:
            return Transform(shelter_movie_frame(visitor, clip, "end"), xysize=(1920, 1080))
        return Transform(shelter_wait_image(clip, visitor), xysize=(1920, 1080))

    def shelter_hold_current_frame():
        # Run before Return removes the clicked screen, including old saves
        # that have never passed through the new playback/backdrop code.
        renpy.show("shelter_hold", what=shelter_video_end(shelter_still))

    def shelter_movie_frame(visitor, clip, edge):
        if visitor == "undral":
            return shelter_undral_poster(clip, edge)
        if visitor == "naraa":
            return shelter_naraa_poster(clip, edge)
        return "images/transitions/" + visitor + "/" + clip + "-" + edge + ".jpg"

    def shelter_movie_start_image(visitor, clip):
        return shelter_movie_frame(visitor, clip, "start")

    def shelter_movie_path(visitor, clip):
        path = "Video/" + visitor + "/" + SHELTER_VISITORS[visitor]["clips"][clip][0]
        start = SHELTER_CLIP_STARTS.get(visitor + "/" + clip)
        end = SHELTER_CLIP_ENDS.get(visitor + "/" + clip)
        bounds = (("from %s " % start) if start is not None else "") + (("to %s" % end) if end is not None else "")
        return ("<%s>" % bounds.strip() if bounds else "") + path

    def shelter_speech_position(clip):
        position = renpy.music.get_pos(channel="shelter_video")
        start = SHELTER_CLIP_STARTS.get(shelter_visitor + "/" + clip)
        # Ren'Py backends can report either source time or time since <from>.
        if position is not None and start is not None and position < start:
            position += start
        return position

    shelter_movies = {
        (visitor, key): Movie(
            play=shelter_movie_path(visitor, key),
            channel="shelter_video", loop=False, size=(1920, 1080),
            start_image=Transform(shelter_movie_start_image(visitor, key), xysize=(1920, 1080)),
            image=Transform(shelter_movie_frame(visitor, key, "end"), xysize=(1920, 1080)),
            keep_last_frame=True)
        for visitor, encounter in SHELTER_VISITORS.items()
        for key, data in encounter["clips"].items()
    }

    # Margad's first response stays on one decoder. The conversation screen
    # pauses this movie for the player's two follow-up question buttons, then
    # resumes the same stream instead of swapping to a still frame.
    shelter_margad_answer1_movie = Movie(
        play="<to 22.040>Video/margad/Chotgor hariult 1.webm",
        channel="shelter_video", loop=False, size=(1920, 1080),
        start_image=Transform(shelter_movie_frame("margad", "answer1", "start"), xysize=(1920, 1080)),
        image=Transform(shelter_movie_frame("margad", "answer1_part3", "end"), xysize=(1920, 1080)),
        keep_last_frame=True)


    def shelter_movie_for(visitor, clip):
        # A saved/older movie cache can predate newly registered visitors.
        # Populate missing entries on demand instead of crashing with KeyError.
        key = (visitor, clip)
        if key not in shelter_movies:
            shelter_movies[key] = Movie(
                play=shelter_movie_path(visitor, clip),
                channel="shelter_video", loop=False, size=(1920, 1080),
                start_image=Transform(shelter_movie_start_image(visitor, clip), xysize=(1920, 1080)),
                image=Transform(shelter_movie_frame(visitor, clip, "end"), xysize=(1920, 1080)),
                keep_last_frame=True)
        return shelter_movies[key]

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
            ypos (580 if shelter_visitor in ("Bayra", "ganba", "ganzo") else 630 if shelter_visitor == "Swat" else 710)
            xsize 1344
            padding (35, 22)
            text shelter_data("lines")[clip] style "shelter_text" size (24 if shelter_visitor == "Bayra" else 26 if shelter_visitor in ("Swat", "ganba", "ganzo") else 30) xalign 0.5 text_align 0.5
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

# Player speaks over the waiting portrait; Maral responds only after EOF.
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

# One continuous Margad response movie with two interactive pause points.
screen shelter_margad_answer1_playback():
    modal True
    default stage = 0
    default stage_elapsed = 0.0

    add shelter_movie_frame("margad", "answer1", "start") xysize (1920, 1080)
    add shelter_margad_answer1_movie xysize (1920, 1080)
    use shelter_actions(enabled=False)

    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    on "hide" action [Stop("shelter_player"), Function(renpy.music.set_pause, False, channel="shelter_video")]

    $ video_position = renpy.music.get_pos(channel="shelter_video")
    $ player_position = renpy.music.get_pos(channel="shelter_player")

    if stage == 0 and video_position is not None and 1.073 <= video_position < 11.525:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos 710
            xsize 1344
            padding (35, 22)
            text MARGAD_LINES["answer1"] style "shelter_text" text_align 0.5 xalign 0.5
    elif stage == 3 and video_position is not None and 13.140 <= video_position < 16.414:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos 710
            xsize 1344
            padding (35, 22)
            text MARGAD_LINES["answer1_part2"] style "shelter_text" text_align 0.5 xalign 0.5
    elif stage == 6 and video_position is not None and 17.740 <= video_position < 22.040:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos 710
            xsize 1344
            padding (35, 22)
            text MARGAD_LINES["answer1_part3"] style "shelter_text" text_align 0.5 xalign 0.5

    if stage == 1:
        textbutton MARGAD_QUESTION1_PART2:
            style "shelter_button"
            text_style "shelter_button_text"
            text_size 27
            text_text_align 0.5
            xalign 0.5
            ypos 670
            xysize (850, 112)
            action [
                Play("shelter_player", MARGAD_SUPPLIED_PLAYER_VOICES["question1_part2"][0]),
                SetScreenVariable("stage_elapsed", 0.0),
                SetScreenVariable("stage", 2)]
    elif stage == 4:
        textbutton MARGAD_QUESTION1_PART3:
            style "shelter_button"
            text_style "shelter_button_text"
            text_size 27
            text_text_align 0.5
            xalign 0.5
            ypos 670
            xysize (850, 112)
            action [
                Play("shelter_player", MARGAD_SUPPLIED_PLAYER_VOICES["question1_part3"][0]),
                SetScreenVariable("stage_elapsed", 0.0),
                SetScreenVariable("stage", 5)]
    elif stage in (2, 5):
        $ voice_key = "question1_part2" if stage == 2 else "question1_part3"
        $ voice_cue = MARGAD_SUPPLIED_PLAYER_VOICES[voice_key]
        $ voice_caption = MARGAD_QUESTION1_PART2 if stage == 2 else MARGAD_QUESTION1_PART3
        if player_position is not None and voice_cue[1] <= player_position < voice_cue[2]:
            frame:
                background Solid("#080707dd")
                xalign 0.5
                ypos 710
                xsize 1344
                padding (35, 22)
                text voice_caption style "shelter_text" text_align 0.5 xalign 0.5

    if not renpy.get_screen("shelter_protocol"):
        if stage == 0:
            timer 0.03 repeat True action If(
                video_position is not None and video_position >= 11.525,
                [Function(renpy.music.set_pause, True, channel="shelter_video"), SetScreenVariable("stage", 1)],
                Function(renpy.restart_interaction))
        elif stage == 2:
            timer 0.03 repeat True action If(
                stage_elapsed >= 0.3 and not renpy.music.get_playing(channel="shelter_player"),
                [Function(renpy.music.set_pause, False, channel="shelter_video"), SetScreenVariable("stage_elapsed", 0.0), SetScreenVariable("stage", 3)],
                SetScreenVariable("stage_elapsed", stage_elapsed + 0.03))
        elif stage == 3:
            timer 0.03 repeat True action If(
                video_position is not None and video_position >= 16.414,
                [Function(renpy.music.set_pause, True, channel="shelter_video"), SetScreenVariable("stage", 4)],
                Function(renpy.restart_interaction))
        elif stage == 5:
            timer 0.03 repeat True action If(
                stage_elapsed >= 0.3 and not renpy.music.get_playing(channel="shelter_player"),
                [Function(renpy.music.set_pause, False, channel="shelter_video"), SetScreenVariable("stage_elapsed", 0.0), SetScreenVariable("stage", 6)],
                SetScreenVariable("stage_elapsed", stage_elapsed + 0.03))
        elif stage == 6:
            timer 0.03 repeat True action If(
                stage_elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_video"),
                Return(True),
                SetScreenVariable("stage_elapsed", stage_elapsed + 0.03))

    use shelter_hold_skip([
        Stop("shelter_player"),
        Function(renpy.music.set_pause, False, channel="shelter_video"),
        Stop("shelter_video"),
        Return("skipped")])
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

label shelter_player_line(voice_key, caption=None):
    # New characters may have response video audio before player voice is supplied.
    if shelter_player_voice(voice_key) is None:
        return
    $ shelter_hold_current_frame()
    window hide None
    $ _skipping = False
    $ renpy.music.play(shelter_player_voice(voice_key)[0], channel="shelter_player", loop=False)
    call screen shelter_player_speech(voice_key, caption)
    $ renpy.music.stop(channel="shelter_player")
    return

label shelter_clip(clip):
    window hide None
    $ _skipping = False
    if not renpy.showing("shelter_hold"):
        # Also repair saves created before a persistent backdrop existed.
        scene expression Transform(shelter_movie_start_image(shelter_visitor, clip), xysize=(1920, 1080)) as shelter_hold
        with None
    hide screen shelter_transition_status
    # A called screen is transient. Keep an opaque image on the master layer
    # too, so screen removal, loading and transitions never expose scene black.
    scene expression Transform(shelter_movie_start_image(shelter_visitor, clip), xysize=(1920, 1080)) as shelter_hold
    # Finish the transition using stills before the decoder starts. A live
    # Movie inside Dissolve can expose an uninitialised video render target.
    with Dissolve(0.6 if clip == "intro" else 0.16)
    if renpy.emscripten:
        $ shelter_web_begin("Video/" + shelter_visitor + "/" + shelter_data("clips")[clip][0], shelter_web_clip_cues(clip), poster=shelter_movie_start_image(shelter_visitor, clip), armed=shelter_clip_is_armed(clip), start_time=SHELTER_CLIP_STARTS.get(shelter_visitor + "/" + clip), end_time=SHELTER_CLIP_ENDS.get(shelter_visitor + "/" + clip), end_poster=shelter_movie_frame(shelter_visitor, clip, "end"))
        call screen shelter_web_wait
    else:
        call screen shelter_playback(clip)
    $ shelter_still = clip
    scene expression Transform(shelter_movie_frame(shelter_visitor, clip, "end"), xysize=(1920, 1080)) as shelter_hold
    call screen shelter_clip_handoff(clip)
    scene expression shelter_video_end(clip) as shelter_hold
    return

label shelter_margad_answer1_conversation:
    window hide None
    $ _skipping = False
    scene expression Transform(shelter_movie_frame("margad", "answer1", "start"), xysize=(1920, 1080)) as shelter_hold
    with Dissolve(0.16)
    if renpy.emscripten:
        $ shelter_web_begin(
            "Video/margad/Chotgor hariult 1.webm",
            ((1.073, 11.525, "", MARGAD_LINES["answer1"]),
            (13.140, 16.414, "", MARGAD_LINES["answer1_part2"]),
            (17.740, 22.040, "", MARGAD_LINES["answer1_part3"])),
            poster=shelter_movie_frame("margad", "answer1", "start"),
            end_time=22.040,
            end_poster=shelter_movie_frame("margad", "answer1_part3", "end"),
            interjections=(
                (11.525, MARGAD_QUESTION1_PART2, MARGAD_SUPPLIED_PLAYER_VOICES["question1_part2"]),
                (16.414, MARGAD_QUESTION1_PART3, MARGAD_SUPPLIED_PLAYER_VOICES["question1_part3"])))
        call screen shelter_web_wait
    else:
        call screen shelter_margad_answer1_playback
    $ shelter_still = "answer1_part3"
    scene expression Transform(shelter_movie_frame("margad", "answer1_part3", "end"), xysize=(1920, 1080)) as shelter_hold
    call screen shelter_clip_handoff("answer1_part3")
    scene expression shelter_video_end("answer1_part3") as shelter_hold
    return

label shelter_encounter:
    play music "<volume 0.18>audio/Audio/shuum.mp3" fadeout 0.6 fadein 1.0
    $ quick_menu = False
    $ shelter_run_order = shelter_make_visitor_order()
    $ shelter_visitor = shelter_run_order[0]
    $ shelter_chinba_outcome = None
    $ shelter_outcomes = {}
    $ shelter_deeremchin_outcomes = {}
    $ shelter_admitted = 0
    $ shelter_civilians_saved = 0
    $ shelter_civilians_killed = 0
    $ shelter_visitors_seen = 0
    $ shelter_story_minutes = SHELTER_CLOCK_START
    $ shelter_inspection_progress = {}
    $ shelter_inspection_requests = []
    $ shelter_inspection_views = {}
    $ shelter_checkpoint_created = False
    $ shelter_checkpoint_written = False
    jump shelter_visit_start

label shelter_visit_start:
    $ shelter_asked = []
    $ shelter_choice = None
    $ shelter_still = "arrival" if shelter_visitor in ("Chinba", "Swat") else "intro"
    call shelter_clip("intro") from _call_shelter_clip_2
    jump shelter_question_phase

label shelter_question_phase:
    call screen shelter_questions
    $ shelter_choice = _return
    jump shelter_handle_choice

label shelter_decision_phase:
    call screen shelter_decision
    $ shelter_choice = _return
    jump shelter_handle_choice

label shelter_handle_choice:
    if shelter_visitor == "deeremchin":
        jump shelter_deeremchin_handle_choice
    if isinstance(shelter_choice, int):
        if shelter_has_inspection(shelter_visitor, shelter_choice):
            call shelter_inspect_belongings from _call_shelter_inspect_belongings
            jump shelter_decision_phase
        $ shelter_asked.append(shelter_choice)
        if shelter_visitor == "margad" and shelter_choice == 0:
            # The first line starts one continuous response movie. Its two
            # follow-up questions are buttons shown while that movie is paused.
            call shelter_player_line("question1", MARGAD_QUESTION1_PART1)
            call shelter_margad_answer1_conversation
        elif shelter_visitor == "naraa" and shelter_choice == 1:
            call shelter_player_line("question2_part1", NARAA_QUESTIONS[1])
            call shelter_naraa_answer2_conversation
        else:
            call shelter_player_line("question%d" % (shelter_choice + 1), shelter_data("questions")[shelter_choice]) from _call_shelter_player_line_2
            call shelter_clip("answer%d" % (shelter_choice + 1)) from _call_shelter_clip_3
        jump shelter_decision_phase
    elif shelter_choice == "aim":
        call shelter_clip("aim") from _call_shelter_clip_4
        call screen shelter_decision(armed=True)
        $ shelter_choice = _return
        if shelter_choice == "lower":
            call shelter_clip("lower") from _call_shelter_clip_5
            jump shelter_decision_phase
        elif shelter_choice in ("reject", "admit"):
            call shelter_clip("lower") from _call_shelter_clip_6
        jump shelter_handle_choice
    elif shelter_choice == "shoot":
        call shelter_clip("shoot") from _call_shelter_clip_7
        jump shelter_resolve_visitor
    elif shelter_choice == "reject":
        call shelter_player_line("reject") from _call_shelter_player_line_3
        call shelter_clip("reject") from _call_shelter_clip_8
        jump shelter_resolve_visitor
    elif shelter_choice == "admit":
        call shelter_player_line("admit") from _call_shelter_player_line_4
        call shelter_clip("admit") from _call_shelter_clip_9
        jump shelter_resolve_visitor
    jump shelter_decision_phase

label shelter_resolve_visitor:
    $ shelter_record_outcome(shelter_visitor, shelter_choice)
    if shelter_visitor == "Chinba":
        $ shelter_chinba_outcome = shelter_choice
    $ shelter_status = shelter_campaign_status()
    if shelter_status == "continue" and not shelter_admitted_monster():
        call shelter_save_midpoint from _call_shelter_save_midpoint
    if shelter_status == "casualties":
        $ shelter_mistakes = shelter_civilian_mistakes()
        call screen shelter_result("ТА ХОЖИГДЛОО", "Та [shelter_mistakes] энгийн хүнийг хөнөөсөн эсвэл хөөж явуулсан. Зөвшөөрөгдөх алдааны дээд хэмжээ 2.")
    elif shelter_admitted_monster():
        $ shelter_monster_ending = "Хүүхэд чөтгөр болон хувирч, тан руу дайрлаа." if shelter_visitor == "undral" else "Эмэгтэй чөтгөр болон хувирч, тан руу дайрлаа." if shelter_visitor == "deeremchin" else "Ану чөтгөр болон хувирч, тан руу дайрлаа." if shelter_visitor == "anu" else "Маргад шууд тан руу дайрлаа." if shelter_visitor == "margad" else "Маралын дүр аймшигтайгаар хувирч, тэр чөтгөрийн инээдээр инээн тан руу дайрлаа."
        call screen shelter_result("ТА АЮУЛЫГ ДОТОГШ ОРУУЛЛАА", shelter_monster_ending)
    elif shelter_status == "win":
        call screen shelter_result("ТА ХОЖЛОО", "Та [SHELTER_CIVILIAN_TARGET] энгийн иргэнийг хорогдох байранд оруулж аварлаа.")
    elif shelter_status == "shortfall":
        call screen shelter_result("ТА ХОЖИГДЛОО", "[SHELTER_TOTAL_VISITORS] хүнийг шалгаж дууслаа. Та [shelter_civilians_saved] / [SHELTER_CIVILIAN_TARGET] энгийн иргэнийг аварсан.")
    elif shelter_next_visitor_id() is not None:
        jump shelter_next_visitor
    else:
        # The available visitor preview is not a complete campaign victory.
        $ shelter_mistakes = shelter_civilian_mistakes()
        call screen shelter_result("ТУРШИЛТЫН ХЭСЭГ ДУУСЛАА", "Оруулсан: [shelter_admitted] • Аврагдсан: [shelter_civilians_saved]/40 • Алдаа: [shelter_mistakes]/2. Үлдсэн дүрүүд хараахан нэмэгдээгүй.")
    if _return == "replay":
        jump shelter_encounter
    return

label shelter_next_visitor:
    $ renpy.music.stop(channel="shelter_player")
    $ renpy.music.stop(channel="shelter_video")
    $ _skipping = False
    # Blend directly from the departure frame to the ledger; no black stop.
    # Keep its live clock/counts after the transient card returns, so the next
    # visitor dissolves from the ledger rather than the previous departure.
    show screen shelter_transition_status
    call screen shelter_next_visitor_card with Dissolve(0.5)
    $ renpy.music.stop(channel="shelter_knock")
    $ shelter_visitor = shelter_next_visitor_id()
    jump shelter_visit_start
