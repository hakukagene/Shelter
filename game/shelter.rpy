# Video-driven encounter using the supplied VP9/Opus WebM assets.
define SHELTER_FONT = "fonts/RobotoCondensed-Regular.ttf"
define SHELTER_BOLD = "fonts/RobotoCondensed-Bold.ttf"

default shelter_still = "intro"
default shelter_asked = []
default shelter_choice = None
# Keep Maral as the default for saves made before the two-visitor sequence.
default shelter_visitor = "Maral"
default shelter_chinba_outcome = None
# The supplied Bayra aim movie ends with one black frame after speech.
# Stop before that frame; keep the original source and audio untouched.
define SHELTER_CLIP_ENDS = {"Bayra/aim": 13.11}

# Append unique IDs and civilian classifications as new visitors are added.
define SHELTER_CIVILIAN_COUNT = 43
define SHELTER_MONSTER_COUNT = 30
define SHELTER_TOTAL_VISITORS = SHELTER_CIVILIAN_COUNT + SHELTER_MONSTER_COUNT
define SHELTER_CIVILIAN_TARGET = 40
define SHELTER_MAX_CIVILIAN_DEATHS = 2
define SHELTER_MAX_CIVILIAN_MISTAKES = 2
# Available roster, also the original sequence for saves predating random order.
define SHELTER_VISITOR_ORDER = ("Chinba", "Maral", "Swat", "Bayra", "anu", "deeremchin", "ganba")
default shelter_run_order = None
define SHELTER_CIVILIANS = {"Chinba": True, "Maral": False, "Swat": True, "Bayra": True, "anu": False, "ganba": True}
# Armor stops the bullet: Orgil leaves alive after being shot.
define SHELTER_NONLETHAL_SHOOT = ("Swat",)
default shelter_outcomes = {}
default shelter_admitted = 0
default shelter_civilians_saved = 0
default shelter_civilians_killed = 0
default shelter_visitors_seen = 0
# None gives older saves a stable time derived from their completed visits.
default shelter_story_minutes = None

define SHELTER_CLIPS = {
    "intro": ("Maral ehlel.webm", 12.808),
    "answer1": ("Maral hariult1.webm", 6.168),
    "answer2": ("Maral hariult2.webm", 5.928),
    "answer3": ("Maral hariult3.webm", 7.968),
    "aim": ("Maral buu gargah.webm", 11.568),
    "lower": ("Maral buudahaa bolih.webm", 3.048),
    "shoot": ("Maral buudah.webm", 8.048),
    "admit": ("Maral oruulah B huvilbar.webm", 6.048),
    "reject": ("Maral yavah.webm", 5.008),
}

define SHELTER_QUESTIONS = [
    "Чи ямар тайван байна аа. Айхгүй байгаа юм уу?",
    "Манай хорогдох байрыг хаанаас сонссон бэ?",
    "Надад худлаа яривал оруулахгүй гэдгийг мэдэж байгаа биз дээ?",
]

define SHELTER_LINES = {
    "intro": "Сайн байна уу. Би танай хорогдох байрны талаар сонсоод ирж байна аа. Энэ аюултай үед шалгаж оруулах байлгүй дээ. Би шалгуулахад бэлэн байна.",
    "answer1": "Айдас шийдвэр гаргахад туслахгүй л дээ. Та ч бас айж байгаа мөртлөө өөрийгөө барьж байна шүү дээ.",
    "answer2": "Радиогоор сонссон юм аа. Хэд хэдэн хорогдох байр хэлсний хамгийн ойр нь танайх байлаа.",
    "answer3": "Тэгвэл намайг сайн шалга. Гэхдээ намайг оруулж болохгүй гэдэг дүгнэлтэд хүрэхийн тулд бодитой шалтгаан хэрэгтэй биз дээ?",
    "aim": "Чи намайг буудаж болно. Гэхдээ эхлээд яагаад гэдгээ өөрөөсөө асуугаарай.",
}

# Cue windows measured from the bundled audio; times use the decoder clock.
# Keep these separate so dialogue edits do not require changing screen logic.
define SHELTER_SPEECH_WINDOWS = {
    "intro": (0.0, 12.49),
    "answer1": (0.568, 5.716),
    "answer2": (0.691, 5.597),
    "answer3": (0.705, 7.332),
    "aim": (3.199, 8.260),
}

