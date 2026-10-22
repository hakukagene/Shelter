# A dedicated midpoint slot, never whichever manual/autosave happens to be newest.
define SHELTER_CHECKPOINT_SLOT = "shelter-midpoint-v1"
define SHELTER_CHECKPOINT_TARGET = 20
default shelter_checkpoint_created = False
default shelter_checkpoint_written = False

init python:
    def shelter_has_checkpoint():
        info = renpy.slot_json(SHELTER_CHECKPOINT_SLOT) or {}
        return (info.get("shelter_checkpoint") == 1
            and info.get("civilians_saved", 0) >= SHELTER_CHECKPOINT_TARGET
            and renpy.can_load(SHELTER_CHECKPOINT_SLOT))

    def shelter_write_checkpoint():
        global shelter_checkpoint_written
        if shelter_checkpoint_written:
            return
        # Save from a stable interaction AFTER the twentieth visitor resolves.
        # This flag is in the save, so loading it cannot write it again.
        shelter_checkpoint_written = True
        renpy.retain_after_load()
        renpy.take_screenshot()
        renpy.save(SHELTER_CHECKPOINT_SLOT, extra_info="20 энгийн хүн аварсан", extra_json={
            "shelter_checkpoint": 1, "civilians_saved": shelter_civilians_saved})
        renpy.restart_interaction()

screen shelter_midpoint_checkpoint():
    modal True
    use shelter_transition_status
    frame:
        xalign 0.5
        ypos 940
        padding (30, 18)
        background Frame("gui/shelter/metal/button.png", 20, 16)
        text "20 ЭНГИЙН ХҮН АВАРЛАА · ЯВЦ ХАДГАЛАГДЛАА" style "shelter_text" size 27
    if not shelter_checkpoint_written:
        timer 0.1 action Function(shelter_write_checkpoint)
    else:
        timer 1.0 action Return(True)
    key "dismiss" action NullAction()
    key "game_menu" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()

label shelter_save_midpoint:
    if not shelter_checkpoint_created and shelter_civilians_saved >= SHELTER_CHECKPOINT_TARGET:
        $ shelter_checkpoint_created = True
        $ shelter_checkpoint_written = False
        $ renpy.block_rollback()
        $ renpy.retain_after_load()
        call screen shelter_midpoint_checkpoint
    return
