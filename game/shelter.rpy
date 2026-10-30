# Encounter flow labels. Shared screens, media and rules live in
# encounter_screens.rpy, encounter_media.rpy and campaign.rpy; each visitor's
# data and quirks are registered in that visitor's own file.
# Keep these labels in this file: saves refer to their statements by file.
default shelter_still = "intro"
default shelter_asked = []
default shelter_choice = None
# Keep Maral as the default for saves made before the two-visitor sequence.
default shelter_visitor = "Maral"
# No longer read; kept so the name stays defined for older saves.
default shelter_chinba_outcome = None

label shelter_player_line(voice_key, caption=None):
    # New characters may have response video audio before player voice is supplied.
    if shelter_player_voice(voice_key) is None:
        return
    $ shelter_hold_current_frame()
    window hide None
    $ _skipping = False
    $ renpy.music.play(shelter_player_voice(voice_key)[0], channel="shelter_player", loop=False)
    call screen shelter_player_speech(voice_key, caption)
    $ renpy.music.stop(channel="shelter_player")
    return

label shelter_clip(clip):
    window hide None
    $ _skipping = False
    if not renpy.showing("shelter_hold"):
        # Also repair saves created before a persistent backdrop existed.
        scene expression Transform(shelter_movie_start_image(shelter_visitor, clip), xysize=(1920, 1080)) as shelter_hold
        with None
    hide screen shelter_transition_status
    # A called screen is transient. Keep an opaque image on the master layer
    # too, so screen removal, loading and transitions never expose scene black.
    scene expression Transform(shelter_movie_start_image(shelter_visitor, clip), xysize=(1920, 1080)) as shelter_hold
    # Finish the transition using stills before the decoder starts. A live
    # Movie inside Dissolve can expose an uninitialised video render target.
    with Dissolve(0.6 if clip == "intro" else 0.16)
    if renpy.emscripten:
        $ shelter_web_begin("Video/" + shelter_visitor + "/" + shelter_data("clips")[clip][0], shelter_web_clip_cues(clip), poster=shelter_movie_start_image(shelter_visitor, clip), armed=shelter_clip_is_armed(clip), start_time=SHELTER_CLIP_STARTS.get(shelter_visitor + "/" + clip), end_time=SHELTER_CLIP_ENDS.get(shelter_visitor + "/" + clip), end_poster=shelter_movie_frame(shelter_visitor, clip, "end"))
        call screen shelter_web_wait
    else:
        call screen shelter_playback(clip)
    $ shelter_still = clip
    scene expression Transform(shelter_movie_frame(shelter_visitor, clip, "end"), xysize=(1920, 1080)) as shelter_hold
    call screen shelter_clip_handoff(clip)
    scene expression shelter_video_end(clip) as shelter_hold
    return

# The first line starts one continuous response movie. Its two follow-up
# questions are buttons shown while that movie is paused.
label shelter_margad_answer1_conversation:
    call shelter_player_line("question1", MARGAD_QUESTION1_PART1) from _call_shelter_player_line_9
    window hide None
    $ _skipping = False
    scene expression Transform(shelter_movie_frame("margad", "answer1", "start"), xysize=(1920, 1080)) as shelter_hold
    with Dissolve(0.16)
    if renpy.emscripten:
        $ shelter_web_begin(
            "Video/margad/Chotgor hariult 1.webm",
            ((1.073, 11.525, "", MARGAD_LINES["answer1"]),
            (13.140, 16.414, "", MARGAD_LINES["answer1_part2"]),
            (17.740, 22.040, "", MARGAD_LINES["answer1_part3"])),
            poster=shelter_movie_frame("margad", "answer1", "start"),
            end_time=22.040,
            end_poster=shelter_movie_frame("margad", "answer1_part3", "end"),
            interjections=(
                (11.525, MARGAD_QUESTION1_PART2, MARGAD_SUPPLIED_PLAYER_VOICES["question1_part2"]),
                (16.414, MARGAD_QUESTION1_PART3, MARGAD_SUPPLIED_PLAYER_VOICES["question1_part3"])))
        call screen shelter_web_wait
    else:
        call screen shelter_margad_answer1_playback
    $ shelter_still = "answer1_part3"
    scene expression Transform(shelter_movie_frame("margad", "answer1_part3", "end"), xysize=(1920, 1080)) as shelter_hold
    call screen shelter_clip_handoff("answer1_part3")
    scene expression shelter_video_end("answer1_part3") as shelter_hold
    return

label shelter_encounter:
    play music "<volume 0.18>audio/Audio/shuum.mp3" fadeout 0.6 fadein 1.0
    $ quick_menu = False
    $ shelter_run_order = shelter_make_visitor_order()
    $ shelter_visitor = shelter_run_order[0]
    $ shelter_outcomes = {}
    $ shelter_deeremchin_outcomes = {}
    $ shelter_admitted = 0
    $ shelter_civilians_saved = 0
    $ shelter_civilians_killed = 0
    $ shelter_visitors_seen = 0
    $ shelter_story_minutes = SHELTER_CLOCK_START
    $ shelter_inspection_progress = {}
    $ shelter_inspection_requests = []
    $ shelter_inspection_views = {}
    $ shelter_checkpoint_created = False
    $ shelter_checkpoint_written = False
    jump shelter_visit_start

