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

init python:
    renpy.music.register_channel("shelter_video", mixer="voice", loop=False, movie=True)
    def shelter_wait_image(clip):
        if clip == "aim":
            return "images/Maral/Maral ineeh.png"
        return "images/Maral/Maral idle zassan.jpg"

    def shelter_video_end(clip):
        # Terminal clips end on the dark result panel, not a missing still.
        if clip in ("shoot", "admit", "reject"):
            return Solid("#080606", xysize=(1920, 1080))
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
    yalign 0.5

screen shelter_backdrop():
    add shelter_video_end(shelter_still) xysize (1920, 1080)

screen shelter_header(stage, utilities=True):
    add Solid("#080707b8") xysize (1920, 76)
    text "ХОРОГДОХ БАЙР  /  [stage]" style "shelter_text" xpos 65 ypos 22 size 26 color "#e2bc86"
    if utilities:
        hbox:
            xpos 1410
            ypos 16
            spacing 24
            textbutton "Хадгалах" action ShowMenu("save") text_font SHELTER_FONT text_size 26
            textbutton "Тохиргоо" action ShowMenu("preferences") text_font SHELTER_FONT text_size 26
    frame:
        background Solid("#100c0cdc")
        xalign 0.5
        ypos 585
        padding (28, 8)
        text "МАРАЛ  •  28" style "shelter_text" font SHELTER_BOLD size 28

screen shelter_playback(clip):
    modal True
    default elapsed = 0.0
    add shelter_movies[clip] xysize (1920, 1080)
    use shelter_header("ЯРИЛЦЛАГА", utilities=False)
    use shelter_actions(enabled=False, armed=clip in ("aim", "shoot", "lower"))
    # Block click-to-dismiss and keyboard skipping while the clip plays.
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    if clip in SHELTER_LINES:
        frame:
            background Solid("#080707dd")
            xpos 70
            ypos 760
            xsize 1000
            padding (35, 22)
            text SHELTER_LINES[clip] style "shelter_text" size 30
    # A short startup grace avoids interpreting a not-yet-started decoder as EOF.
    # Actual playback completion, rather than a fixed timer, drives progression.
    timer 0.1 repeat True action If(
        elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_video"),
        Return(True), SetScreenVariable("elapsed", elapsed + 0.1))

# Always visible during the encounter. Text remains native for crisp Cyrillic.
screen shelter_actions(enabled=True, armed=False):
    hbox:
        xpos 1100
        ypos 790
        spacing 8
        for caption, result, icon in [("Буудах" if armed else "Буу онилох", "shoot" if armed else "aim", "aim"), ("Хөөж явуулах", "reject", "reject"), ("Дотогш оруулах", "admit", "admit")]:
            button:
                xysize (240, 240)
                padding (0, 0)
                background Transform("gui/shelter/actions/" + icon + ".png", xysize=(240, 240))
                hover_background Transform("gui/shelter/actions/" + icon + ".png", xysize=(240, 240), matrixcolor=BrightnessMatrix(0.14))
                insensitive_background Transform("gui/shelter/actions/" + icon + ".png", xysize=(240, 240), matrixcolor=SaturationMatrix(0.35))
                focus_mask True
                sensitive enabled
                action Return(result)
                text caption:
                    font SHELTER_BOLD
                    size 25
                    color "#f4dfaf"
                    hover_color "#ffffff"
                    insensitive_color "#aa9d86"
                    xalign 0.5
                    ypos 142
                    outlines [(1, "#000b", 0, 1)]

screen shelter_questions():
    modal True
    use shelter_backdrop
    use shelter_header("АСУУЛТ / ШИЙДВЭР")
    use shelter_question_buttons
    use shelter_actions

screen shelter_question_buttons():
    vbox:
        xpos 70
        ypos 795
        spacing 14
        text "ЮУ АСУУХ ВЭ?" style "shelter_text" size 25 color "#e2bc86"
        hbox:
            spacing 12
            for index, question in enumerate(SHELTER_QUESTIONS):
                button:
                    style "shelter_button"
                    padding (16, 12)
                    xsize 320
                    ysize 190
                    sensitive index not in shelter_asked
                    action Return(index)
                    vbox:
                        spacing 8
                        text ("АСУУСАН" if index in shelter_asked else "%02d" % (index + 1)) style "shelter_button_text" size 22 color "#e2bc86"
                        text question style "shelter_button_text" size 26

screen shelter_decision(armed=False):
    modal True
    use shelter_backdrop
    use shelter_header("ШИЙДВЭР ГАРГАХ")
    use shelter_actions(armed=armed)
    if armed:
        textbutton "Буугаа буулгах":
            style "shelter_button"
            text_style "shelter_button_text"
            xpos 70
            ypos 900
            xsize 550
            ysize 92
            action Return("lower")
    else:
        use shelter_question_buttons

screen shelter_result(title, description):
    modal True
    use shelter_backdrop
    add Solid("#080606cb")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 28
        xsize 1100
        text title style "shelter_text" font SHELTER_BOLD size 60 xalign 0.5
        text description style "shelter_text" text_align 0.5 xalign 0.5 size 34
        textbutton "Дахин тоглох":
            style "shelter_button"
            text_style "shelter_button_text"
            xalign 0.5
            action Return("replay")
        textbutton "Үндсэн цэс":
            style "shelter_button"
            text_style "shelter_button_text"
            xalign 0.5
            action Return("menu")

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
        call shelter_clip("reject")
        call screen shelter_result("ХААЛГА ХААЛТТАЙ ҮЛДЛЭЭ", "Марал дуугүй эргэн явлаа. Та түүнийг хорогдох байранд оруулсангүй.")
    elif shelter_choice == "admit":
        call shelter_clip("admit")
        call screen shelter_result("ТА АЮУЛЫГ ДОТОГШ ОРУУЛЛАА", "Маралын дүр аймшигтайгаар хувирч, тэр чөтгөрийн инээдээр инээн тан руу дайрлаа.")
    if _return == "replay":
        jump shelter_encounter
    return
