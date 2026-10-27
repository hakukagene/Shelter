# Naraa - civilian encounter. Media supplied in game/Video/naraa/.
# Durations were measured from the supplied VP9/Opus WebMs.
define NARAA_POSTERS = {
    "idle": "images/naraa/Naraa Idle.jpg",
    "aim": "images/naraa/Naraa garaa orgov.png",
}
define NARAA_POSTER_STATES = {
    "intro": ("idle", "idle"),
    "answer1": ("idle", "idle"),
    "answer2": ("idle", "idle"),
    "answer3": ("idle", "idle"),
    "aim": ("idle", "aim"),
    "lower": ("aim", "idle"),
    "shoot": ("aim", "aim"),
    "admit": ("idle", "idle"),
    "reject": ("idle", "idle"),
}

init python:
    def shelter_naraa_poster(clip, edge="end"):
        states = NARAA_POSTER_STATES.get(clip, ("idle", "idle"))
        return NARAA_POSTERS[states[0 if edge == "start" else 1]]

define NARAA_CLIPS = {
    "intro": ("Naraa Ehlel.webm", 12.368),
    "answer1": ("Naraa Hariult 1.webm", 38.968),
    "answer2": ("Naraa Hariult 2.webm", 26.688),
    "answer3": ("Naraa Hariult 3.webm", 15.368),
    "aim": ("Naraa garaa orgoh.webm", 12.128),
    "lower": ("Naraa garaa buulgah.webm", 3.048),
    "shoot": ("Naraag buudah.webm", 4.048),
    "admit": ("Naraa Oruulah.webm", 7.043),
    "reject": ("Naraa hoogdoh.webm", 8.968),
}

# Player question captions.
define NARAA_QUESTIONS = [
    "Чамд юу тохиолдоо вэ?",
    "Чамайг яагаад би оруулах ёстой вэ?",
    "Цүнхэнд чинь юу байгаа вэ?",
]
# Subtitles restored from the supplied Shelter character script.
# Broad clip windows keep script captions visible; these are not word-level timings.
define NARAA_LINES = {
    "intro": "Сайн уу, сайхан залуу минь. Энэ хорогдох байр мөн үү? Намайг оруулаач. Чи нар харамсахгүй шүү.",
    "answer1": "За байз… буудлын арын гудамжинд нэг үйлчлүүлэгч маань гэнэт хүн рүү дайрсан. Эхэндээ маргалдаж байна гэж бодоод холдсон л доо, гэтэл тэр хүний нүүр нэг л сонин болж эхэлсэн. Манай найзууд руу дайраад бөөн цус нөж болоод эхэлсэн, би бүр ШОК. Хаа сайгүй сандарсан гүйлдсэн хүмүүс. Би зугтаж такси хайж байгаад машинд мөргүүлчихсэн. Хэсэг ухаангүй байсан бололтой. Сэрээд харсан энэ хавьд гэрэл гарч байгаа харагдаад хүрээд ирлээ.",
    "answer2": "Наадах чинь хорогдох байр юм биш үү. Орж хорогдоё л доо. Би тийм ч энгийн хүн биш л дээ. За л даа, ийм сайхан хүүхнийг үх гээд орхино гэж үү? Намайг оруулбал би хариуг чинь барина шүү. Яаж гэдгийг нь чи мэдэж байгаа биз дээ айн? кк",
    "answer3": "Миний хувийн эд зүйлс байгаа. Уучлаарай, хэт хувийн эд зүйлс байгаа тул би харуулж чадахгүй нь.",
    "aim": "Оёоёоёо, яасан айхтар ууртай юм. Чи арай буудчихгүй биз дээ айн.",
    "reject": "Ёооё, чи лав гомо байх аа.",
    "admit": "Ёооё, тийм байлгүй дээ. Надад эрчүүд ер нь татгалзаад байдаггүй л дээ. Би чамайг Gay юм болов уу л гэж бодож эхэлж байлаа шүү."
}
define NARAA_SPEECH_WINDOWS = {
    "intro": (0.0, NARAA_CLIPS["intro"][1]),
    "answer1": (0.0, NARAA_CLIPS["answer1"][1]),
    "answer2": (0.0, NARAA_CLIPS["answer2"][1]),
    "answer3": (0.0, NARAA_CLIPS["answer3"][1]),
    "aim": (0.0, NARAA_CLIPS["aim"][1]),
    "reject": (0.0, NARAA_CLIPS["reject"][1]),
    "admit": (0.0, NARAA_CLIPS["admit"][1]),
}

# Naraa's question recordings are registered in player_voices.rpy.

