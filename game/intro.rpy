# Opening film. The source MP4 is kept beside the desktop-compatible WebM.
define SHELTER_INTRO_VIDEO = "Video/Introvideo/Intro.webm"
define SHELTER_INTRO_SUBTITLES = "Video/Introvideo/Intro.mn.srt"

init python:
    import bisect as shelter_intro_bisect
    import re as shelter_intro_re

    renpy.music.register_channel(
        "shelter_intro_video", mixer="voice", loop=False,
        stop_on_mute=False, movie=True)

    def shelter_load_intro_subtitles(filename):
        """Read editable UTF-8 SRT cues, in seconds on the movie's own clock."""
        with renpy.file(filename) as source:
            contents = source.read().decode("utf-8-sig").replace("\r\n", "\n")
        cues = []
        for block in shelter_intro_re.split(r"\n\s*\n", contents.strip()):
            lines = block.splitlines()
            timestamps = shelter_intro_re.fullmatch(
                r"(\d+):(\d{2}):(\d{2}),(\d{3}) --> "
                r"(\d+):(\d{2}):(\d{2}),(\d{3})", lines[1])
            if timestamps is None:
                raise ValueError("Invalid intro subtitle timestamp: " + lines[1])
            values = [int(value) for value in timestamps.groups()]
            start = values[0] * 3600 + values[1] * 60 + values[2] + values[3] / 1000.0
            end = values[4] * 3600 + values[5] * 60 + values[6] + values[7] / 1000.0
            if end <= start or (cues and start < cues[-1][1]):
                raise ValueError("Intro subtitle cues must be ordered and non-overlapping.")
            # Keep each timed cue on one line, including externally edited SRTs.
            caption = " ".join(" ".join(lines[2:]).split())
            speaker = ""
            for name in ("Хурандаа", "Цэрэг"):
                if caption.startswith(name + ":"):
                    speaker, caption = name, caption[len(name) + 1:].lstrip()
                    break
            cues.append((start, end, speaker, caption))
        return tuple(cues)

    shelter_intro_cues = shelter_load_intro_subtitles(SHELTER_INTRO_SUBTITLES)
    shelter_intro_cue_starts = tuple(cue[0] for cue in shelter_intro_cues)

    def shelter_intro_subtitle(position):
        if position is None:
            return None
        index = shelter_intro_bisect.bisect_right(shelter_intro_cue_starts, position) - 1
        if index >= 0 and position < shelter_intro_cues[index][1]:
            return shelter_intro_cues[index]
        return None

    shelter_intro_movie = Movie(
        play=SHELTER_INTRO_VIDEO, channel="shelter_intro_video",
        loop=False, size=(1920, 1080),
        start_image=Solid("#000000"), image=Solid("#000000"))


screen shelter_intro_playback():
    modal True
    default elapsed = 0.0

    add Solid("#000000")
    add shelter_intro_movie xysize (1920, 1080)

    # A deliberate button / Escape skips the film; ordinary clicks don't.
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    key "rollforward" action NullAction()
    key "hide_windows" action NullAction()
    key "game_menu" action Return("skipped")
    on "hide" action Stop("shelter_intro_video")

    vbox:
        xalign 1.0
        xoffset -48
        ypos 48
        spacing 8
        use shelter_metal_button("Алгасах  ››", Return("skipped"), 260)
        if renpy.variant("pc"):
            text "ESC":
                font SHELTER_FONT
                size 18
                color "#d7cbb7"
                outlines [(1, "#000c", 0, 1)]
                xalign 1.0
                xoffset -12

    $ cue = shelter_intro_subtitle(renpy.music.get_pos(channel="shelter_intro_video"))
    if cue:
        frame:
            background Solid("#080707d9")
            xalign 0.5
            yanchor 1.0
            ypos 1016
            xsize 1520
            padding (36, 22)
            hbox:
                xalign 0.5
                spacing 10
                if cue[2]:
                    text (cue[2] + ":"):
                        font SHELTER_BOLD
                        size 36
                        color "#d9aa83"
                        layout "nobreak"
                text cue[3]:
                    id "intro_subtitle"
                    style "shelter_text"
                    size 36
                    xalign 0.5
                    text_align 0.5
                    layout "nobreak"

    # The timer refreshes the screen; only the decoder determines cue time/EOF.
    # A startup grace period avoids treating a queued movie as already finished.
    timer 0.03 repeat True action If(
        elapsed >= 1.0 and not renpy.music.get_playing(channel="shelter_intro_video"),
        Return("finished"), SetScreenVariable("elapsed", elapsed + 0.03))


label shelter_intro:
    window hide
    $ quick_menu = False
    $ _skipping = False
    $ renpy.block_rollback()
    stop music
    scene black
    if renpy.emscripten:
        $ shelter_web_begin(SHELTER_INTRO_VIDEO, shelter_intro_cues, intro=True)
        call screen shelter_web_wait
        $ shelter_web_close()
    else:
        call screen shelter_intro_playback
    $ renpy.music.stop(channel="shelter_intro_video")
    $ _skipping = False
    $ renpy.block_rollback()
    return