define SHELTER_PLAYER_VOICES = {
    "question1": ("audio/Chingune/MaralAsuult1.wav", 0.620, 2.501),
    "question2": ("audio/Chingune/MaralAsuult2.wav", 0.865, 2.699),
    "question3": ("audio/Chingune/MaralAsuult3.wav", 0.780, 3.954),
    "reject": ("audio/Chingune/MaralHuuh.wav", 0.395, 1.549),
    "admit": ("audio/Chingune/MaralOruulah.wav", 0.347, 0.879),
}

define SHELTER_CLOCK_START = 23 * 60 + 10

define CHINBA_CLIPS = {
    "reject": ("Chinbaa yavah.webm", 13.648),
    "intro": ("Chinbaa ehlel.webm", 15.928),
    "answer1": ("Chinbaa hariult 1.webm", 8.128),
    "answer2": ("Chinbaa hariult 2.webm", 11.048),
    "answer3": ("Chinbaa hariult 3.webm", 3.568),
    "aim": ("Chinbaa buu gargah.webm", 3.048),
    "lower": ("Chinbaa buu buulgah.webm", 3.048),
    "shoot": ("Chinbaa buuduulah.webm", 3.048),
    "admit": ("Chinbaa oruulah.webm", 11.368),
}

define CHINBA_QUESTIONS = [
    "Чамд юу тохиолдоо вэ?",
    "Нүүр чинь яагаа вэ?",
    "Үүргэвч дотрохоо харуул.",
]

define CHINBA_LINES = {
    "intro": "Ах аа, хаалгаа нээгээрэй! Би хүргэлт хийж яваад зам дээр хүмүүс бие бие рүүгээ дайрахыг харсан. Мотоциклоо орхиод гүйж ирлээ. Утас маань ч ажиллахгүй байна.",
    "answer1": "Хорооллын уулзвар дээр. Нэг хүн машинд мөргүүлчихээд юу ч болоогүй юм шиг босоод явсан. Дараа нь хүмүүс орилолдоод эхэлсэн.",
    "answer2": "Нэг хүн намайг мотоциклоос татаж унагаасан. Унагаагаад араас хөөгөөд байсан. Би арай гэж мултарч ирлээ.",
    "answer3": "Тэгээ тэг. Дотор нь захиалгын хоол, утасны цэнэглэгч л байгаа.",
}

define CHINBA_SPEECH_WINDOWS = {
    "intro": (0.0, 15.928),
    "answer1": (0.554, 8.128),
    "answer2": (0.434, 11.048),
    "answer3": (0.411, 3.568),
}

define CHINBA_PLAYER_VOICES = {
    "question1": ("audio/Chingune/ChinbaAsuult1.wav", 0.505, 1.438),
    "question2": ("audio/Chingune/ChinbaAsuult2.wav", 0.36, 0.503),
    "question3": ("audio/Chingune/ChinbaAsuult3.wav", 0.567, 1.394),
    "reject": ("audio/Chingune/ChinbaHuuh.wav", 0.765, 0.993),
    "admit": ("audio/Chingune/ChinbaOruulah.wav", 0.383, 0.763),
}


define SWAT_CLIPS = {'intro': ('swat ehlel.webm', 17.928), 'answer1': ('swat hariult 1.webm', 14.728), 'answer2': ('swat hariult 2.webm', 11.464), 'answer3': ('swat hariult 3.webm', 14.728), 'aim': ('swat buu gargah.webm', 7.304), 'lower': ('swat buugaa buulgah.webm', 3.058), 'shoot': ('swat buuduulav.webm', 14.493), 'reject': ('swat hoogdov.webm', 12.936), 'admit': ('swat oroh.webm', 8.05)}
# Оргил — Энгийн хүн 2, from the updated author script.
define SWAT_QUESTIONS = [
    "Та үнэмлэхээ үзүүлээч",
    "Танай салааныхан яг хаана, яаж амь үрэгдсэн юм бэ?",
    "Хувцас чинь цус болсон байна. Чи шархадсан юм уу?",
]
define SWAT_LINES = {
    "intro": "Сайн байна уу? Хорогдох байр мөн үү? Бидэнд ойролцоох хорогдох байр луу ухрах тушаал ирсэн. Радио холбоо тасраад, салааныхантайгаа буцаж холбогдож чадсангүй. Манай салааныхан бүгд үхсэн. Би л ганцаараа амьд үлдлээ. Энэ гадуур чинь хаа сайгүй мангасууд байна. Хурдан хаалгаа нээгээрэй.",
    "answer1": "Юун үнэмлэх вэ? Тулааны үеэр цүнх, үнэмлэхээ алдсан. Би тусгай салааны ахлах түрүүч Оргил байна. Хувцас, тэмдгийг минь хар л даа. Одоо бичиг баримт нэхэж зогсох цаг мөн үү? Алив хурдлаач!",
    "answer2": "Хорооллын уулзварын цаана зам хаагдаад бид хүмүүсийг машинаас нь гаргаж байсан. Гэнэт л энгийн иргэд гэж бодож байсан хүмүүс маань бидэн рүү дайрсан. Сум ч тэднийг зогсоож чадсангүй. Би л зугтаж амжлаа.",
    "answer3": "Миний цус биш ээ. Би шархадсан нөхрөө үүрч явсан юм. Даан ч тэр амь үрэгдчихсэн. Чи хаалгаа хурдан нээхгүй бол би ч бас амь үрэгдэх гээд байна. Алив хурдлаач!",
    "aim": "Оролдоод үз л дээ! Чи намайг ингэж айлгаж чадна гэж бодоо юу?",
    "shoot": "Өө алдгийн байна. За яахав чи харамсана аа.",
    "reject": "Юу яриад байна аа. Чи намайг эндээс хөөж чадна гэж бодоо юу?",
    "admit": "Уучлаарай, жаахан түрэмгий аашилчихлаа. Саяхан нөхдөө алдаад уураа барьж дийлсэнгүй. Би энд хэрэгтэй хүн байхыг хичээнэ. Намайг оронгуут хурдан хаалгаа хаагаарай.",
}