label shelter_visit_start:
    $ shelter_asked = []
    $ shelter_choice = None
    $ shelter_still = shelter_data("first_still")
    call shelter_clip("intro") from _call_shelter_clip_2
    jump shelter_question_phase

label shelter_question_phase:
    call screen shelter_questions
    $ shelter_choice = _return
    jump shelter_handle_choice

label shelter_decision_phase:
    call screen shelter_decision
    $ shelter_choice = _return
    jump shelter_handle_choice

label shelter_handle_choice:
    # A visitor with its own decision rules (the pair) handles every choice.
    if shelter_data("choice_label"):
        jump expression shelter_data("choice_label")
    if isinstance(shelter_choice, int):
        if shelter_has_inspection(shelter_visitor, shelter_choice):
            call shelter_inspect_belongings from _call_shelter_inspect_belongings
            jump shelter_decision_phase
        $ shelter_asked.append(shelter_choice)
        if shelter_choice in shelter_data("conversations"):
            # A conversation plays its own player line and paused response movie.
            call expression shelter_data("conversations")[shelter_choice] from _call_shelter_conversation
        else:
            call shelter_player_line("question%d" % (shelter_choice + 1), shelter_data("questions")[shelter_choice]) from _call_shelter_player_line_2
            call shelter_clip("answer%d" % (shelter_choice + 1)) from _call_shelter_clip_3
        jump shelter_decision_phase
    elif shelter_choice == "aim":
        call shelter_clip("aim") from _call_shelter_clip_4
        call screen shelter_decision(armed=True)
        $ shelter_choice = _return
        if shelter_choice == "lower":
            call shelter_clip("lower") from _call_shelter_clip_5
            jump shelter_decision_phase
        elif shelter_choice in ("reject", "admit"):
            call shelter_clip("lower") from _call_shelter_clip_6
        jump shelter_handle_choice
    elif shelter_choice == "shoot":
        call shelter_clip("shoot") from _call_shelter_clip_7
        jump shelter_resolve_visitor
    elif shelter_choice == "reject":
        call shelter_player_line("reject") from _call_shelter_player_line_3
        call shelter_clip("reject") from _call_shelter_clip_8
        jump shelter_resolve_visitor
    elif shelter_choice == "admit":
        call shelter_player_line("admit") from _call_shelter_player_line_4
        call shelter_clip("admit") from _call_shelter_clip_9
        jump shelter_resolve_visitor
    jump shelter_decision_phase

label shelter_resolve_visitor:
    $ shelter_record_outcome(shelter_visitor, shelter_choice)
    $ shelter_status = shelter_campaign_status()
    if shelter_status == "continue" and not shelter_admitted_monster():
        call shelter_save_midpoint from _call_shelter_save_midpoint
    if shelter_status == "casualties":
        $ shelter_mistakes = shelter_civilian_mistakes()
        call screen shelter_result("ТА ХОЖИГДЛОО", "Та [shelter_mistakes] энгийн хүнийг хөнөөсөн эсвэл хөөж явуулсан. Зөвшөөрөгдөх алдааны дээд хэмжээ [SHELTER_MAX_CIVILIAN_MISTAKES].")
    elif shelter_admitted_monster():
        $ shelter_monster_ending = shelter_data("monster_ending")
        call screen shelter_result("ТА АЮУЛЫГ ДОТОГШ ОРУУЛЛАА", shelter_monster_ending)
    elif shelter_status == "win":
        call screen shelter_result("ТА ХОЖЛОО", "Та [SHELTER_CIVILIAN_TARGET] энгийн иргэнийг хорогдох байранд оруулж аварлаа.")
    elif shelter_status == "shortfall":
        call screen shelter_result("ТА ХОЖИГДЛОО", "[SHELTER_TOTAL_VISITORS] хүнийг шалгаж дууслаа. Та [shelter_civilians_saved] / [SHELTER_CIVILIAN_TARGET] энгийн иргэнийг аварсан.")
    elif shelter_next_visitor_id() is not None:
        jump shelter_next_visitor
    else:
        # The available visitor preview is not a complete campaign victory.
        $ shelter_mistakes = shelter_civilian_mistakes()
        call screen shelter_result("ТУРШИЛТЫН ХЭСЭГ ДУУСЛАА", "Оруулсан: [shelter_admitted] • Аврагдсан: [shelter_civilians_saved]/[SHELTER_CIVILIAN_TARGET] • Алдаа: [shelter_mistakes]/[SHELTER_MAX_CIVILIAN_MISTAKES]. Үлдсэн дүрүүд хараахан нэмэгдээгүй.")
    if _return == "replay":
        jump shelter_encounter
    return

label shelter_next_visitor:
    $ renpy.music.stop(channel="shelter_player")
    $ renpy.music.stop(channel="shelter_video")
    $ _skipping = False
    # Blend directly from the departure frame to the ledger; no black stop.
    # Keep its live clock/counts after the transient card returns, so the next
    # visitor dissolves from the ledger rather than the previous departure.
    show screen shelter_transition_status
    call screen shelter_next_visitor_card with Dissolve(0.5)
    $ renpy.music.stop(channel="shelter_knock")
    $ shelter_visitor = shelter_next_visitor_id()
    jump shelter_visit_start
