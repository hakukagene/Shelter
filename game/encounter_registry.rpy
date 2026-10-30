# Visitor registry. Each character file registers its own clips, dialogue and
# quirks with shelter_register_visitor(); shared encounter code reads those
# fields instead of testing visitor names. Adding a visitor touches one file.

init -1 python:
    SHELTER_VISITORS = {}

    # Unarmed waiting states share one still unless a visitor overrides them.
    SHELTER_IDLE_CLIPS = ("intro", "answer1", "answer2", "answer3", "lower")
    SHELTER_DEFAULT_ARMED_ACTIONS = (("Буудах", "shoot", "shoot"), ("Буугаа буулгах", "lower", "lower"))
    SHELTER_DEFAULT_FINAL_CHOICES = ("admit", "reject", "shoot")

    def shelter_register_visitor(visitor, roster_position, civilian, clips, questions,
            lines, windows, voices=None, supplied_voices=None,
            stills="transitions", idle_still=None, idle_clips=SHELTER_IDLE_CLIPS,
            frame_clips=None, frame_fallback="intro", still_aliases=None,
            posters=None, poster_states=None, first_still="intro",
            subtitle_y=710, subtitle_size=30, conversations=None,
            monster_ending=None, nonlethal_shoot=False,
            armed_actions=SHELTER_DEFAULT_ARMED_ACTIONS,
            final_choices=SHELTER_DEFAULT_FINAL_CHOICES, visits=1,
            choice_label=None, hooks=None):
        """
        `roster_position` keeps the original sequence used by saves that
        predate the random visitor order. `civilian` is True, False (monster)
        or None for a pair whose bookkeeping lives in `hooks`.

        Waiting stills use one of three `stills` sources:
        "transitions": extracted movie frames; `idle_still` is (clip, edge).
        "frames": images/<visitor>/frames/<name>.jpg; `idle_still` is a name,
            `frame_clips` optionally limits other names to `frame_fallback`.
        "posters": authored `posters` chosen by `poster_states`.

        `conversations` maps a question index to a label that replaces the
        usual player line + answer clip. `hooks` may override can_ask, can_aim,
        admitted_monster, record_outcome, rejected_civilians and fatal_shots.
        """
        if visitor in SHELTER_VISITORS:
            raise Exception("Visitor registered twice: " + visitor)
        if any(data["roster_position"] == roster_position for data in SHELTER_VISITORS.values()):
            raise Exception("Duplicate roster position %d for %s" % (roster_position, visitor))
        if civilian is False and not monster_ending:
            raise Exception("Monster visitor needs a monster_ending: " + visitor)
        if stills not in ("transitions", "frames", "posters"):
            raise Exception("Unknown stills source for %s: %s" % (visitor, stills))
        if stills == "posters" and not (posters and poster_states):
            raise Exception("Poster stills need posters and poster_states: " + visitor)
        SHELTER_VISITORS[visitor] = {
            "roster_position": roster_position,
            "civilian": civilian,
            "clips": clips,
            "questions": questions,
            "lines": lines,
            "windows": windows,
            # Supplied recordings override earlier shared/placeholder voices.
            "voices": dict(voices or {}, **(supplied_voices or {})),
            "supplied_voices": supplied_voices or {},
            "stills": stills,
            "idle_still": idle_still,
            "idle_clips": idle_clips,
            "frame_clips": frame_clips,
            "frame_fallback": frame_fallback,
            "still_aliases": still_aliases or {},
            "posters": posters,
            "poster_states": poster_states,
            "first_still": first_still,
            "subtitle_y": subtitle_y,
            "subtitle_size": subtitle_size,
            "conversations": conversations or {},
            "monster_ending": monster_ending,
            "nonlethal_shoot": nonlethal_shoot,
            "armed_actions": armed_actions,
            "final_choices": final_choices,
            "visits": visits,
            "choice_label": choice_label,
            "hooks": hooks or {},
        }

    def shelter_data(key, visitor=None):
        return SHELTER_VISITORS[visitor or shelter_visitor][key]

    def shelter_hook(name, visitor=None):
        return SHELTER_VISITORS[visitor or shelter_visitor]["hooks"].get(name)

# Character files register at init 1, after their own defines at init 0.
# Derived tables are built once every registration has run.
init 2 python:
    # Available roster, also the original sequence for saves predating random order.
    SHELTER_VISITOR_ORDER = tuple(sorted(SHELTER_VISITORS,
        key=lambda visitor: SHELTER_VISITORS[visitor]["roster_position"]))
    # Pairs (civilian None) are counted per person by their own hooks.
    SHELTER_CIVILIANS = {visitor: data["civilian"] for visitor, data in SHELTER_VISITORS.items()
        if data["civilian"] is not None}
    # Armor stops the bullet: the visitor leaves alive after being shot.
    SHELTER_NONLETHAL_SHOOT = tuple(visitor for visitor in SHELTER_VISITOR_ORDER
        if SHELTER_VISITORS[visitor]["nonlethal_shoot"])