define SWAT_SPEECH_WINDOWS = {'intro': (0, 17.037), 'answer1': (1.015, 14.279), 'answer2': (0.817, 10.859), 'answer3': (1.536, 14.279), 'aim': (0, 6.65), 'shoot': (0, 14.48), 'reject': (0.555, 12.92), 'admit': (2.424, 7.83)}


# Баяр — Энгийн хүн 9; fourth playable encounter.
define BAYRA_CLIPS = {'intro': ('intro.webm', 15.182), 'answer1': ('answer1.webm', 36.436), 'answer2': ('answer2.webm', 14.181), 'answer3': ('answer3.webm', 19.219), 'aim': ('aim.webm', 13.18), 'lower': ('lower.webm', 4.271), 'shoot': ('shoot.webm', 3.737), 'admit': ('admit.webm', 10.377), 'reject': ('reject.webm', 10.143)}
define BAYRA_QUESTIONS = [
    "Та хэн бэ?",
    "Та энэ хорогдох байрыг хаанаас мэдэж ирэв?",
    "Наад цүнхэн доторхоо харуулаач",
]
define BAYRA_LINES = {
    "intro": "За ашгүй дээ. Хаалгаа нээгээрэй. Энд удаан байж чадахгүй нь... Хаалгаа яагаад нээхгүй байна аа. Намайг оруулахгүй юм уу?",
    "answer1": "Чи намайг нэг л дутуу үнэлээд байна даа. Монтек корпорацийг мэднэ биз дээ. Би Монтек-ийн ерөнхий захирал Баяр гэж хүн байна аа. Найзууд маань намайг баян Баяраа гэж дууддаг л даа. Чи тэгж дуудаж болно шүү. Би сая жолоочтойгоо өөрийн хорогдох байр луугаа давхиж яваад осолд орчихлоо. Чамд хэд хэрэгтэйгээ л хэлчих. 20 саяыг өгвөл болох уу? За за 30 саяыг өгье. Хөөе 30 сая шүү дээ. Мэдрэл муутай хүнтэй таарчихгүй байгаа даа.",
    "answer2": "Мэдэлгүй яахав. Мөнгө байхад ямар ч мэдээллийг авч болдог юм. Уг нь надад Шарга морьтод хувийн хорогдох байр байгаа л даа. Даанч одоо тийшээ явахаасаа өнгөрөөд байна. Нисдэг тэрэг маань ирсэнгүй.",
    "answer3": "За тэгж ярихгүй шүү. Энд үнэтэй цайтай зүйлс байгаа. Ёстой Туулын мөсийг долоох шахам байж цуглуулсан зүйлс. Чам шиг гуйлгачин... За за хаалгаа хурдлаач. Надад энд мөнгө байна, чи хэдийг хүсэж байна? Би хүссэн мөнгийг чинь өгье.",
    "aim": "Хүүе хүүе. Би чамайг баян болгож чадна шүү дээ. Алив ер нь даргатай чинь уулзъя. Даргыгаа дуудаадах аа.",
    "reject": "Өө заяа нь хаясан юм бэ? Дүү ч том алдаа гаргалаа даа. Одоо яая гэхэв.",
    "admit": "Тийм байлгүй дээ. Мөнгөнд дургүй хүн гэж байдаггүй юм.",
}
define BAYRA_SPEECH_WINDOWS = {'intro': (3.219, 12.612), 'answer1': (0.332, 35.687), 'answer2': (0.236, 13.726), 'answer3': (0.359, 18.307), 'aim': (2.224, 10.117), 'reject': (0.878, 6.335), 'admit': (0.468, 4.005)}


