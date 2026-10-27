# Naraa - civilian encounter. Media supplied in game/Video/naraa/.
# Durations were measured from the supplied VP9/Opus WebMs.
define NARAA_CLIPS = {
    "intro": ("Naraa Ehlel.webm", 12.368),
    "answer1": ("Naraa Hariult 1.webm", 38.968),
    "answer2": ("Naraa Hariult 2.webm", 26.688),
    "answer3": ("Naraa Hariult 3.webm", 15.368),
    "aim": ("Naraa garaa orgoh.webm", 12.128),
    "lower": ("Naraa garaa buulgah.webm", 3.048),
    "shoot": ("Naraag buudah.webm", 4.048),
    "admit": ("Naraa Oruulah.webm", 7.043),
    "reject": ("Naraa hoogdoh.webm", 8.968),
}

# Player question captions.
define NARAA_QUESTIONS = [
    "Чамд юу тохиолдоо вэ?",
    "Чамайг яагаад би оруулах ёстой вэ?",
    "Цүнхэнд чинь юу байгаа вэ?",
]
# Subtitles restored from the supplied Shelter character script.
# Broad clip windows keep script captions visible; these are not word-level timings.
define NARAA_LINES = {
    "intro": "Сайн уу, сайхан залуу минь. Энэ хорогдох байр мөн үү? Намайг оруулаач. Чи нар харамсахгүй шүү.",
    "answer1": "За байз… буудлын арын гудамжинд нэг үйлчлүүлэгч маань гэнэт хүн рүү дайрсан. Эхэндээ маргалдаж байна гэж бодоод холдсон л доо, гэтэл тэр хүний нүүр нэг л сонин болж эхэлсэн. Манай найзууд руу дайраад бөөн цус нөж болоод эхэлсэн, би бүр ШОК. Хаа сайгүй сандарсан гүйлдсэн хүмүүс. Би зугтаж такси хайж байгаад машинд мөргүүлчихсэн. Хэсэг ухаангүй байсан бололтой. Сэрээд харсан энэ хавьд гэрэл гарч байгаа харагдаад хүрээд ирлээ.",
    "answer2": "Наадах чинь хорогдох байр юм биш үү. Орж хорогдоё л доо. Би тийм ч энгийн хүн биш л дээ. За л даа, ийм сайхан хүүхнийг үх гээд орхино гэж үү? Намайг оруулбал би хариуг чинь барина шүү. Яаж гэдгийг нь чи мэдэж байгаа биз дээ айн? кк",
    "answer3": "Миний хувийн эд зүйлс байгаа. Уучлаарай, хэт хувийн эд зүйлс байгаа тул би харуулж чадахгүй нь.",
    "aim": "Оёоёоёо, яасан айхтар ууртай юм. Чи арай буудчихгүй биз дээ айн.",
    "reject": "Ёооё, чи лав гомо байх аа.",
    "admit": "Ёооё, тийм байлгүй дээ. Надад эрчүүд ер нь татгалзаад байдаггүй л дээ. Би чамайг Gay юм болов уу л гэж бодож эхэлж байлаа шүү."
}
define NARAA_SPEECH_WINDOWS = {
    "intro": (0.0, NARAA_CLIPS["intro"][1]),
    "answer1": (0.0, NARAA_CLIPS["answer1"][1]),
    "answer2": (0.0, NARAA_CLIPS["answer2"][1]),
    "answer3": (0.0, NARAA_CLIPS["answer3"][1]),
    "aim": (0.0, NARAA_CLIPS["aim"][1]),
    "reject": (0.0, NARAA_CLIPS["reject"][1]),
    "admit": (0.0, NARAA_CLIPS["admit"][1]),
}

# Naraa's question recordings are registered in player_voices.rpy.

