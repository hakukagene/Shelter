# Safari uses a persistent inline HTML video element. Ren'Py still owns the
# story, choices, saves and audio; the browser owns video decoding and its clock.
init python:
    import json as shelter_web_json

    def shelter_web_begin(path, cues=(), intro=False, poster=None, armed=False):
        payload = {
            "src": "game/" + path.rsplit(".", 1)[0] + ".mp4",
            "cues": cues,
            "intro": intro,
            "poster": "game/" + poster if poster else None,
            "armed": armed,
            "volume": preferences.get_volume("voice"),
            "muted": preferences.get_mute("voice"),
        }
        renpy.emscripten.run_script(
            "window.ShelterVideo.start(" + shelter_web_json.dumps(payload) + ")")

    def shelter_web_tick():
        if renpy.emscripten.run_script_int("window.ShelterVideo.finished ? 1 : 0"):
            renpy.end_interaction(True)

    def shelter_web_close():
        renpy.emscripten.run_script("window.ShelterVideo.close()")

    def shelter_web_clip_cues(clip):
        window = shelter_data("windows").get(clip)
        if not window:
            return ()
        return ((window[0], window[1], "", shelter_data("lines")[clip]),)

screen shelter_web_wait():
    modal True
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    key "game_menu" action NullAction()
    timer 0.05 repeat True action Function(shelter_web_tick)
