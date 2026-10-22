# Only the title is baked into the paper. Labels, counts and clock stay live.
# Text follows the paper's ruled lines instead of leaning in italic type.
transform shelter_ledger_ink:
    rotate -4.0
    rotate_pad False

transform shelter_clock_angle:
    rotate -4.0
    rotate_pad False

style shelter_ledger_number is default:
    font "fonts/ShelterLedgerDigits.ttf"
    size 92
    color "#29221bea"
    outlines []

style shelter_ledger_label is default:
    font "fonts/ShelterLedgerLabels.ttf"
    size 48
    color "#29221bea"
    outlines []
    line_spacing 2

screen shelter_transition_status():
    add "gui/shelter/intermission/ledger.jpg" xysize (1920, 1080)

    # Each center follows the notebook's diagonal column. Digits are 70% of
    # their previous 132px size, with the same -4 degree baseline as the rules.
    for caption, amount, label_pos, number_pos, ink, counter_id in [
        ("Шалгасан хүн", shelter_visitors_seen, (634, 460), (1260, 444), "#29221bea", "ledger_checked"),
        ("Хөөж явуулсан\nэнгийн иргэн", shelter_civilians_rejected(), (642, 638), (1284, 622), "#29221bea", "ledger_rejected"),
        ("Алсан\nэнгийн иргэн", shelter_civilians_killed, (650, 820), (1308, 804), "#691e22ec", "ledger_killed")]:
        text caption:
            style "shelter_ledger_label"
            color ink
            pos label_pos
            anchor (0.0, 0.5)
            at shelter_ledger_ink
        text str(amount):
            id counter_id
            style "shelter_ledger_number"
            color ink
            pos number_pos
            anchor (0.5, 0.5)
            at shelter_ledger_ink

    # A small original seven-segment font keeps the alarm clock dynamic.
    for digits, lit in [("88:88", False), (shelter_clock_text(), True)]:
        text digits:
            font "fonts/ShelterClock.ttf"
            size 103
            color ("#ff8450" if lit else "#4d180b55")
            outlines ([(6, "#ff2c091b", 0, 0), (3, "#ff3d1660", 0, 0), (1, "#ff5228", 0, 0)] if lit else [])
            pos (978, 135)
            anchor (0.5, 0.5)
            at shelter_clock_angle
