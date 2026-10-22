# Character belongings are evidence to examine, never an automatic verdict.
# Assets use alpha atlases or standalone cutouts; each prop stays separate.
default shelter_inspection_progress = {}

init python:
    import pygame

    SHELTER_INSPECTION_SPRITES = {
        "delivery_bag": ("containers.png", (0, 90, 580, 770)),
        "school_bag": ("containers.png", (580, 250, 450, 580)),
        "business_bag": ("containers.png", (1040, 245, 496, 585)),
        "meal": ("items.png", (10, 60, 525, 430)),
        "charger": ("items.png", (540, 90, 505, 415)),
        "schedule": ("items.png", (1050, 10, 480, 500)),
        "notebook": ("items.png", (25, 535, 440, 455)),
        "drawing": ("anu-notebook.webp", None),
        "rabbit": ("items.png", (1090, 510, 440, 505)),
    }
    SHELTER_INSPECTION_ITEMS = {
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
            "name": "Зургийн дэвтэр", "action": "Дэвтрийг нээх",
            "description": "Анугийн сургуулийн цүнхэнд байсан жижиг дэвтэр.",
            "detail": "Сүүлийн хуудсанд энэ хорогдох байрны хаалга, дотор талын дугуй түгжээг зуржээ.",
            "revealed_sprite": "drawing", "close_action": "Дэвтрийг хаах",
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
        def __init__(self, **kwargs):
            super(ShelterInspectionView, self).__init__(**kwargs)
            self.sprite = None
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

        def render(self, width, height, st, at):
            rv = renpy.Render(660, 430)
            if self.sprite:
                child = Transform(shelter_inspection_sprite(self.sprite),
                    xysize=(470, 350), fit="contain", zoom=self.magnification,
                    rotate=self.angle, rotate_pad=True)
                rendered = renpy.render(child, 660, 430, st, at)
                w, h = rendered.get_size()
                rv.blit(rendered, ((660-w)/2, (430-h)/2))
            return rv.subsurface((0, 0, 660, 430))

        def event(self, ev, x, y, st):
            inside = 0 <= x < 660 and 0 <= y < 430
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

style inspection_text is shelter_text:
    size 28
    color "#e4ded2"

style inspection_button is shelter_button:
    padding (18, 12)
    xminimum 100
    yminimum 64

style inspection_button_text is shelter_button_text:
    size 26

screen shelter_inspection(visitor):
    modal True
    default selected_item = None
    default revealed = False
    default viewer = ShelterInspectionView()
    $ bag = SHELTER_INSPECTIONS[visitor]
    $ checked = sum(shelter_inspection_done(visitor, item) for item in bag["items"])

    add "images/inspection/workbench.png" xysize (1920, 1080)
    add Solid("#00000042")
    add Solid("#090b0ee8") xpos 0 ypos 0 xysize (1920, 125)
    add Solid("#a2885c") xpos 64 ypos 124 xysize (1792, 2)
    text "ҮЗЛЭГИЙН ШИРЭЭ" style "inspection_text" font SHELTER_BOLD size 42 xpos 64 ypos 28
    text bag["title"] style "inspection_text" size 25 color "#ada69b" xpos 67 ypos 80
    text bag["owner"] style "inspection_text" size 30 xanchor 1.0 xpos 1850 ypos 45

    # The character's own container sits on the desk, with loose objects nearby.
    if visitor != "Bayra":
        add Transform(shelter_inspection_sprite(bag["bag"]), xysize=(530, 650), fit="contain") xpos 84 ypos 225
    $ spots = [(665, 255), (750, 475), (620, 710)] if len(bag["items"]) == 3 else [(660, 330), (725, 625)]
    for i, item_id in enumerate(bag["items"]):
        $ item = SHELTER_INSPECTION_ITEMS[item_id]
        $ is_bag = item_id == "business_bag"
        $ spot = (225, 310) if is_bag else spots[i]
        button:
            id ("inspection_item_" + item_id)
            xpos spot[0]
            ypos spot[1]
            xysize ((640, 530) if is_bag else (265, 210))
            padding (8, 8)
            background None
            hover_background Solid("#eed4a21a")
            selected_background Solid("#eed4a20d")
            selected selected_item == item_id
            action [SetScreenVariable("selected_item", item_id), SetScreenVariable("revealed", False), Function(viewer.choose, item_id)]
            vbox:
                spacing 8
                xalign 0.5
                add Transform(shelter_inspection_sprite(item_id), xysize=((580, 440) if is_bag else (235, 150)), fit="contain") xalign 0.5
                text item["name"] style "inspection_text" size 24 text_align 0.5 xalign 0.5
                if shelter_inspection_done(visitor, item_id):
                    text "ШАЛГАСАН" style "inspection_text" size 17 color "#bfa776" xalign 0.5

    frame:
        xpos 1080
        ypos 155
        xysize (776, 785)
        background Solid("#090b0ee3")
        padding (42, 28)
        if selected_item is None:
            vbox:
                yalign 0.5
                spacing 24
                text "ЭД ЗҮЙЛЭЭ СОНГОНО УУ" style "inspection_text" font SHELTER_BOLD size 32
                text bag["note"] style "inspection_text" xsize 670
                text "Дарж авах · Томруулах · Чирж эргүүлэх" style "inspection_text" size 23 color "#ada69b"
        else:
            $ selected = SHELTER_INSPECTION_ITEMS[selected_item]
            text selected["name"] style "inspection_text" font SHELTER_BOLD size 34
            add viewer xpos 0 ypos 65
            text "Чирж эргүүлэх · Дугуйгаар томруулах" style "inspection_text" size 21 color "#a9a395" xpos 0 ypos 500
            hbox:
                ypos 535
                spacing 10
                textbutton "Зүүн" style "inspection_button" action Function(viewer.turn, -15)
                textbutton "Баруун" style "inspection_button" action Function(viewer.turn, 15)
                textbutton "−" style "inspection_button" action Function(viewer.zoom, -0.15)
                textbutton "+" style "inspection_button" action Function(viewer.zoom, 0.15)
                textbutton "Тавих" style "inspection_button" action [SetScreenVariable("selected_item", None), Function(viewer.choose, None)]
            text (selected["detail"] if revealed else selected["description"]):
                style "inspection_text"
                size 25
                xpos 0
                ypos 613
                xsize 680
            if selected_item == "notebook" and revealed and 2 not in shelter_asked:
                textbutton "Энэ зургийн тухай асуух":
                    style "inspection_button"
                    xpos 0 ypos 700 xsize 680
                    action Return("ask_drawing")
            else:
                textbutton (selected.get("close_action", "Шалгасан") if revealed else selected["action"]):
                    style "inspection_button"
                    xpos 0 ypos 700 xsize 680
                    sensitive not revealed or "revealed_sprite" in selected
                    action [Function(shelter_inspection_mark, visitor, selected_item), SetScreenVariable("revealed", not revealed), Function(viewer.choose, selected_item if revealed else selected.get("revealed_sprite", selected_item))]

    add Solid("#090b0eee") xpos 0 ypos 965 xysize (1920, 115)
    textbutton "ҮЗЛЭГ ДУУСГАХ":
        style "inspection_button"
        xpos 1500 ypos 986 xysize (355, 70)
        action Return("close")
    key "game_menu" action Return("close")
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    if selected_item:
        key "K_LEFT" action Function(viewer.turn, -15)
        key "K_RIGHT" action Function(viewer.turn, 15)
        key "K_EQUALS" action Function(viewer.zoom, 0.15)
        key "K_MINUS" action Function(viewer.zoom, -0.15)

label shelter_inspect_belongings:
    $ shelter_hold_current_frame()
    window hide None
    $ _skipping = False
    # Anu's third answer is about the drawing; find it before asking her.
    if shelter_visitor != "anu" and 2 not in shelter_asked:
        call shelter_player_line("question3", shelter_data("questions")[2]) from _call_shelter_player_line
        call shelter_clip("answer3") from _call_shelter_clip
        $ shelter_asked.append(2)
    # A save made during this screen must retain checked items, instead of
    # rolling data back to the beginning of the call-screen statement.
    $ renpy.retain_after_load()
    call screen shelter_inspection(shelter_visitor) with Dissolve(0.2)
    if _return == "ask_drawing" and shelter_visitor == "anu" and 2 not in shelter_asked:
        call shelter_player_line("drawing", "Чи энэ зургийг зурсан уу?") from _call_shelter_player_line_1
        call shelter_clip("answer3") from _call_shelter_clip_1
        $ shelter_asked.append(2)
    return
