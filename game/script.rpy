# A new game opens with the story film, then the first visitor.
label start:
    call shelter_intro from _call_shelter_intro
    call screen shelter_protocol(briefing=True)
    call shelter_encounter from _call_shelter_encounter
    return