# Player questions supplied for Bayra; windows measured from each recording.
define BAYRA_PLAYER_VOICES = {
    "question1": ("audio/Bayra/asuult1.wav", 0.151, 0.628),
    "question2": ("audio/Bayra/asuult2.wav", 0.191, 2.004),
    "question3": ("audio/Bayra/asuult3.wav", 0.171, 1.571),
}

# Ану — Чөтгөр 2; fifth encounter. Folder spelling matches the uploaded assets.
define ANU_CLIPS = {
    "intro": ("intro.webm", 17.000),
    "answer1": ("answer1.webm", 16.000),
    "answer2": ("answer2.webm", 19.800),
    "answer3": ("answer3.webm", 11.560),
    "aim": ("aim.webm", 10.560),
    "lower": ("lower.webm", 3.040),
    "shoot": ("shoot.webm", 6.040),
    "admit": ("admit.webm", 6.040),
    "reject": ("reject.webm", 19.520),
}
define ANU_QUESTIONS = [
    "Ээжийг чинь хамгийн сүүлд хаана харсан бэ?",
    "Замд чинь том хүн тааралдаагүй гэж үү?",
    "Цүнхээ нээгээд харуул даа.",
]
define ANU_LINES = {
    "intro": "Ах аа... хаалгаа нээгээч. Би ээжийгээ олохгүй байна. Ээж маань танайд байж магадгүй. Би энд ганцаараа баймааргүй байна.",
    "answer1": "Ээж намайг энд ирнэ гэдгийг мэдэж байгаа. Тэр хаалганы цаанаас намайг дуудаад байна. Та сонсохгүй байна уу? Тэр яг одоо миний нэрийг дуудаж байна.",
    "answer2": "Тааралдсан. Тэд намайг ганцааранг минь орхисон. Та ч бас намайг орхих уу? Наад дотор чинь хүүхэд байгаа юу?",
    "answer3": "Тийм. Энэ хаалгыг би зүүдэндээ харсан. Гэхдээ яг юуны хаалга гэдгийг би мэдэхгүй байна. Харин та мэдэх үү?",
    "aim": "Ах аа, би ээж дээрээ очмоор байна. Намайг оруулчих л даа.",
    "reject": "Та намайг буцаагаад дуудаж магадгүй шүү.",
}
define ANU_SPEECH_WINDOWS = {
    "intro": (3.798, 16.319), "answer1": (1.070, 14.665),
    "answer2": (1.547, 18.508), "answer3": (0.750, 10.865),
    "aim": (4.478, 9.787), "reject": (3.960, 6.053),
}

