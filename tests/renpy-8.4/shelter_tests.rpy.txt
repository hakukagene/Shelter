testcase shelter_flow:
    $ _test.timeout = 40.0
    run Start()
    pause 1.0
    assert renpy.get_screen("shelter_playback")
    click
    pause 1.0
    assert renpy.get_screen("shelter_playback")
    pause 10.0
    assert renpy.get_screen("shelter_questions")
    assert not renpy.get_screen("shelter_decision")
    "01" pos (0.5, 0.5)
    pause 8.0
    assert renpy.get_screen("shelter_decision")
    assert shelter_asked == [0]
    "Дахин асуулт" pos (0.5, 0.5)
    pause 0.5
    "02" pos (0.5, 0.5)
    pause 7.0
    assert shelter_asked == [0, 1]
    "Буу онилох" pos (0.5, 0.5)
    pause 13.0
    assert renpy.get_screen("shelter_decision")
    assert shelter_still == "aim"
    "Буугаа буулгах" pos (0.5, 0.5)
    pause 4.0
    assert shelter_still == "lower"
    "Хөөж явуулах" pos (0.5, 0.5)
    pause 0.5
    assert renpy.get_screen("shelter_result")
    "Дахин тоглох" pos (0.5, 0.5)
    pause 11.0
    assert shelter_asked == []
    "03" pos (0.5, 0.5)
    pause 7.0
    assert shelter_asked == [2]
    "Дотогш оруулах" pos (0.5, 0.5)
    pause 0.5
    assert renpy.get_screen("shelter_result")
    $ renpy.quit()

testcase shelter_shoot:
    $ _test.timeout = 40.0
    run Start()
    pause 11.0
    "01" pos (0.5, 0.5)
    pause 7.0
    "Буу онилох" pos (0.5, 0.5)
    pause 13.0
    "Буудах" pos (0.5, 0.5)
    pause 9.0
    assert shelter_still == "shoot"
    assert renpy.get_screen("shelter_result")
    $ renpy.quit()
