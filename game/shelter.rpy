# Video-driven encounter. Runtime WebM files are derived from the MP4 sources.
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
    "admit": ("Maral oruulah.webm", 6.048),
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
    # Construct Movie displayables once, not on every screen evaluation.
    shelter_movies = {
        key: Movie(play="Video/Maral/runtime/" + data[0], channel="shelter_video",
                   loop=False, size=(1920, 1080),
                   start_image="images/stills/" + key + "_start.jpg",
                   image="images/stills/" + key + ".jpg")
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
    if shelter_still in ("intro", "answer1", "answer2", "answer3", "lower"):
        add "images/Maral idle zassan.jpg" xysize (1920, 1080)
    else:
        add "images/stills/[shelter_still].jpg" xysize (1920, 1080)

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
    add shelter_movies[clip]
    use shelter_header("ЯРИЛЦЛАГА", utilities=False)
    # Block click-to-dismiss and keyboard skipping while the clip plays.
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    if clip in SHELTER_LINES:
        frame:
            background Solid("#080707dd")
            xpos 210
            ypos 820
            xsize 1500
            padding (35, 22)
            text SHELTER_LINES[clip] style "shelter_text" size 32
    # A short startup grace avoids interpreting a not-yet-started decoder as EOF.
    # Actual playback completion, rather than a fixed timer, drives progression.
    timer 0.1 repeat True action If(
        elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_video"),
        Return(True), SetScreenVariable("elapsed", elapsed + 0.1))

screen shelter_questions():
    modal True
    use shelter_backdrop
    use shelter_header("АСУУЛТ СОНГОХ")
    vbox:
        xpos 70
        ypos 810
        spacing 18
        at shelter_fade
        text "ЮУ АСУУХ ВЭ?" style "shelter_text" size 25 color "#e2bc86"
        hbox:
            spacing 20
            for index, question in enumerate(SHELTER_QUESTIONS):
                button:
                    style "shelter_button"
                    xsize 580
                    ysize 170
                    sensitive index not in shelter_asked
                    action Return(index)
                    vbox:
                        spacing 12
                        text ("АСУУСАН" if index in shelter_asked else "%02d" % (index + 1)) style "shelter_button_text" size 24 color "#e2bc86"
                        text question style "shelter_button_text" size 30
    # Final decisions deliberately do not appear in this phase.

screen shelter_decision(armed=False):
    modal True
    use shelter_backdrop
    use shelter_header("ШИЙДВЭР ГАРГАХ")
    vbox:
        xpos 1300
        ypos 685
        spacing 14
        at shelter_fade
        text "ШИЙДВЭРЭЭ СОНГОНО УУ" style "shelter_text" size 25 color "#e2bc86"
        if armed:
            textbutton "Буудах":
                style "shelter_button"
                text_style "shelter_button_text"
                text_color "#ff7770"
                xsize 550
                ysize 92
                action Return("shoot")
            textbutton "Буугаа буулгах":
                style "shelter_button"
                text_style "shelter_button_text"
                xsize 550
                ysize 92
                action Return("lower")
        else:
            for caption, result in [("Буу онилох", "aim"), ("Хөөж явуулах", "reject"), ("Дотогш оруулах", "admit")]:
                textbutton caption:
                    style "shelter_button"
                    text_style "shelter_button_text"
                    xsize 550
                    ysize 92
                    action Return(result)
    if not armed and len(shelter_asked) < len(SHELTER_QUESTIONS):
        textbutton "Дахин асуулт асуух":
            style "shelter_button"
            text_style "shelter_button_text"
            xpos 70
            ypos 915
            xsize 720
            ysize 92
            action Return("questions")

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
    $ shelter_asked.append(shelter_choice)
    call shelter_clip("answer%d" % (shelter_choice + 1))
    jump shelter_decision_phase

label shelter_decision_phase:
    call screen shelter_decision
    $ shelter_choice = _return
    if shelter_choice == "questions":
        jump shelter_question_phase
    elif shelter_choice == "aim":
        call shelter_clip("aim")
        call screen shelter_decision(armed=True)
        if _return == "lower":
            call shelter_clip("lower")
            jump shelter_decision_phase
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