init python:
    renpy.music.register_channel("shelter_knock", mixer="sfx", loop=False, stop_on_mute=False)
    SHELTER_VISITORS = {
        "ganba": {"clips": GANBA_CLIPS, "questions": GANBA_QUESTIONS,
                "lines": GANBA_LINES, "windows": GANBA_SPEECH_WINDOWS, "voices": {}},
        "deeremchin": {"clips": DEEREMCHIN_CLIPS, "questions": DEEREMCHIN_QUESTIONS,
                "lines": DEEREMCHIN_LINES, "windows": DEEREMCHIN_SPEECH_WINDOWS,
                "voices": DEEREMCHIN_PLAYER_VOICES},
        "anu": {"clips": ANU_CLIPS, "questions": ANU_QUESTIONS,
                "lines": ANU_LINES, "windows": ANU_SPEECH_WINDOWS, "voices": {}},
        "Bayra": {"clips": BAYRA_CLIPS, "questions": BAYRA_QUESTIONS,
                "lines": BAYRA_LINES, "windows": BAYRA_SPEECH_WINDOWS, "voices": BAYRA_PLAYER_VOICES},
        "Swat": {"clips": SWAT_CLIPS, "questions": SWAT_QUESTIONS,
                "lines": SWAT_LINES, "windows": SWAT_SPEECH_WINDOWS, "voices": {}},
        "Maral": {"clips": SHELTER_CLIPS, "questions": SHELTER_QUESTIONS,
                "lines": SHELTER_LINES, "windows": SHELTER_SPEECH_WINDOWS,
                "voices": SHELTER_PLAYER_VOICES},
        "Chinba": {"clips": CHINBA_CLIPS, "questions": CHINBA_QUESTIONS,
                "lines": CHINBA_LINES, "windows": CHINBA_SPEECH_WINDOWS,
                "voices": CHINBA_PLAYER_VOICES},
    }

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

    def shelter_killed_total():
        # The ledger counts every fatal shot, including monsters. Orgil's armor
        # stops the bullet; the separate civilian-loss rule remains unchanged.
        return sum(choice == "shoot" and visitor not in SHELTER_NONLETHAL_SHOOT
                for visitor, choice in shelter_outcomes.items()) + sum(
                    choice == "shoot" for choice in shelter_deeremchin_outcomes.values())

    def shelter_record_outcome(visitor, choice):
        # Copy-on-write supports saves/rollback; one outcome per visitor.
        global shelter_outcomes, shelter_admitted, shelter_civilians_saved
        global shelter_civilians_killed, shelter_visitors_seen, shelter_story_minutes
        if visitor in shelter_outcomes:
            return
        allowed = ("admit", "reject", "shoot_man", "shoot_woman") if visitor == "deeremchin" else ("admit", "reject", "shoot")
        if choice not in allowed:
            raise ValueError("Not a final decision: " + str(choice))
        # Advance once per resolved visitor, never during screen prediction or
        # redraw. Ren'Py saves/rolls back both this value and its random state.
        elapsed = 7 if shelter_visitors_seen == 0 else renpy.random.randint(4, 9)
        shelter_story_minutes = shelter_clock_minutes() + elapsed
        shelter_outcomes = dict(shelter_outcomes, **{visitor: choice})
        if visitor == "deeremchin":
            shelter_visitors_seen += 2
            shelter_finish_deeremchin(choice)
            return
        civilian = SHELTER_CIVILIANS[visitor]
        shelter_visitors_seen += 1
        if choice == "admit":
            shelter_admitted += 1
            if civilian:
                shelter_civilians_saved += 1
        elif choice == "shoot" and civilian and visitor not in SHELTER_NONLETHAL_SHOOT:
            shelter_civilians_killed += 1

    def shelter_civilian_mistakes():
        # Fatal shots are already counted, including the man in the pair.
        # Rejecting a civilian (or forcing armored Orgil to leave) also loses one.
        rejected = sum(SHELTER_CIVILIANS.get(visitor, False) and
            (choice == "reject" or (choice == "shoot" and visitor in SHELTER_NONLETHAL_SHOOT))
            for visitor, choice in shelter_outcomes.items())
        rejected += shelter_deeremchin_outcomes.get("man") in ("reject", "lost")
        return shelter_civilians_killed + rejected

    def shelter_campaign_status():
        if shelter_civilian_mistakes() > SHELTER_MAX_CIVILIAN_MISTAKES:
            return "casualties"
        if shelter_civilians_saved >= SHELTER_CIVILIAN_TARGET:
            return "win"
        if shelter_visitors_seen >= SHELTER_TOTAL_VISITORS:
            return "shortfall"
        return "continue"

    def shelter_data(key):
        return SHELTER_VISITORS[shelter_visitor][key]

    renpy.music.register_channel("shelter_player", mixer="voice", loop=False, stop_on_mute=False)
    # Muting dialogue must silence the soundtrack, not stop/skip the movie.
    # Movie channels must not pre-buffer the next file like audio-only channels.
    renpy.music.register_channel(
        "shelter_video", mixer="voice", loop=False, movie=True,
        stop_on_mute=False, buffer_queue=False)
    def shelter_wait_image(clip, visitor=None):
        visitor = visitor or shelter_visitor
        if visitor == "ganba":
            if clip in ("intro", "answer1", "answer2", "answer3", "lower"):
                return shelter_movie_frame(visitor, "answer1", "start")
            return shelter_movie_frame(visitor, clip, "end")
        if visitor == "deeremchin":
            # Match the actual video framing; never reintroduce a shot person.
            if clip in ("aim", "shoot_man", "shoot_woman") or shelter_clip_is_terminal(clip):
                return shelter_movie_frame(visitor, clip, "end")
            return shelter_movie_frame(visitor, "answer3", "start")
        # Maral's answer1 still is a close-up. Keep the doorway framing fixed
        # between questions, including old saves that stopped on that answer.
        if visitor == "Maral" and clip in ("intro", "answer1", "answer2", "answer3", "lower"):
            return "images/Maral/frames/intro.jpg"
        if visitor in ("Bayra", "anu"):
            if clip in ("intro", "answer1", "answer2", "answer3", "lower"):
                clip = "idle"
            # Old Bayra saves can still contain split-clip still names.
            clip = {"arrival": "arrival_start", "enter": "admit", "leave": "reject"}.get(clip, clip)
            return "images/" + visitor + "/frames/" + clip + ".jpg"
        if visitor == "Swat":
            if clip in ("intro", "answer1", "answer2", "answer3", "lower"):
                clip = "idle"
            return "images/Swat/frames/" + clip + ".jpg"
        # Reference-matched frames extracted from the source videos (not the supplied PNGs).
        # idle: Chinbaa hariult 3, first frame; aim: Chinbaa buuduulah, first frame.
        # Keep the same neutral pose for every unarmed question/waiting state.
        if visitor == "Chinba" and clip in ("intro", "answer1", "answer2", "answer3", "lower"):
            return "images/Chinba/frames/idle.jpg"
        allowed = ("intro", "answer1", "answer2", "answer3", "aim", "lower")
        if visitor == "Chinba":
            allowed += ("arrival", "shoot", "admit", "reject")
        if clip not in allowed:
            clip = "intro"
        return "images/" + visitor + "/frames/" + clip + ".jpg"

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
        return "images/transitions/" + visitor + "/" + clip + "-" + edge + ".jpg"

    def shelter_movie_start_image(visitor, clip):
        return shelter_movie_frame(visitor, clip, "start")

    def shelter_movie_path(visitor, clip):
        path = "Video/" + visitor + "/" + SHELTER_VISITORS[visitor]["clips"][clip][0]
        end = SHELTER_CLIP_ENDS.get(visitor + "/" + clip)
        return ("<to %s>" % end if end else "") + path

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

