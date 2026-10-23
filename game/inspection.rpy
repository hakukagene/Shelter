# Character belongings are evidence to examine, never an automatic verdict.
# Assets use alpha atlases or standalone cutouts; each prop stays separate.
default shelter_inspection_progress = {}
default shelter_inspection_requests = []

init python:
    import pygame

    SHELTER_INSPECTION_SPRITES = {
        "ganba_bag": ("ganba-bag.webp", None),
        "delivery_bag": ("containers.png", (0, 90, 580, 770)),
        "school_bag": ("containers.png", (580, 250, 450, 580)),
        "business_bag": ("containers.png", (1040, 245, 496, 585)),
        "meal": ("items.png", (10, 60, 525, 430)),
        "charger": ("items.png", (540, 90, 505, 415)),
        "schedule": ("items.png", (1050, 10, 480, 500)),
        "notebook": ("anu-notebook.webp", None),
        "rabbit": ("items.png", (1090, 510, 440, 505)),
    }
    SHELTER_INSPECTION_ITEMS = {
        "ganba_bag": {
            "name": "Шилтэй архинууд", "action": "Торыг шалгах",
            "description": "Ганбаагийн авч ирсэн гялгар тортой зүйлс.",
            "detail": "Торон дотор шилтэй архинууд байна. Түүний зоориноос авчирсан гэж хэлсэн зүйлтэй таарч байна.",
        },
        "meal": {
            "name": "Захиалгын хоол", "action": "Савлагааг шалгах",
            "description": "Хүргэлтийн үүргэвчнээс гаргасан хоолны сав.",
            "detail": "Хоол савлагаатайгаа байна. Чинбаагийн хэлсэн захиалгын хоол энэ бололтой.",
        },
        "charger": {
            "name": "Утасны цэнэглэгч", "action": "Ойроос шалгах",
            "description": "Цэнэглэгч болон ороосон USB кабель.",
            "detail": "Энгийн утасны цэнэглэгч, кабель байна. Энд утсыг нь залгаж турших боломжгүй.",
        },
        "schedule": {
            "name": "Хүргэлтийн хуваарь", "action": "Хуваарийг унших",
            "description": "Нугалаастай, хүснэгттэй цаас.",
            "detail": "Захиалга хүргэх хуваарь байна. Чинбаа хүргэлт хийж явсан гэж хэлсэн.",
        },
        "notebook": {
            "name": "Зургийн дэвтэр", "action": "Зургийн тухай асуух ",
            "description": "Анугийн сургуулийн цүнхэнд байсан жижиг дэвтэр.",
            "detail": "Сүүлийн хуудсанд энэ хорогдох байрны хаалга, дотор талын дугуй түгжээг зуржээ.",

        },
        "rabbit": {
            "name": "Туулайн чихмэл", "action": "Ойроос шалгах",
            "description": "Анугийн гартаа барьж ирсэн туулай. Цүнхнийх нь хажууд тавьжээ.",
            "detail": "Урт чихтэй, улаан зүрхтэй даавуун туулай байна.",
        },
        "business_bag": {
            "name": "Баяраагийн хар цүнх", "action": "Гаднаас нь шалгах",
            "description": "Баяраа цүнхээ нээж үзүүлэхээс татгалзлаа.",
            "detail": "Цүнх хаалттай хэвээр. Дотор нь юу байгааг харах боломж олгосонгүй.",
        },
    }
    # Extend this table only when a visitor and their belongings are supplied.
    SHELTER_INSPECTIONS = {
        "ganba": {"owner": "ГАНБАА", "bag": "ganba_bag",
            "title": "Гялгар тортой шилнүүд", "items": ("ganba_bag",),
            "note": "Тортой шилнүүдийг сонгож ойроос шалгаарай."},
        "Chinba": {"owner": "ЧИНБАА", "bag": "delivery_bag",
            "title": "Хүргэлтийн үүргэвч", "items": ("meal", "charger", "schedule"),
            "note": "Үүргэвчний эд зүйл дээр дарж авч үзээрэй."},
        "anu": {"owner": "АНУ", "bag": "school_bag",
            "title": "Сургуулийн цүнх", "items": ("notebook", "rabbit"),
            "note": "Дэвтрийг нээж үзээрэй. Туулайг цүнхний хажууд тавьсан байна."},
        "Bayra": {"owner": "БАЯРАА", "bag": "business_bag",
            "title": "Хаалттай хар цүнх", "items": ("business_bag",),
            "note": "Цүнхийг зөвхөн гаднаас нь шалгах боломжтой."},
    }

    def shelter_has_inspection(visitor, question):
        return question == 2 and visitor in SHELTER_INSPECTIONS

    def shelter_inspection_sprite(name):
        filename, rect = SHELTER_INSPECTION_SPRITES[name]
        image = "images/inspection/" + filename
        return Crop(rect, image) if rect is not None else image

    def shelter_inspection_done(visitor, item):
        return item in shelter_inspection_progress.get(visitor, ())

    def shelter_inspection_mark(visitor, item):
        global shelter_inspection_progress
        if not shelter_inspection_done(visitor, item):
            shelter_inspection_progress = dict(shelter_inspection_progress,
                **{visitor: tuple(shelter_inspection_progress.get(visitor, ())) + (item,)})

    class ShelterInspectionView(renpy.Displayable):
        """A draggable 2D prop viewer, also usable with buttons and keys.

        No render or texture objects are retained, so save/load is supported.
        It rotates the illustration in its plane, not a fabricated 3D backside.
        """
        def __init__(self, sprite=None, **kwargs):
            super(ShelterInspectionView, self).__init__(**kwargs)
            self.sprite = sprite
            self.angle = 0.0
            self.magnification = 1.0
            self.drag_x = None
            self.drag_angle = 0.0

        def choose(self, sprite):
            self.sprite = sprite
            self.angle = 0.0
            self.magnification = 1.0
            self.drag_x = None
            renpy.redraw(self, 0)

        def turn(self, amount):
            self.angle = (self.angle + amount) % 360
            renpy.redraw(self, 0)

        def zoom(self, amount):
            self.magnification = min(1.6, max(0.75, self.magnification + amount))
            renpy.redraw(self, 0)

        def reset(self):
            self.angle = 0.0
            self.magnification = 1.0
            self.drag_x = None
            renpy.redraw(self, 0)

        def render(self, width, height, st, at):
            rv = renpy.Render(900, 680)
            if self.sprite:
                child = Transform(shelter_inspection_sprite(self.sprite),
                    xysize=(770, 610), fit="contain", zoom=self.magnification,
                    rotate=self.angle, rotate_pad=True)
                rendered = renpy.render(child, 900, 680, st, at)
                w, h = rendered.get_size()
                rv.blit(rendered, ((900-w)/2, (680-h)/2))
            return rv.subsurface((0, 0, 900, 680))

        def event(self, ev, x, y, st):
            inside = 0 <= x < 900 and 0 <= y < 680
            if ev.type == pygame.MOUSEBUTTONDOWN and inside:
                if ev.button == 1:
                    self.drag_x, self.drag_angle = x, self.angle
                elif ev.button in (4, 5):
                    self.zoom(0.1 if ev.button == 4 else -0.1)
                else:
                    return
                raise renpy.IgnoreEvent()
            if ev.type == pygame.MOUSEMOTION and self.drag_x is not None:
                self.angle = (self.drag_angle + (x - self.drag_x) * 0.5) % 360
                renpy.redraw(self, 0)
                raise renpy.IgnoreEvent()
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.drag_x is not None:
                self.drag_x = None
                raise renpy.IgnoreEvent()

