# The selected ledger artwork contains only its title and three row labels.
# Counts and clock digits are live, with no gameplay mutation during rendering.
transform shelter_ledger_ink:
    rotate -4.0
    rotate_pad False

transform shelter_clock_angle:
    rotate -4.0
    rotate_pad False

style shelter_ledger_number is default:
    font "fonts/ShelterLedgerDigits.ttf"
    italic True
    size 132
    color "#29221bea"
    outlines []

screen shelter_transition_status():
    add "gui/shelter/intermission/ledger.jpg" xysize (1920, 1080)

    # Positions match the three blank cells in the photographed paper.
    for amount, center, ink in [
        (shelter_visitors_seen, (1276, 444), "#29221bea"),
        (shelter_admitted, (1296, 622), "#29221bea"),
        (shelter_killed_total(), (1316, 804), "#691e22ec")]:
        text str(amount):
            style "shelter_ledger_number"
            color ink
            pos center
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
