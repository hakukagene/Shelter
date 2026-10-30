# Campaign rules: roster order, the story clock and outcome bookkeeping.
# Visitor-specific rules come from the registry (encounter_registry.rpy).
# Design totals for the full campaign. The registered roster is smaller until
# every visitor's footage is supplied; the preview ending covers that case.
define SHELTER_CIVILIAN_COUNT = 43
define SHELTER_MONSTER_COUNT = 30
define SHELTER_TOTAL_VISITORS = SHELTER_CIVILIAN_COUNT + SHELTER_MONSTER_COUNT
define SHELTER_CIVILIAN_TARGET = 40
define SHELTER_MAX_CIVILIAN_DEATHS = 2
define SHELTER_MAX_CIVILIAN_MISTAKES = 2
default shelter_run_order = None
default shelter_outcomes = {}
default shelter_admitted = 0
default shelter_civilians_saved = 0
default shelter_civilians_killed = 0
default shelter_visitors_seen = 0
# None gives older saves a stable time derived from their completed visits.
default shelter_story_minutes = None

define SHELTER_CLOCK_START = 23 * 60 + 10

init 1 python:
    def shelter_make_visitor_order():
        # Shuffle once per new game/replay, using Ren'Py's rollback-aware RNG.
        order = list(SHELTER_VISITOR_ORDER)
        renpy.random.shuffle(order)
        return order

    def shelter_next_visitor_id():
        # Old saves keep their original remaining sequence. Never reshuffle on
        # load, during a movie, or while displaying the clock between visitors.
        order = shelter_run_order or SHELTER_VISITOR_ORDER
        remaining = order[order.index(shelter_visitor) + 1:]
        return next((visitor for visitor in remaining if visitor not in shelter_outcomes), None)

    def shelter_clock_minutes():
        if shelter_story_minutes is None:
            return SHELTER_CLOCK_START + 7 * shelter_visitors_seen
        return shelter_story_minutes

    def shelter_clock_text():
        minutes = shelter_clock_minutes() % (24 * 60)
        return "%02d:%02d" % (minutes // 60, minutes % 60)

    def shelter_hooked_total(name):
        # Visitors with their own bookkeeping (the pair) report their counts.
        return sum(data["hooks"][name]() for data in SHELTER_VISITORS.values()
            if name in data["hooks"])

    def shelter_killed_total():
        # Total fatal shots, including monsters, for encounter bookkeeping.
        # The ledger displays shelter_civilians_killed instead. Orgil survives.
        return sum(choice == "shoot" and visitor not in SHELTER_NONLETHAL_SHOOT
                for visitor, choice in shelter_outcomes.items()
                if "fatal_shots" not in SHELTER_VISITORS.get(visitor, {}).get("hooks", {})
            ) + shelter_hooked_total("fatal_shots")

    def shelter_record_outcome(visitor, choice):
        # Copy-on-write supports saves/rollback; one outcome per visitor.
        global shelter_outcomes, shelter_admitted, shelter_civilians_saved
        global shelter_civilians_killed, shelter_visitors_seen, shelter_story_minutes
        if visitor in shelter_outcomes:
            return
        if choice not in shelter_data("final_choices", visitor):
            raise ValueError("Not a final decision: " + str(choice))
        # Advance once per resolved visitor, never during screen prediction or
        # redraw. Ren'Py saves/rolls back both this value and its random state.
        elapsed = 7 if shelter_visitors_seen == 0 else renpy.random.randint(4, 9)
        shelter_story_minutes = shelter_clock_minutes() + elapsed
        shelter_outcomes = dict(shelter_outcomes, **{visitor: choice})
        shelter_visitors_seen += shelter_data("visits", visitor)
        record = shelter_hook("record_outcome", visitor)
        if record:
            record(choice)
            return
        civilian = SHELTER_CIVILIANS[visitor]
        if choice == "admit":
            shelter_admitted += 1
            if civilian:
                shelter_civilians_saved += 1
        elif choice == "shoot" and civilian and visitor not in SHELTER_NONLETHAL_SHOOT:
            shelter_civilians_killed += 1

    def shelter_civilians_rejected():
        # Derive from saved outcomes: includes armored Orgil leaving after a
        # nonlethal shot and the civilian man lost when the pair is expelled.
        # Monsters and admitted civilians never enter this count.
        rejected = sum(SHELTER_CIVILIANS.get(visitor, False) and
            (choice == "reject" or (choice == "shoot" and visitor in SHELTER_NONLETHAL_SHOOT))
            for visitor, choice in shelter_outcomes.items())
        return rejected + shelter_hooked_total("rejected_civilians")

    def shelter_civilian_mistakes():
        return shelter_civilians_killed + shelter_civilians_rejected()

    def shelter_campaign_status():
        if shelter_civilian_mistakes() > SHELTER_MAX_CIVILIAN_MISTAKES:
            return "casualties"
        if shelter_civilians_saved >= SHELTER_CIVILIAN_TARGET:
            return "win"
        if shelter_visitors_seen >= SHELTER_TOTAL_VISITORS:
            return "shortfall"
        return "continue"

    # Per-visitor rules default to the single-visitor encounter; hooks override.
    def shelter_can_ask_questions():
        hook = shelter_hook("can_ask")
        return hook() if hook else True

    def shelter_can_aim():
        hook = shelter_hook("can_aim")
        return hook() if hook else True

    def shelter_action_choices(armed=False):
        if armed:
            return list(shelter_data("armed_actions"))
        return [("Хөөх", "reject", "reject"), ("Оруулах", "admit", "admit")]

    def shelter_clip_is_terminal(clip):
        return clip in ("shoot", "admit", "reject", "man_admit", "man_reject", "woman_admit", "woman_reject")

    def shelter_clip_is_armed(clip):
        return clip in ("aim", "shoot", "lower", "shoot_man", "shoot_woman")

    def shelter_admitted_monster():
        hook = shelter_hook("admitted_monster")
        if hook:
            return hook()
        return shelter_choice == "admit" and not SHELTER_CIVILIANS[shelter_visitor]
