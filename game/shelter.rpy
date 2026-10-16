# Video-driven encounter using the supplied VP9/Opus WebM assets.
define SHELTER_FONT = "fonts/RobotoCondensed-Regular.ttf"
define SHELTER_BOLD = "fonts/RobotoCondensed-Bold.ttf"

default shelter_still = "intro"
default shelter_asked = []
default shelter_choice = None

define SHELTER_CLIPS = {
    "intro": ("Maral ehlel.webm", 12.808),
    "answer1": ("Maral hariult1.webm", 6.168),
    "answer2": ("Maral hariult2.webm", 5.928),
    "answer3": ("Maral hariult3.webm", 6.168),
    "aim": ("Maral buu gargah.webm", 11.568),
    "lower": ("Maral buudahaa bolih.webm", 3.048),
    "shoot": ("Maral buudah.webm", 8.048),
    "admit": ("Maral oruulah B huvilbar.webm", 6.048),
    "reject": ("Maral yavah.webm", 5.008),
}

define SHELTER_QUESTIONS = [
    "Чи ямар тайван байна аа. Айхгүй байгаа юм уу?",
    "Манай хорогдох байрыг хаанаас сонссон бэ?",
    "Надад худлаа яривал оруулахгүй гэдгийг мэдэж байгаа биз дээ?",
]

define SHELTER_LINES = {
    "intro": "Сайн байна уу. Би танай хорогдох байрны талаар сонсоод ирж байна аа. Энэ аюултай үед шалгаж оруулах байлгүй дээ. Би шалгуулахад бэлэн байна.",
    "answer1": "Айдас шийдвэр гаргахад туслахгүй л дээ. Та ч бас айж байгаа мөртлөө өөрийгөө барьж байна шүү дээ.",
    "answer2": "Радиогоор сонссон юм аа. Хэд хэдэн хорогдох байр хэлсний хамгийн ойр нь танайх байлаа.",
    "answer3": "Тэгвэл намайг сайн шалга. Гэхдээ намайг оруулж болохгүй гэдэг дүгнэлтэд хүрэхийн тулд бодитой шалтгаан хэрэгтэй биз дээ?",
    "aim": "Чи намайг буудаж болно. Гэхдээ эхлээд яагаад гэдгээ өөрөөсөө асуугаарай.",
}

# Cue windows measured from the bundled audio; times use the decoder clock.
# Keep these separate so dialogue edits do not require changing screen logic.
define SHELTER_SPEECH_WINDOWS = {
    "intro": (0.0, 12.49),
    "answer1": (0.568, 5.716),
    "answer2": (0.691, 5.597),
    "answer3": (0.568, 5.716),
    "aim": (3.199, 8.260),
}

define SHELTER_PLAYER_VOICES = {
    "question1": ("audio/Chingune/MaralAsuult1.wav", 0.620, 2.501),
    "question2": ("audio/Chingune/MaralAsuult2.wav", 0.865, 2.699),
    "question3": ("audio/Chingune/MaralAsuult3.wav", 0.780, 3.954),
    "reject": ("audio/Chingune/MaralHuuh.wav", 0.395, 1.549),
    "admit": ("audio/Chingune/MaralOruulah.wav", 0.347, 0.879),
}

init python:
    renpy.music.register_channel("shelter_player", mixer="voice", loop=False, stop_on_mute=False)
    renpy.music.register_channel("shelter_video", mixer="voice", loop=False, movie=True)
    def shelter_wait_image(clip):
        if clip == "aim":
            return "images/Maral/Maral ineeh.png"
        return "images/Maral/Maral idle zassan.jpg"

    def shelter_video_end(clip):
        # Terminal clips share the result background to avoid a black flash.
        if clip in ("shoot", "admit", "reject"):
            return Transform("gui/shelter/ending/lockdown.jpg", xysize=(1920, 1080))
        return Transform(shelter_wait_image(clip), xysize=(1920, 1080))

    # Movie.size does not resize fallback images; size those explicitly too.
    shelter_movies = {
        key: Movie(play="Video/Maral/" + data[0], channel="shelter_video",
                loop=False, size=(1920, 1080),
                start_image=Transform(shelter_wait_image("aim" if key in
                    ("shoot", "lower") else "intro"), xysize=(1920, 1080)),
                image=shelter_video_end(key))
        for key, data in SHELTER_CLIPS.items()
    }

transform shelter_fade:
    alpha 0.0
    linear 0.2 alpha 1.0

style shelter_text is default:
    font SHELTER_FONT
    size 30
    color "#f2e9d9"
    outlines [(1, "#0009", 0, 1)]

style shelter_button is button:
    background Frame("gui/shelter/idle.png", 16, 16)
    hover_background Frame("gui/shelter/hover.png", 16, 16)
    insensitive_background Frame("gui/shelter/disabled.png", 16, 16)
    padding (24, 16)

style shelter_button_text is shelter_text:
    hover_color "#ffd38c"
    insensitive_color "#807b73"
    xalign 0.5
    yalign 0.5
    text_align 0.5

screen shelter_backdrop():
    add shelter_video_end(shelter_still) xysize (1920, 1080)



screen shelter_playback(clip):
    modal True
    default elapsed = 0.0
    add shelter_movies[clip] xysize (1920, 1080)
    use shelter_actions(enabled=False, armed=clip in ("aim", "shoot", "lower"))
    # Block click-to-dismiss and keyboard skipping while the clip plays.
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    $ speech_position = renpy.music.get_pos(channel="shelter_video")
    $ speech_window = SHELTER_SPEECH_WINDOWS.get(clip)
    if speech_window and speech_position is not None and speech_window[0] <= speech_position < speech_window[1]:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos 710
            xsize 1344
            padding (35, 22)
            text SHELTER_LINES[clip] style "shelter_text" size 30 xalign 0.5 text_align 0.5
    # A short startup grace avoids interpreting a not-yet-started decoder as EOF.
    # Actual playback completion, rather than a fixed timer, drives progression.
    timer 0.03 repeat True action If(
        elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_video"),
        Return(True), SetScreenVariable("elapsed", elapsed + 0.03))