transform shelter_fade:
    alpha 0.0
    linear 0.2 alpha 1.0

transform shelter_tail_to_idle:
    alpha 1.0
    pause 0.07
    linear 0.18 alpha 0.0

style shelter_text is default:
    font SHELTER_FONT
    size 30
    color "#f2e9d9"
    outlines [(1, "#0009", 0, 1)]

style shelter_button is button:
    background Frame("gui/shelter/idle.png", 16, 16)
    hover_background Frame("gui/shelter/hover.png", 16, 16)
    insensitive_background Transform(Frame("gui/shelter/disabled.png", 16, 16), matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.15))
    padding (24, 16)

style shelter_button_text is shelter_text:
    hover_color "#ffd38c"
    insensitive_color "#777777"
    xalign 0.5
    yalign 0.5
    text_align 0.5

screen shelter_backdrop():
    add shelter_video_end(shelter_still) xysize (1920, 1080)



screen shelter_playback(clip):
    modal True
    default elapsed = 0.0
    # Movie can briefly render transparent while its decoder changes state.
    # Keep a full-size poster underneath it, including during Dissolve.
    add shelter_movie_start_image(shelter_visitor, clip) xysize (1920, 1080)
    add shelter_movies[(shelter_visitor, clip)] xysize (1920, 1080)
    use shelter_actions(enabled=False, armed=shelter_clip_is_armed(clip))
    # Block click-to-dismiss and keyboard skipping while the clip plays.
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    $ speech_position = renpy.music.get_pos(channel="shelter_video")
    $ speech_window = shelter_data("windows").get(clip)
    if speech_window and speech_position is not None and speech_window[0] <= speech_position < speech_window[1]:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos (580 if shelter_visitor in ("Bayra", "ganba") else 630 if shelter_visitor == "Swat" else 710)
            xsize 1344
            padding (35, 22)
            text shelter_data("lines")[clip] style "shelter_text" size (24 if shelter_visitor == "Bayra" else 26 if shelter_visitor in ("Swat", "ganba") else 30) xalign 0.5 text_align 0.5
    # A short startup grace avoids interpreting a not-yet-started decoder as EOF.
    # Actual playback completion, rather than a fixed timer, drives progression.
    timer 0.03 repeat True action If(renpy.get_screen("shelter_protocol"), NullAction(), If(
        elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_video"),
        Return(True), SetScreenVariable("elapsed", elapsed + 0.03)))
    use shelter_protocol_button