# Concept 01: one prop on the illuminated bench, live tag and compact controls.
style inspection_text is shelter_text:
    size 28
    color "#e4ded2"

style inspection_button is button:
    background Frame("gui/shelter/metal/button.png", 28, 18)
    hover_background Transform(Frame("gui/shelter/metal/button.png", 28, 18), matrixcolor=BrightnessMatrix(0.14))
    insensitive_background Transform(Frame("gui/shelter/metal/button.png", 28, 18), matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.16))
    padding (24, 16)
    xminimum 100
    yminimum 64

style inspection_button_text is shelter_button_text:
    size 26

screen inspection_plate(caption, icon, command, enabled=True, width=500):
    button:
        style "inspection_button"
        xysize (width, 94)
        sensitive enabled
        action command
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 15
            add "gui/shelter/inspection/" + icon + ".svg" xysize (45, 45) yalign 0.5
            text caption style "inspection_button_text" font SHELTER_BOLD size 26 yalign 0.5 xmaximum (width-115)

screen shelter_inspection(visitor):
    modal True
    default selected_item = "business_bag" if visitor == "Bayra" else None
    default revealed = False
    default viewer = ShelterInspectionView(SHELTER_INSPECTIONS[visitor]["bag"])
    $ bag = SHELTER_INSPECTIONS[visitor]
    $ checked = sum(shelter_inspection_done(visitor, item) for item in bag["items"])
    $ selected = SHELTER_INSPECTION_ITEMS.get(selected_item)
    # Saves from the previous screen may have an empty viewer at the overview.
    if viewer.sprite is None:
        $ viewer.choose(bag["bag"] if selected_item is None else selected_item)

    add "images/inspection/bench-v2.jpg" xysize (1920, 1080)
    add Solid("#06070766") xysize (1920, 112)
    text "ҮЗЛЭГИЙН ШИРЭЭ" style "inspection_text" font SHELTER_BOLD size 42 xpos 64 ypos 26
    text bag["title"] style "inspection_text" size 22 color "#b9aa91" xpos 66 ypos 78
    text bag["owner"] style "inspection_text" size 30 xanchor 1.0 xpos 1788 ypos 38
    add Solid("#9f86574d") xpos 65 ypos 111 xysize (1790, 1)

    # A single main prop replaces the former duplicate desk/detail previews.
    add "gui/shelter/inspection/shadow.svg" xpos 575 ypos 745 xysize (700, 140)
    add viewer xpos 475 ypos 145

    # Other items remain within reach, like a small tray to the left of the lamp.
    if visitor != "Bayra":
        vbox:
            xpos 64
            ypos 180
            spacing 12
            text "ЭД ЗҮЙЛС · [checked]/[len(bag['items'])]" style "inspection_text" size 21 color "#c1ad8a"
            for item_id in bag["items"]:
                $ item = SHELTER_INSPECTION_ITEMS[item_id]
                button:
                    id ("inspection_item_" + item_id)
                    xysize (344, 118)
                    padding (13, 10)
                    background Solid("#080909b3")
                    hover_background Frame("gui/shelter/metal/selected.png", 28, 18)
                    selected_background Frame("gui/shelter/metal/selected.png", 28, 18)
                    selected selected_item == item_id
                    action [
                        SetScreenVariable("selected_item", item_id),
                        SetScreenVariable("revealed", False),
                        Function(viewer.choose, item_id)
                    ]
                    hbox:
                        spacing 12
                        yalign 0.5
                        add Transform(shelter_inspection_sprite(item_id), xysize=(87, 83), fit="contain") yalign 0.5
                        vbox:
                            yalign 0.5
                            spacing 7
                            text item["name"] style "inspection_text" size 24 xsize 205
                            if shelter_inspection_done(visitor, item_id):
                                text "ШАЛГАСАН" style "inspection_text" size 16 color "#b9a278"
            if selected_item:
                textbutton "Тавих":
                    style "inspection_button"
                    xsize 344
                    action [SetScreenVariable("selected_item", None), SetScreenVariable("revealed", False), Function(viewer.choose, bag["bag"])]

    # Real text on a blank paper tag supports every item and localization.
    fixed:
        xpos 34
        ypos 694
        xysize (460, 178)
        add "images/inspection/evidence-tag.webp" xysize (460, 178)
        vbox:
            xpos 132
            ypos 37
            xsize 294
            spacing 10
            text (selected["name"] if selected else bag["title"]):
                font SHELTER_BOLD
                size 27
                color "#29251d"
                outlines []
            text ("Хаалттай" if visitor == "Bayra" else "Шалгасан" if selected_item and shelter_inspection_done(visitor, selected_item) else "Шалгаж байна" if selected_item else "Эд зүйлээ сонгоно уу"):
                font SHELTER_FONT
                size 23
                color "#514431"
                outlines []
        if visitor == "Bayra":
            button:
                id "inspection_item_business_bag"
                xysize (460, 178)
                background None
                action [SetScreenVariable("selected_item", "business_bag"), SetScreenVariable("revealed", False), Function(viewer.choose, "business_bag")]

    frame:
        xpos 1395
        ypos 340
        xsize 460
        background Frame("gui/shelter/metal/button.png", 28, 18)
        padding (29, 25)
        hbox:
            spacing 17
            add "gui/shelter/inspection/" + ("lock" if visitor == "Bayra" else "check" if revealed else "info") + ".svg" xysize (47, 47)
            text (selected["detail"] if revealed else selected["description"] if selected else bag["note"]):
                style "inspection_text"
                size 25
                xsize 335
                line_spacing 4

    add Solid("#08080760") xpos 0 ypos 905 xysize (1920, 175)
    add Solid("#a88c5944") xpos 64 ypos 905 xysize (1792, 1)
    fixed:
        xpos 64
        ypos 938
        xysize (510, 94)
        if selected:
            if selected_item == "notebook":
                if 2 not in shelter_asked:
                    use inspection_plate(
                        "Зургийн тухай асуух",
                        "inspect",
                        Return("ask_drawing"),
                        width=510
                    )
                else:
                    use inspection_plate(
                        "Шалгасан",
                        "check",
                        NullAction(),
                        enabled=False,
                        width=510
                    )
            else:
                use inspection_plate(
                    selected.get("close_action", "Шалгасан") if revealed else selected["action"],
                    "check" if revealed and "revealed_sprite" not in selected else "inspect",
                    [
                        Function(shelter_inspection_mark, visitor, selected_item),
                        SetScreenVariable("revealed", not revealed),
                        Function(
                            viewer.choose,
                            selected_item if revealed else selected.get("revealed_sprite", selected_item)
                        )
                    ],
                    enabled=not revealed or "revealed_sprite" in selected,
                    width=510
                )
        else:
            use inspection_plate(
                "Эд зүйлээ сонгоно уу",
                "inspect",
                NullAction(),
                enabled=False,
                width=510
            )

    hbox:
        xpos 700
        ypos 937
        spacing 15
        for icon, caption, command in [
                ("left", "Зүүн", Function(viewer.turn, -15)),
                ("right", "Баруун", Function(viewer.turn, 15)),
                ("minus", "−", Function(viewer.zoom, -0.15)),
                ("plus", "+", Function(viewer.zoom, 0.15)),
                ("reset", "Төвлөрүүлэх", Function(viewer.reset))]:
            button:
                id ("inspection_" + icon)
                xysize (88, 88)
                padding (0, 0)
                background "gui/shelter/inspection/round.svg"
                hover_background Transform("gui/shelter/inspection/round.svg", matrixcolor=BrightnessMatrix(0.16))
                action command
                tooltip caption
                alt caption
                add "gui/shelter/inspection/" + icon + ".svg" xysize (62, 62) align (0.5, 0.5)
    text "Чирж эргүүлэх · Дугуйгаар томруулах" style "inspection_text" size 20 color "#b3a58e" xalign 0.5 ypos 1040
    fixed:
        xpos 1435
        ypos 938
        xysize (420, 94)
        use inspection_plate("ҮЗЛЭГ ДУУСГАХ", "exit", Return("close"), width=420)
    key "game_menu" action Return("close")
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    key "K_LEFT" action Function(viewer.turn, -15)
    key "K_RIGHT" action Function(viewer.turn, 15)
    key "K_EQUALS" action Function(viewer.zoom, 0.15)
    key "K_MINUS" action Function(viewer.zoom, -0.15)
    use shelter_protocol_button