# Armed mode offers exactly two actions; aiming lives in the question row.
screen shelter_actions(enabled=True, armed=False):
    hbox:
        xalign 0.5
        ypos 880
        spacing 24
        if armed:
            for caption, result in [("Буудах", "shoot"), ("Буугаа буулгах", "lower")]:
                textbutton caption:
                    style "shelter_button"
                    text_style "shelter_button_text"
                    text_size 28
                    xysize (330, 120)
                    sensitive enabled
                    action Return(result)
        else:
            for caption, result, icon in [("Хөөх", "reject", "reject"), ("Оруулах", "admit", "admit")]:
                button:
                    xysize (180, 180)
                    padding (0, 0)
                    background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180))
                    hover_background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180), matrixcolor=BrightnessMatrix(0.14))
                    insensitive_background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180), matrixcolor=SaturationMatrix(0.35))
                    focus_mask True
                    sensitive enabled
                    action Return(result)
                    text caption:
                        font SHELTER_BOLD
                        size 15
                        color "#f4dfaf"
                        hover_color "#ffffff"
                        insensitive_color "#aa9d86"
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
    $ cue = SHELTER_PLAYER_VOICES[voice_key]
    if caption and position is not None and cue[1] <= position < cue[2]:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos 710
            xsize 1344
            padding (35, 22)
            text caption style "shelter_text" text_align 0.5 xalign 0.5
    timer 0.03 repeat True action If(
        elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_player"),
        Return(True), SetScreenVariable("elapsed", elapsed + 0.03))

screen shelter_question_choices():
    hbox:
        xalign 0.5
        ypos 655
        spacing 16
        for index, question in enumerate(SHELTER_QUESTIONS):
            textbutton question:
                style "shelter_button"
                text_style "shelter_button_text"
                text_size 26
                text_text_align 0.5
                xysize (330, 170)
                sensitive index not in shelter_asked
                action Return(index)
        textbutton "Буу онилох":
            style "shelter_button"
            text_style "shelter_button_text"
            text_size 26
            xysize (330, 170)
            action Return("aim")

screen shelter_questions():
    modal True
    use shelter_backdrop
    use shelter_actions
    use shelter_question_choices


screen shelter_decision(armed=False):
    modal True
    use shelter_backdrop
    use shelter_actions(armed=armed)
    if not armed:
        use shelter_question_choices


# Concept 01: live text and actions over the text-free lockdown artwork.
screen shelter_result(title, description):
    modal True
    add "gui/shelter/ending/lockdown.jpg" xysize (1920, 1080)
    text title:
        style "shelter_text"
        font SHELTER_BOLD
        size 54
        xalign 0.5
        ypos 393
        xsize 1160
        text_align 0.5
    text description:
        style "shelter_text"
        size 32
        xalign 0.5
        ypos 493
        xsize 1120
        text_align 0.5
    # Hit areas match the two physical plates in the background.
    for caption, result, left in [("Дахин тоглох", "replay", 566), ("Үндсэн цэс", "menu", 982)]:
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

label shelter_player_line(voice_key, caption=None):
    window hide
    $ _skipping = False
    $ renpy.music.play(SHELTER_PLAYER_VOICES[voice_key][0], channel="shelter_player", loop=False)
    call screen shelter_player_speech(voice_key, caption)
    $ renpy.music.stop(channel="shelter_player")
    return

label shelter_clip(clip):
    window hide
    $ _skipping = False
    call screen shelter_playback(clip)
    $ shelter_still = clip
    return

label shelter_encounter:
    $ quick_menu = False
    $ shelter_asked = []
    $ shelter_still = "intro"
    call shelter_clip("intro")
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
    if isinstance(shelter_choice, int):
        $ shelter_asked.append(shelter_choice)
        call shelter_player_line("question%d" % (shelter_choice + 1), SHELTER_QUESTIONS[shelter_choice])
        call shelter_clip("answer%d" % (shelter_choice + 1))
        jump shelter_decision_phase
    elif shelter_choice == "aim":
        call shelter_clip("aim")
        call screen shelter_decision(armed=True)
        $ shelter_choice = _return
        if shelter_choice == "lower":
            call shelter_clip("lower")
            jump shelter_decision_phase
        elif shelter_choice in ("reject", "admit"):
            call shelter_clip("lower")
        jump shelter_handle_choice
    elif shelter_choice == "shoot":
        call shelter_clip("shoot")
        call screen shelter_result("БУУДСАН", "Та гох дарлаа. Маралтай хийсэн энэ уулзалт дууслаа.")
    elif shelter_choice == "reject":
        call shelter_player_line("reject")
        call shelter_clip("reject")
        call screen shelter_result("ХААЛГА ХААЛТТАЙ ҮЛДЛЭЭ", "Марал дуугүй эргэн явлаа. Та түүнийг хорогдох байранд оруулсангүй.")
    elif shelter_choice == "admit":
        call shelter_player_line("admit")
        call shelter_clip("admit")
        call screen shelter_result("ТА АЮУЛЫГ ДОТОГШ ОРУУЛЛАА", "Маралын дүр аймшигтайгаар хувирч, тэр чөтгөрийн инээдээр инээн тан руу дайрлаа.")
    if _return == "replay":
        jump shelter_encounter
    return
