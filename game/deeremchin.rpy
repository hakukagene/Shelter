# Latest author DOCX: one civilian man and one monster woman arrive together.
# They share one encounter/clock transition, but count as two checked people.
default shelter_deeremchin_outcomes = {}

define DEEREMCHIN_CLIPS = {
    "intro": ("Deeremchin ehlel.webm", 7.528),
    "answer1": ("Deeremchin hariult1.webm", 8.328),
    "answer2": ("Deeremchin hariult2.webm", 11.648),
    "answer3": ("Deeremchin hariult3.webm", 8.048),
    "aim": ("Deeremchin buu tulgah.webm", 15.088),
    "shoot_man": ("Deeremching buudah.webm", 3.048),
    "shoot_woman": ("Huuhniig buudah.webm", 9.088),
    "admit": ("2uulang ni oruulav.webm", 7.048),
    "reject": ("2uulang ni hooj yavuulav.webm", 6.208),
    "man_admit": ("Deeremchin dangaaraa oroh.webm", 9.648),
    "man_reject": ("deeremchin dangaaraa hoogdov.webm", 5.048),
    "woman_admit": ("Huuhniig oruulah.webm", 6.048),
    "woman_reject": ("Emegteig hooh.webm", 5.048),
}

define DEEREMCHIN_QUESTIONS = [
    "Тайван бай. Наад эмэгтэй чинь хэн бэ? Царайг нь харуулаач.",
    "Та хоёрыг тэдний нэг биш гэж би яаж мэдэх юм?",
    "Эмэгтэй та зүгээр үү? Танд юу тохиолдоо вэ?",
]
define DEEREMCHIN_LINES = {
    "intro": "Наад хаалгаа хурдан нээ. Нээхгүй бол энэний хоолойг хэрчлээ шүү.",
    "answer1": "Энд шаардлагыг чи биш би тавина. Хаалгаа нээ. Нээхгүй бол энэ гэмгүй охины үхэлд чи буруутан болно гэж мэдээрэй. Хурдал, хурдал!",
    "answer2": "Би тэдний нэг биш шүү. Энэ хүүхнийг бол мэдэхгүй юм байна. Замдаа тааралдсан юм. Гэхдээ дорой амьтан байна лээ дээ. Чи цэрэг биз дээ. Гэмгүй хүнийг үхүүлбэл шийтгүүлнэ биз дээ.",
    "answer3": "Наадах чинь ярьж чадахгүй ээ. Би амыг нь боочихсон байгаа. Хаалгаа онгойлговол би ороод бууж өгнө өө. Намайг оруулаад хүлсэн ч болно.",
    "aim": "Битгий буудаарай. Энэ эмэгтэй өөрөө санал болгосон юм аа. Энэ хорогдох байрны талаар ч энэ надад хэлсэн. Би зүгээр л түүнтэй тохиролцон жүжиглэж байсан төдий.",
    "shoot_woman": "Ёоё. Чи зөв сонголт хийлээ. Наад хүүхэн чинь надад ч гэсэн эвгүй санагдаад байсан юм. Манийгаа одоо оруулна биз дээ.",
    "man_admit": "За ёстой баярлалаа хөгшөөн. Би ахиж ийм асуудал гаргахгүй ээ.",
    "man_reject": "Новш, новш, новш...",
}
# Audio cues exclude the gunshot and the silent lead-in to the confession.
define DEEREMCHIN_SPEECH_WINDOWS = {
    "intro": (3.668, 7.40),
    "answer1": (0.645, 7.828),
    "answer2": (1.172, 11.316),
    "answer3": (0.374, 7.363),
    "aim": (3.643, 14.067),
    "shoot_woman": (3.157, 8.731),
    "man_admit": (0.658, 3.250),
    "man_reject": (1.348, 3.10),
}
define DEEREMCHIN_PLAYER_VOICES = {
    "question1": ("audio/deeremchin/Chinguun asuult1.mp3", 0.417, 3.278),
    "question2": ("audio/deeremchin/Chinguun asuult2.mp3", 0.502, 3.069),
    "question3": ("audio/deeremchin/Chinguun asuult3.mp3", 0.284, 2.347),
    "reject": ("audio/deeremchin/CHinguun 2uulang ni hoov.mp3", 0.464, 2.152),
}

