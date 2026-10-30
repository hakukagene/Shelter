# Margad, 18: monster. The first answer is a three-part conversation.
define MARGAD_CLIPS = {
    "intro": ("Chotgor ehlel.webm", 21.728),
    "answer1": ("Chotgor hariult 1.webm", 11.525),
    "answer1_part2": ("Chotgor hariult 1.webm", 3.274),
    "answer1_part3": ("Chotgor hariult 1.webm", 4.300),
    "answer2": ("Chotgor hariult 2.webm", 16.648),
    "answer3": ("Chotgor hariult 3.webm", 9.528),
    "aim": ("Chotgor Buu tulgah.webm", 4.288),
    "lower": ("Chotgor buugaa bolih.webm", 3.048),
    "shoot": ("Chotgor buuduulah.webm", 7.048),
    "reject": ("ChotgorHuuh.webm", 5.046),
    "admit": ("Chotgor oruulah.webm", 6.408),
}

define MARGAD_QUESTIONS = [
    "Чи Cosplayer юм бол яагаад багаа тайлахгүй байгаа юм бэ?",
    "Чи тэгээд ямар киноны юу гэдэг дүрийн өмсгөл өмссөн юм бэ?",
    "Наад цус чинь жинхэнэ үү?",
]

define MARGAD_QUESTION1_PART1 = "Чи Cosplayer юм бол яагаад багаа тайлахгүй байгаа юм бэ?"
define MARGAD_QUESTION1_PART2 = "Наадах чинь баг юм бол яагаад ам нь хөдлөөд байгаа юм."
define MARGAD_QUESTION1_PART3 = "Ийм тэнэг түүхэнд чинь итгэнэ гэж бодоо юу?"

define MARGAD_LINES = {
    "intro": "Хөөе, хөөе, битгий буудчихаарай. Би мангас биш шүү. Би cosplay арга хэмжээнд оролцоод явж байсан юм аа. Яг мангас шиг харагдаж байгаа биз? Хэхэ. Харин хүмүүс айж зугтаад л байна. Би хүн байна аа, битгий айгаарай гээд очихоор л царай хараад зугтаагаад байх юм.",
    "answer1": "Харин арга хэмжээн дээр баг маань салж унаад, манай найз бид хоёр яараад супер цавуу түрхэж байгаад янзалсан юм аа. Тэгсэн цавуу нь бүр бие, нүүртэй маань наалдчихаж.",
    "answer1_part2": "Энэ харин ам дагаж хөдөлдөг баг юм аа.",
    "answer1_part3": "Нээрээ. Намайг оруулж энэ багийг тайлахад туслаач.",
    "answer2": "Ёо, та анимэ үздэггүй юм уу даа. Харваас ойлгомжтой байгаа биз дээ. Яагаав, Naruto дээр гардаг шүү дээ. Яагаав, НАРУТО ШИППҮҮДЭН. Кагэ башин но жицү.",
    "answer3": "Энэ жинхэнэ цус биш ээ. Cosplay үзүүлбэрт ашигласан будаг шүү дээ. Та сайн хар л даа. Үнэртэх ч үгүй байгаа биз дээ. Ахаа, би яг өлсөж үхлээ. Оръё л доо.",
    "aim": "Больё оо, агаа. Байя, агаа.",
}

# Source-clock windows. Split answer-one clips seek within the same WebM.
define MARGAD_SPEECH_WINDOWS = {
    "intro": (0.000, 20.772),
    "answer1": (1.073, 11.525),
    "answer1_part2": (13.140, 16.414),
    "answer1_part3": (17.740, 22.040),
    "answer2": (1.231, 15.934),
    "answer3": (0.886, 8.965),
    "aim": (1.273, 4.022),
}

define MARGAD_SUPPLIED_PLAYER_VOICES = {
    "question1": ("audio/margad/margad asuult1 1heseg.wav", 0.090, 2.884),
    "question1_part2": ("audio/margad/margad asuult1 2heseg.wav", 0.101, 2.608),
    "question1_part3": ("audio/margad/margad asuult1 3heseg.wav", 0.101, 2.163),
    "question2": ("audio/margad/margad asuult2.wav", 0.000, 3.396),
    "question3": ("audio/margad/margad asuult3.wav", 0.082, 1.418),
}

init 1 python:
    # Preserve the exact pose across the two player interjections.
    shelter_register_visitor("margad", roster_position=9, civilian=False,
        clips=MARGAD_CLIPS, questions=MARGAD_QUESTIONS, lines=MARGAD_LINES,
        windows=MARGAD_SPEECH_WINDOWS, supplied_voices=MARGAD_SUPPLIED_PLAYER_VOICES,
        idle_still=("answer1", "start"),
        idle_clips=("intro", "answer1_part3", "answer2", "answer3", "lower"),
        conversations={0: "shelter_margad_answer1_conversation"},
        monster_ending="Маргад шууд тан руу дайрлаа.")

init 2 python:
    # Margad's first response stays on one decoder. The conversation screen
    # pauses this movie for the player's two follow-up question buttons, then
    # resumes the same stream instead of swapping to a still frame.
    shelter_margad_answer1_movie = Movie(
        play="<to 22.040>Video/margad/Chotgor hariult 1.webm",
        channel="shelter_video", loop=False, size=(1920, 1080),
        start_image=Transform(shelter_movie_frame("margad", "answer1", "start"), xysize=(1920, 1080)),
        image=Transform(shelter_movie_frame("margad", "answer1_part3", "end"), xysize=(1920, 1080)),
        keep_last_frame=True)

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
