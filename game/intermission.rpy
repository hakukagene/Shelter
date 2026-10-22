# Presentation only: the encounter screen owns the knock and transition timers.
style shelter_status_label is default:
    font SHELTER_FONT
    size 27
    color "#bcb7ad"
    outlines []

style shelter_status_number is shelter_status_label:
    font SHELTER_BOLD
    size 78
    color "#eee5d4"

screen shelter_transition_status():
    add Solid("#070809")

    # A recessed steel console with quiet red edge lighting.
    add Solid("#5e161a") xpos 238 ypos 163 xysize (1444, 4)
    frame:
        xpos 240
        ypos 168
        xysize (1440, 744)
        padding (0, 0)
        background Frame("gui/shelter/metal/panel.jpg", 32, 32)
        at shelter_fade

        add Solid("#07090bc4") xpos 26 ypos 26 xysize (1388, 692)
        add Solid("#b52e35") xpos 60 ypos 53 xysize (6, 25)
        text "ХОРОГДОХ БАЙР":
            style "shelter_status_label"
            font SHELTER_BOLD
            size 27
            color "#e5dccb"
            xpos 82
            ypos 48
        text "ЭЭЛЖИЙН БҮРТГЭЛ":
            style "shelter_status_label"
            size 22
            color "#827f79"
            xpos 1376
            xanchor 1.0
            ypos 52
        add Solid("#7e756033") xpos 64 ypos 102 xysize (1312, 1)

        text "ШӨНИЙН ЭЭЛЖ":
            style "shelter_status_label"
            size 23
            color "#969185"
            xalign 0.5
            ypos 130
        text SHELTER_NEXT_VISITOR_TIME:
            style "shelter_status_number"
            size 140
            xalign 0.5
            ypos 155
            text_align 0.5

        # These are read-only counters, not buttons.
        for left, caption, amount, limit, accent in [
            (64, "Оруулсан хүн", shelter_admitted, None, "#d5c3a0"),
            (512, "Аврагдсан энгийн иргэн", shelter_civilians_saved, SHELTER_CIVILIAN_TARGET, "#8faf9c"),
            (960, "Алагдсан энгийн иргэн", shelter_civilians_killed, SHELTER_MAX_CIVILIAN_DEATHS, "#d16a6a")]:
            fixed:
                xpos left
                ypos 345
                xysize (416, 216)
                add Solid("#ffffff0b") xysize (416, 216)
                add Solid("#101214") xpos 1 ypos 1 xysize (414, 214)
                add Solid(accent) xpos 24 ypos 0 xysize (48, 2)
                text caption:
                    style "shelter_status_label"
                    size 27
                    xalign 0.5
                    ypos 26
                text (str(amount) if limit is None else "%s {size=36}{color=#89867f}/ %s{/color}{/size}" % (amount, limit)):
                    style "shelter_status_number"
                    color accent
                    xalign 0.5
                    ypos 68
                    text_align 0.5
                if limit == SHELTER_CIVILIAN_TARGET:
                    add Solid("#252c29") xpos 28 ypos 180 xysize (360, 4)
                    if amount > 0:
                        add Solid(accent) xpos 28 ypos 180 xysize (int(360 * min(1.0, float(amount) / limit)), 4)
                elif limit == SHELTER_MAX_CIVILIAN_DEATHS:
                    for mark in range(SHELTER_MAX_CIVILIAN_DEATHS):
                        add Solid(accent if mark < amount else "#3a292b") xpos (28 + mark * 124) ypos 180 xysize (112, 4)
                else:
                    text "ХОРОГДОХ БАЙРАНД":
                        style "shelter_status_label"
                        size 18
                        color "#827e74"
                        xalign 0.5
                        ypos 174

        text "Шалгасан хүн":
            style "shelter_status_label"
            size 26
            xpos 64
            ypos 603
        text "[shelter_visitors_seen] / [SHELTER_TOTAL_VISITORS]":
            style "shelter_status_label"
            font SHELTER_BOLD
            size 29
            color "#ddd5c6"
            xpos 1376
            xanchor 1.0
            ypos 600
        add Solid("#282726") xpos 64 ypos 648 xysize (1312, 4)
        if shelter_visitors_seen > 0:
            add Solid("#a7977d") xpos 64 ypos 648 xysize (int(1312 * min(1.0, float(shelter_visitors_seen) / SHELTER_TOTAL_VISITORS)), 4)
        text "Дараагийн хүнийг хүлээж байна…":
            style "shelter_status_label"
            size 21
            color "#77756e"
            xalign 0.5
            ypos 678
