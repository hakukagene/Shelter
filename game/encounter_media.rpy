# Movies, stills and audio channels shared by every encounter.

# The supplied Bayra aim movie ends with one black frame after speech.
# Stop before that frame; keep the original source and audio untouched.
define SHELTER_CLIP_STARTS = {
    "margad/answer1_part2": 13.140,
    "margad/answer1_part3": 17.740,
}
define SHELTER_CLIP_ENDS = {
    "Bayra/aim": 13.11,
    "margad/answer1": 11.525,
    "margad/answer1_part2": 16.414,
    "margad/answer1_part3": 22.040,
}

init 1 python:
    renpy.music.register_channel("shelter_knock", mixer="sfx", loop=False, stop_on_mute=False)
    renpy.music.register_channel("shelter_player", mixer="voice", loop=False, stop_on_mute=False)
    # Muting dialogue must silence the soundtrack, not stop/skip the movie.
    # Movie channels must not pre-buffer the next file like audio-only channels.
    renpy.music.register_channel(
        "shelter_video", mixer="voice", loop=False, movie=True,
        stop_on_mute=False, buffer_queue=False)

    def shelter_wait_image(clip, visitor=None):
        # The still behind the choice buttons after `clip`. Unarmed waiting
        # states share the visitor's idle still, including old saves that
        # stopped on an answer whose last frame is a different framing.
        visitor = visitor or shelter_visitor
        data = SHELTER_VISITORS[visitor]
        if data["stills"] == "posters":
            return shelter_poster(visitor, clip)
        if data["stills"] == "frames":
            if clip in data["idle_clips"]:
                name = data["idle_still"]
            else:
                name = data["still_aliases"].get(clip, clip)
                if data["frame_clips"] is not None and name not in data["frame_clips"]:
                    name = data["frame_fallback"]
            return "images/" + visitor + "/frames/" + name + ".jpg"
        if clip in data["idle_clips"] or clip not in data["clips"]:
            idle_clip, idle_edge = data["idle_still"]
            return shelter_movie_frame(visitor, idle_clip, idle_edge)
        return shelter_movie_frame(visitor, clip, "end")

    def shelter_poster(visitor, clip, edge="end"):
        data = SHELTER_VISITORS[visitor]
        states = data["poster_states"].get(clip, ("idle", "idle"))
        return data["posters"][states[0 if edge == "start" else 1]]

    def shelter_video_end(clip, visitor=None):
        visitor = visitor or shelter_visitor
        if shelter_clip_is_terminal(clip) and clip in SHELTER_VISITORS[visitor]["clips"]:
            return Transform(shelter_movie_frame(visitor, clip, "end"), xysize=(1920, 1080))
        return Transform(shelter_wait_image(clip, visitor), xysize=(1920, 1080))

    def shelter_hold_current_frame():
        # Run before Return removes the clicked screen, including old saves
        # that have never passed through the new playback/backdrop code.
        renpy.show("shelter_hold", what=shelter_video_end(shelter_still))

    def shelter_movie_frame(visitor, clip, edge):
        # Visitors with authored posters have no extracted transition frames.
        if SHELTER_VISITORS[visitor]["stills"] == "posters":
            return shelter_poster(visitor, clip, edge)
        return "images/transitions/" + visitor + "/" + clip + "-" + edge + ".jpg"

    def shelter_movie_start_image(visitor, clip):
        return shelter_movie_frame(visitor, clip, "start")

    def shelter_movie_path(visitor, clip):
        path = "Video/" + visitor + "/" + SHELTER_VISITORS[visitor]["clips"][clip][0]
        start = SHELTER_CLIP_STARTS.get(visitor + "/" + clip)
        end = SHELTER_CLIP_ENDS.get(visitor + "/" + clip)
        bounds = (("from %s " % start) if start is not None else "") + (("to %s" % end) if end is not None else "")
        return ("<%s>" % bounds.strip() if bounds else "") + path

    def shelter_speech_position(clip):
        position = renpy.music.get_pos(channel="shelter_video")
        start = SHELTER_CLIP_STARTS.get(shelter_visitor + "/" + clip)
        # Ren'Py backends can report either source time or time since <from>.
        if position is not None and start is not None and position < start:
            position += start
        return position

    def shelter_movie_for(visitor, clip):
        # A saved/older movie cache can predate newly registered visitors.
        # Populate missing entries on demand instead of crashing with KeyError.
        key = (visitor, clip)
        if key not in shelter_movies:
            shelter_movies[key] = Movie(
                play=shelter_movie_path(visitor, clip),
                channel="shelter_video", loop=False, size=(1920, 1080),
                start_image=Transform(shelter_movie_start_image(visitor, clip), xysize=(1920, 1080)),
                image=Transform(shelter_movie_frame(visitor, clip, "end"), xysize=(1920, 1080)),
                keep_last_frame=True)
        return shelter_movies[key]

# Every registered visitor's clips are known once init 1 has finished.
init 2 python:
    shelter_movies = {
        (visitor, key): Movie(
            play=shelter_movie_path(visitor, key),
            channel="shelter_video", loop=False, size=(1920, 1080),
            start_image=Transform(shelter_movie_start_image(visitor, key), xysize=(1920, 1080)),
            image=Transform(shelter_movie_frame(visitor, key, "end"), xysize=(1920, 1080)),
            keep_last_frame=True)
        for visitor, encounter in SHELTER_VISITORS.items()
        for key, data in encounter["clips"].items()
    }