init python:
    def shelter_deeremchin_survivor():
        if shelter_deeremchin_outcomes.get("man") == "shoot":
            return "woman"
        if shelter_deeremchin_outcomes.get("woman") == "shoot":
            return "man"
        return None

    def shelter_record_deeremchin_person(person, choice):
        # Record a shot immediately, before the survivor decision/save point.
        # Copy-on-write and idempotence prevent double counting on load/rollback.
        global shelter_deeremchin_outcomes, shelter_admitted
        global shelter_civilians_saved, shelter_civilians_killed
        if person in shelter_deeremchin_outcomes:
            return
        shelter_deeremchin_outcomes = dict(shelter_deeremchin_outcomes, **{person: choice})
        if choice == "admit":
            shelter_admitted += 1
            if person == "man":
                shelter_civilians_saved += 1
        elif person == "man" and choice == "shoot":
            shelter_civilians_killed += 1

    def shelter_finish_deeremchin(choice):
        if choice in ("admit", "reject"):
            survivor = shelter_deeremchin_survivor()
            if survivor:
                shelter_record_deeremchin_person(survivor, choice)
            else:
                # On rejection the woman kills the man in the supplied movie.
                # That is not a shot fired by the player, so do not count it as one.
                shelter_record_deeremchin_person("man", "lost" if choice == "reject" else choice)
                shelter_record_deeremchin_person("woman", choice)

    def shelter_can_ask_questions():
        return shelter_visitor != "deeremchin" or shelter_deeremchin_survivor() is None

    def shelter_can_aim():
        return shelter_visitor != "deeremchin" or (
            shelter_deeremchin_survivor() is None and all(i in shelter_asked for i in range(3)))

    def shelter_action_choices(armed=False):
        if armed:
            if shelter_visitor == "deeremchin":
                return [("Эрэгтэйг буудах", "shoot_man", "shoot"),
                        ("Эмэгтэйг буудах", "shoot_woman", "shoot")]
            return [("Буудах", "shoot", "shoot"), ("Буугаа буулгах", "lower", "lower")]
        return [("Хөөх", "reject", "reject"), ("Оруулах", "admit", "admit")]

    def shelter_clip_is_terminal(clip):
        return clip in ("shoot", "admit", "reject", "man_admit", "man_reject", "woman_admit", "woman_reject")

    def shelter_clip_is_armed(clip):
        return clip in ("aim", "shoot", "lower", "shoot_man", "shoot_woman")

    def shelter_admitted_monster():
        if shelter_visitor == "deeremchin":
            return shelter_deeremchin_outcomes.get("woman") == "admit"
        return shelter_choice == "admit" and not SHELTER_CIVILIANS[shelter_visitor]

label shelter_deeremchin_handle_choice:
    if isinstance(shelter_choice, int) and shelter_can_ask_questions():
        if shelter_choice not in shelter_asked:
            $ shelter_asked.append(shelter_choice)
            call shelter_player_line("question%d" % (shelter_choice + 1), DEEREMCHIN_QUESTIONS[shelter_choice])
            call shelter_clip("answer%d" % (shelter_choice + 1))
        jump shelter_decision_phase
    elif shelter_choice == "aim" and shelter_can_aim():
        call shelter_clip("aim")
        call screen shelter_decision(armed=True)
        $ shelter_choice = _return
        jump shelter_deeremchin_handle_choice
    elif shelter_choice in ("shoot_man", "shoot_woman") and shelter_still == "aim" and shelter_can_aim():
        call shelter_clip(shelter_choice)
        $ shelter_record_deeremchin_person(shelter_choice.split("_")[1], "shoot")
        if shelter_campaign_status() == "casualties":
            # The fourth civilian death ends the game immediately.
            jump shelter_resolve_visitor
        jump shelter_decision_phase
    elif shelter_choice in ("admit", "reject"):
        if shelter_deeremchin_survivor() is None:
            call shelter_player_line(shelter_choice)
            call shelter_clip(shelter_choice)
        else:
            call shelter_clip(shelter_deeremchin_survivor() + "_" + shelter_choice)
        jump shelter_resolve_visitor
    jump shelter_decision_phase
