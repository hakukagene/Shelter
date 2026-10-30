# Undral, 25: monster. Source text: the supplied Shelter character script.
# The media workflow refreshes durations from the actual WebMs.
define UNDRAL_CLIPS = {
    "intro": ("Undral ehlel.webm", 20.841),
    "answer1": ("Undral hariult1.webm", 36.133),
    "answer2": ("Undral hariult2.webm", 21.258),
    "answer3": ("Undral hariult3.webm", 13.674),
    "aim": ("Undral garaa orgoh.webm", 3.049),
    "lower": ("Undral garaa buulgah.webm", 3.049),
    "shoot": ("Undral buuduulah.webm", 5.716),
    "reject": ("Undral hoogdoh.webm", 12.383),
    "admit": ("Undral oruulah.webm", 7.049),
}

define UNDRAL_QUESTIONS = [
    "Чамд юу тохиолдоо вэ?",
    "Чи хүн мөн гэдгээ баталж чадах уу?",
    "Хүүхэд чинь зүгээр үү?",
]
define UNDRAL_LINES = {
    "intro": "Ахаа биднийг оруулаач. Гэр лүүгээ очих боломж байдаггүй ээ. Хаа сайгүй аймаар хүмүүс байна. Бид хоёр ахиж энд нуугдаж тэсэхгүй нь ээ. Ахаа гуйж байна. Бид танд төвөг удахгүй байхыг хичээнэ ээ.",
    "answer1": "Би хүүхдээ хадмынхаас аваад гэр лүүгээ автобусаар явж байсан юм. Гэнэт л автобус нэг юм мөргөөд хүмүүс орилолдоод буусан. Автобуснаас буухад аймар хүмүүс бидэн рүү дайрсан. Нэг залуу надад туслаагүй бол бид хоёр ч балрах байлаа. Даанч тэр залуу амьд гараагүй байх аа. Тэр биднийг зугтаалгах гэж амиа золиосолсон.",
    "answer2": "Би танд яаж батлах вэ? Хэрэв та биднийг оруулахгүй бол бид энд амьд гарахгүй шүү дээ. Танаас гуйж байна биднийг оруулаач. Энэ хүүхдээрээ би танд андгайлъя. Би тэдний нэг биш.",
    "answer3": "Зүгээр ээ, одоо унтаж байна. Харин би дааруулчихлаа л гэж санаа зовоод байна. Ахаа хурдлаарай. Хүүхэд минь өвдчихвөл ийм нөхцөлд би баларна.",
    "reject": "Би явж болно оо, та харин миний хүүхдийг аваад үлдчихээч. Гуйж байна.",
}
# Script captions cover each spoken clip; sentence-level timing is not verified.
define UNDRAL_SPEECH_WINDOWS = {
    "intro": (0.0, UNDRAL_CLIPS["intro"][1]),
    "answer1": (0.0, UNDRAL_CLIPS["answer1"][1]),
    "answer2": (0.0, UNDRAL_CLIPS["answer2"][1]),
    "answer3": (0.0, UNDRAL_CLIPS["answer3"][1]),
    "reject": (0.0, UNDRAL_CLIPS["reject"][1]),
}

define UNDRAL_POSTERS = {
    "idle": "images/undral/Undral idle.jpg",
    "aim": "images/undral/undral garaa orgoson.png",
}
define UNDRAL_POSTER_STATES = {
    "intro": ("idle", "idle"),
    "answer1": ("idle", "idle"),
    "answer2": ("idle", "idle"),
    "answer3": ("idle", "idle"),
    "aim": ("idle", "aim"),
    "lower": ("aim", "idle"),
    "shoot": ("aim", "aim"),
    "reject": ("idle", "idle"),
    "admit": ("idle", "idle"),
}

define UNDRAL_SUPPLIED_PLAYER_VOICES = {
    'question1': ('audio/undral/undral asuult1.wav', 0, 1.199),
    'question2': ('audio/undral/undral asuult2.wav', 0, 1.848),
    'question3': ('audio/undral/undral asuult3.wav', 0, 0.887),
}

init 1 python:
    shelter_register_visitor("undral", roster_position=10, civilian=False,
        clips=UNDRAL_CLIPS, questions=UNDRAL_QUESTIONS, lines=UNDRAL_LINES,
        windows=UNDRAL_SPEECH_WINDOWS, supplied_voices=UNDRAL_SUPPLIED_PLAYER_VOICES,
        stills="posters", posters=UNDRAL_POSTERS, poster_states=UNDRAL_POSTER_STATES,
        monster_ending="Хүүхэд чөтгөр болон хувирч, тан руу дайрлаа.")