label shelter_inspect_belongings:
    $ shelter_hold_current_frame()
    window hide None
    $ _skipping = False
    # Anu's bag request plays once; her separate drawing question follows only
    # after opening the notebook. Closing early must not consume answer three.
    if shelter_visitor == "anu" and 2 not in shelter_asked and "anu" not in shelter_inspection_requests:
        call shelter_player_line("question3", shelter_data("questions")[2])
        $ shelter_inspection_requests = shelter_inspection_requests + ["anu"]
    # Anu's third answer is about the drawing; find it before asking her.
    if shelter_visitor != "anu" and 2 not in shelter_asked:
        call shelter_player_line("question3", shelter_data("questions")[2]) from _call_shelter_player_line
        call shelter_clip("answer3") from _call_shelter_clip
        $ shelter_asked.append(2)
    # A save made during this screen must retain checked items, instead of
    # rolling data back to the beginning of the call-screen statement.
    $ renpy.retain_after_load()
    call screen shelter_inspection(shelter_visitor) with Dissolve(0.2)
    if _return == "ask_drawing" and shelter_visitor == "anu":
        call shelter_player_line("notebook", "Чи энэ зургийг зурсан уу?") from _call_shelter_player_line_1
        call shelter_clip("answer3") from _call_shelter_clip_1
        $ shelter_asked.append(2)
    return