# Initial split point from the former first-response clip. Tune against the
# replacement soundtrack if its first line ends earlier/later.
define NARAA_ANSWER2_PAUSE = 5.008
define NARAA_QUESTION2_FOLLOWUP = "Тиймээ гэхдээ би чамайг энгийн хүн гэж яагаад итгэх ёстой гэж?"
define NARAA_ANSWER2_FIRST = "Наадах чинь хорогдох байр юм биш үү. Орж хорогдоё л доо."
define NARAA_ANSWER2_SECOND = "Би тийм ч энгийн хүн биш л дээ. За л даа, ийм сайхан хүүхнийг үх гээд орхино гэж үү? Намайг оруулбал би хариуг чинь барина шүү. Яаж гэдгийг нь чи мэдэж байгаа биз дээ айн? кк"

screen shelter_naraa_answer2_playback():
    modal True
    default stage = 0
    default stage_elapsed = 0.0
    add shelter_movie_frame("naraa", "answer2", "start") xysize (1920, 1080)
    add shelter_movie_for("naraa", "answer2") xysize (1920, 1080)
    use shelter_actions(enabled=False)
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    on "hide" action [Stop("shelter_player"), Function(renpy.music.set_pause, False, channel="shelter_video")]

    $ video_position = renpy.music.get_pos(channel="shelter_video")
    $ voice_cue = shelter_player_voice("question2_part2", "naraa")
    if stage == 1:
        textbutton NARAA_QUESTION2_FOLLOWUP:
            style "shelter_button"
            text_style "shelter_button_text"
            text_size 27
            text_text_align 0.5
            xalign 0.5
            ypos 670
            xysize (850, 112)
            action [Play("shelter_player", voice_cue[0]), SetScreenVariable("stage_elapsed", 0.0), SetScreenVariable("stage", 2)]
    elif stage == 2 or (stage in (0, 3) and video_position is not None):
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos 710
            xsize 1344
            padding (35, 22)
            text (NARAA_QUESTION2_FOLLOWUP if stage == 2 else NARAA_ANSWER2_FIRST if stage == 0 else NARAA_ANSWER2_SECOND) style "shelter_text" size 30 text_align 0.5 xalign 0.5

    if not renpy.get_screen("shelter_protocol"):
        if stage == 0:
            timer 0.03 repeat True action If(
                video_position is not None and video_position >= NARAA_ANSWER2_PAUSE,
                [Function(renpy.music.set_pause, True, channel="shelter_video"), SetScreenVariable("stage", 1)],
                Function(renpy.restart_interaction))
        elif stage == 2:
            timer 0.03 repeat True action If(
                stage_elapsed >= 0.3 and not renpy.music.get_playing(channel="shelter_player"),
                [Function(renpy.music.set_pause, False, channel="shelter_video"), SetScreenVariable("stage_elapsed", 0.0), SetScreenVariable("stage", 3)],
                SetScreenVariable("stage_elapsed", stage_elapsed + 0.03))
        elif stage == 3:
            timer 0.03 repeat True action If(
                stage_elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_video"),
                Return(True), SetScreenVariable("stage_elapsed", stage_elapsed + 0.03))

    use shelter_hold_skip([Stop("shelter_player"), Function(renpy.music.set_pause, False, channel="shelter_video"), Stop("shelter_video"), Return("skipped")])
    use shelter_protocol_button

label shelter_naraa_answer2_conversation:
    window hide None
    $ _skipping = False
    scene expression Transform(shelter_movie_frame("naraa", "answer2", "start"), xysize=(1920, 1080)) as shelter_hold
    with Dissolve(0.16)
    if renpy.emscripten:
        $ shelter_web_begin(
            "Video/naraa/" + NARAA_CLIPS["answer2"][0],
            ((0.0, NARAA_ANSWER2_PAUSE, "", NARAA_ANSWER2_FIRST),
             (NARAA_ANSWER2_PAUSE, NARAA_CLIPS["answer2"][1], "", NARAA_ANSWER2_SECOND)),
            poster=shelter_movie_frame("naraa", "answer2", "start"),
            end_poster=shelter_movie_frame("naraa", "answer2", "end"),
            interjections=((NARAA_ANSWER2_PAUSE, NARAA_QUESTION2_FOLLOWUP, shelter_player_voice("question2_part2", "naraa")),))
        call screen shelter_web_wait
    else:
        call screen shelter_naraa_answer2_playback
    $ shelter_still = "answer2"
    scene expression Transform(shelter_movie_frame("naraa", "answer2", "end"), xysize=(1920, 1080)) as shelter_hold
    call screen shelter_clip_handoff("answer2")
    scene expression shelter_video_end("answer2") as shelter_hold
    return
