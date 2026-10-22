# Live, readable instructions over the approved dossier artwork.
default shelter_protocol_paused_channels = {}

init python:
    def shelter_protocol_pause():
        global shelter_protocol_paused_channels
        shelter_protocol_paused_channels = {
            channel: renpy.music.get_pause(channel=channel)
            for channel in ("shelter_video", "shelter_player", "shelter_knock")}
        for channel in shelter_protocol_paused_channels:
            renpy.music.set_pause(True, channel=channel)

    def shelter_protocol_resume():
        global shelter_protocol_paused_channels
        for channel, paused in shelter_protocol_paused_channels.items():
            renpy.music.set_pause(paused, channel=channel)
        shelter_protocol_paused_channels = {}
        if renpy.emscripten:
            renpy.emscripten.run_script("window.ShelterVideo.resumeFromGuide()")

screen shelter_protocol_button():
    button:
        id "protocol_open"
        xpos 1816
        ypos 24
        xysize (76, 76)
        padding (9, 9)
        background Frame("gui/shelter/metal/button.png", 16, 16)
        hover_background Transform(Frame("gui/shelter/metal/button.png", 16, 16), matrixcolor=BrightnessMatrix(0.2))
        action Show("shelter_protocol")
        tooltip "Тоглоомын заавар"
        alt "Тоглоомын заавар"
        add "gui/shelter/protocol/rules.svg" xysize (58, 58)

screen shelter_protocol(briefing=False):
    modal True
    zorder 200
    add "gui/shelter/protocol/dossier.jpg" xysize (1920, 1080)
    on "show" action Function(shelter_protocol_pause)
    on "hide" action Function(shelter_protocol_resume)
    key "game_menu" action (NullAction() if briefing else Hide("shelter_protocol"))
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    text "БАТЛАГДСАН ТУШААЛ №001":
        font SHELTER_BOLD
        size 29
        color "#e7c4a4"
        pos (958, 251)
        anchor (0.5, 0.5)
        kerning 1
    text "ХОРОГДОХ БАЙРНЫ ПРОТОКОЛ":
        font SHELTER_BOLD
        size 56
        color "#171512"
        pos (985, 330)
        anchor (0.5, 0.5)
    for content, row_y in [
        ("Та {color=#96251c}{b}40{/b}{/color} энгийн хүнийг хүн дүрст чөтгөрүүдээс ялган хорогдох байранд оруулах ёстой.", 430),
        ("Нэг л чөтгөр оруулбал та {color=#96251c}{b}шууд хожигдоно.{/b}{/color}", 515),
        ("Энгийн хүнийг андууран хөнөөх эсвэл хөөж явуулбал таныг {color=#96251c}{b}2 удаа{/b}{/color} уучилна.", 600),
        ("Шийдвэр гаргахаасаа өмнө бүх сонголтыг туршин, {color=#96251c}{b}сэжүүр хай.{/b}{/color}", 688),
        ("{color=#96251c}{b}20{/b}{/color} энгийн хүн оруулсны дараа тоглоом автоматаар {color=#96251c}{b}1 удаа{/b}{/color} хадгалагдана.", 780)]:
        text content:
            font SHELTER_FONT
            size 28
            color "#201b15"
            xpos 658
            ycenter row_y
            xsize 612
            line_spacing 2
    text "НЭГ БУРУУ ШИЙДВЭР БҮГДИЙГ ӨӨРЧИЛЖ МЭДНЭ.":
        font SHELTER_BOLD
        size 25
        color "#f1d8bb"
        pos (1011, 884)
        anchor (0.5, 0.5)
    button:
        id "protocol_close"
        xpos 664
        ypos 936
        xysize (600, 76)
        background None
        hover_background Solid("#ffb99118")
        action (Return(True) if briefing else Hide("shelter_protocol"))
        text ("ОЙЛГОЛОО — ЭЭЛЖЭЭ ЭХЛҮҮЛЭХ  ›" if briefing else "ТОГЛОЛТ РУУ БУЦАХ  ›"):
            font SHELTER_BOLD
            size 31
            color "#f5d8bf"
            hover_color "#ffffff"
            align (0.5, 0.5)