# Both native and HTML playback land on the same decoded end frame first.
# Then only conversational/armed clips blend to their stable waiting pose.
screen shelter_clip_handoff(clip):
    modal True
    $ terminal = shelter_clip_is_terminal(clip)
    use shelter_backdrop
    if not terminal:
        add shelter_movie_frame(shelter_visitor, clip, "end") xysize (1920, 1080) at shelter_tail_to_idle
    use shelter_actions(enabled=False, armed=shelter_clip_is_armed(clip))
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    key "game_menu" action NullAction()
    if renpy.emscripten:
        # Paint this canvas before hiding the HTML video overlay.
        timer 0.03 action Function(shelter_web_close)
    timer (0.12 if terminal else 0.26) action Return(True)

# Armed mode offers exactly two actions; aiming lives in the question row.
screen shelter_actions(enabled=True, armed=False):
    hbox:
        xalign 0.5
        ypos 880
        spacing 24
        $ choices = shelter_action_choices(armed)
        for caption, result, icon in choices:
            button:
                xysize (180, 180)
                padding (0, 0)
                background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180))
                hover_background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180), matrixcolor=BrightnessMatrix(0.14))
                insensitive_background Transform("gui/shelter/actions/" + icon + ".png", xysize=(180, 180), matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.22))
                focus_mask True
                sensitive enabled
                action [Function(shelter_hold_current_frame), Return(result)]
                text caption:
                    font SHELTER_BOLD
                    size 15
                    color "#f4dfaf"
                    hover_color "#ffffff"
                    insensitive_color "#777777"
                    xalign 0.5
                    ypos 107
                    xsize 118
                    text_align 0.5
                    outlines [(1, "#000b", 0, 1)]

# Player speaks over the waiting portrait; Maral responds only after EOF.
screen shelter_player_speech(voice_key, caption=None):
    modal True
    default elapsed = 0.0
    use shelter_backdrop
    use shelter_actions(enabled=False)
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    on "hide" action Stop("shelter_player")
    $ position = renpy.music.get_pos(channel="shelter_player")
    $ cue = shelter_player_voice(voice_key)
    if caption and position is not None and cue[1] <= position < cue[2]:
        frame:
            background Solid("#080707dd")
            xalign 0.5
            ypos 710
            xsize 1344
            padding (35, 22)
            text caption style "shelter_text" text_align 0.5 xalign 0.5
    timer 0.03 repeat True action If(renpy.get_screen("shelter_protocol"), NullAction(), If(
        elapsed >= 0.5 and not renpy.music.get_playing(channel="shelter_player"),
        Return(True), SetScreenVariable("elapsed", elapsed + 0.03)))
    use shelter_protocol_button

screen shelter_question_choices():
    hbox:
        xalign 0.5
        ypos 655
        spacing 16
        for index, question in enumerate(shelter_data("questions")):
            textbutton question:
                style "shelter_button"
                text_style "shelter_button_text"
                text_size (30 if renpy.variant("web") else 26)
                text_text_align 0.5
                xysize (330, 170)
                sensitive index not in shelter_asked or shelter_has_inspection(shelter_visitor, index)
                action [Function(shelter_hold_current_frame), Return(index)]
        textbutton "Буу онилох":
            style "shelter_button"
            text_style "shelter_button_text"
            text_size (30 if renpy.variant("web") else 26)
            xysize (330, 170)
            sensitive shelter_can_aim()
            action [Function(shelter_hold_current_frame), Return("aim")]

screen shelter_questions():
    modal True
    use shelter_backdrop
    use shelter_actions
    use shelter_question_choices
    use shelter_protocol_button


screen shelter_decision(armed=False):
    modal True
    use shelter_backdrop
    use shelter_actions(armed=armed)
    if not armed and shelter_can_ask_questions():
        use shelter_question_choices
    use shelter_protocol_button


screen shelter_anu_admission():
    # Compatibility for saves made while the old admission placeholder was open.
    modal True
    add shelter_movie_frame("anu", "admit", "end") xysize (1920, 1080)
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    timer 1.2 action Return(True)

# Concept 01: live text and actions over the text-free lockdown artwork.
screen shelter_result(title, description):
    modal True
    on "show" action Play("music", "<volume 0.50>audio/Audio/menu2.mp3", loop=True, fadeout=0.6, fadein=0.8)
    add "gui/shelter/ending/lockdown.jpg" xysize (1920, 1080)
    text title:
        style "shelter_text"
        font SHELTER_BOLD
        size 54
        xalign 0.5
        ypos 393
        xsize 1160
        text_align 0.5
    # Hit areas match the two physical plates in the background.
    for caption, result, left in [("Дахин тоглох", "replay", 580), ("Үндсэн цэс", "menu", 1025)]:
        button:
            xpos left
            ypos 645
            xysize (384, 145)
            padding (0, 0)
            background None
            hover_background Solid("#ffd6a01c")
            action Return(result)
            text caption:
                font SHELTER_FONT
                size 34
                color "#f2e9d9"
                hover_color "#ffffff"
                outlines [(1, "#0009", 0, 1)]
                xpos 120
                yalign 0.5

# Unskippable story-time card, followed by the supplied metal-door recording.
screen shelter_next_visitor_card():
    modal True
    use shelter_transition_status
    key "dismiss" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "rollback" action NullAction()
    on "hide" action Stop("shelter_knock")
    timer 2.0 action Play("shelter_knock", "audio/Audio/door .wav", loop=False)
    # Allow the full supplied 2.20-second knock before the visitor fades in.
    timer 4.5 action Return(True)

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
        $ shelter_web_begin("Video/" + shelter_visitor + "/" + shelter_data("clips")[clip][0], shelter_web_clip_cues(clip), poster=shelter_movie_start_image(shelter_visitor, clip), armed=shelter_clip_is_armed(clip), end_time=SHELTER_CLIP_ENDS.get(shelter_visitor + "/" + clip), end_poster=shelter_movie_frame(shelter_visitor, clip, "end"))
        call screen shelter_web_wait
    else:
        call screen shelter_playback(clip)
    $ shelter_still = clip
    scene expression Transform(shelter_movie_frame(shelter_visitor, clip, "end"), xysize=(1920, 1080)) as shelter_hold
    call screen shelter_clip_handoff(clip)
    scene expression shelter_video_end(clip) as shelter_hold
    return

label shelter_encounter:
    play music "<volume 0.18>audio/Audio/shuum.mp3" fadeout 0.6 fadein 1.0
    $ quick_menu = False
    $ shelter_run_order = shelter_make_visitor_order()
    $ shelter_visitor = shelter_run_order[0]
    $ shelter_chinba_outcome = None
    $ shelter_outcomes = {}
    $ shelter_deeremchin_outcomes = {}
    $ shelter_admitted = 0
    $ shelter_civilians_saved = 0
    $ shelter_civilians_killed = 0
    $ shelter_visitors_seen = 0
    $ shelter_story_minutes = SHELTER_CLOCK_START
    $ shelter_inspection_progress = {}
    $ shelter_inspection_requests = []
    $ shelter_checkpoint_created = False
    $ shelter_checkpoint_written = False
    jump shelter_visit_start

label shelter_visit_start:
    $ shelter_asked = []
    $ shelter_choice = None
    $ shelter_still = "arrival" if shelter_visitor in ("Chinba", "Swat") else "intro"
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
    if shelter_visitor == "deeremchin":
        jump shelter_deeremchin_handle_choice
    if isinstance(shelter_choice, int):
        if shelter_has_inspection(shelter_visitor, shelter_choice):
            call shelter_inspect_belongings from _call_shelter_inspect_belongings
            jump shelter_decision_phase
        $ shelter_asked.append(shelter_choice)
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
    if shelter_visitor == "Chinba":
        $ shelter_chinba_outcome = shelter_choice
    $ shelter_status = shelter_campaign_status()
    if shelter_status == "continue" and not shelter_admitted_monster():
        call shelter_save_midpoint from _call_shelter_save_midpoint
    if shelter_status == "casualties":
        $ shelter_mistakes = shelter_civilian_mistakes()
        call screen shelter_result("ТА ХОЖИГДЛОО", "Та [shelter_mistakes] энгийн хүнийг хөнөөсөн эсвэл хөөж явуулсан. Зөвшөөрөгдөх алдааны дээд хэмжээ 2.")
    elif shelter_admitted_monster():
        $ shelter_monster_ending = "Эмэгтэй чөтгөр болон хувирч, тан руу дайрлаа." if shelter_visitor == "deeremchin" else "Ану чөтгөр болон хувирч, тан руу дайрлаа." if shelter_visitor == "anu" else "Маралын дүр аймшигтайгаар хувирч, тэр чөтгөрийн инээдээр инээн тан руу дайрлаа."
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
        call screen shelter_result("ТУРШИЛТЫН ХЭСЭГ ДУУСЛАА", "Оруулсан: [shelter_admitted] • Аврагдсан: [shelter_civilians_saved]/40 • Алдаа: [shelter_mistakes]/2. Үлдсэн дүрүүд хараахан нэмэгдээгүй.")
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
