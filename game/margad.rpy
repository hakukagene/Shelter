# Margad, 18: monster. The first answer is a three-part conversation.
define MARGAD_CLIPS = {
    "intro": ("Chotgor ehlel.webm", 21.728),
    "answer1": ("Chotgor hariult 1.webm", 11.525),
    "answer1_part2": ("Chotgor hariult 1.webm", 3.274),
    "answer1_part3": ("Chotgor hariult 1.webm", 4.300),
    "answer2": ("Chotgor hariult 2.webm", 16.648),
    "answer3": ("Chotgor hariult 3.webm", 9.528),
    "aim": ("Chotgor Buu tulgah.webm", 4.288),
    "lower": ("Chotgor buugaa bolih.webm", 3.048),
    "shoot": ("Chotgor buuduulah.webm", 7.048),
    # No dedicated rejection movie was supplied. Reuse only the silent tail of
    # the intro so the choice remains playable without mismatched dialogue.
    "reject": ("Chotgor ehlel.webm", 0.955),
    "admit": ("Chotgor oruulah.webm", 6.408),
}

define MARGAD_QUESTIONS = [
    "Чи cosplayer юм бол яагаад багаа тайлахгүй байгаа юм бэ?",
    "Чи тэгээд ямар киноны юу гэдэг дүрийн өмсгөл өмссөн юм бэ?",
    "Наад цус чинь жинхэнэ үү?",
]

define MARGAD_QUESTION1_PART1 = "Чи cosplayer юм бол яагаад багаа тайлахгүй байгаа юм бэ?"
define MARGAD_QUESTION1_PART2 = "Наадах чинь баг юм бол яагаад ам нь хөдлөөд байгаа юм?"
define MARGAD_QUESTION1_PART3 = "Ийм тэнэг түүхэнд чинь итгэнэ гэж бодоо юу?"

define MARGAD_LINES = {
    "intro": "Хөөе, хөөе, битгий буудчихаарай. Би мангас биш шүү. Би cosplay арга хэмжээнд оролцоод явж байсан юм аа. Яг мангас шиг харагдаж байгаа биз? Хэхэ. Харин хүмүүс айж зугтаад л байна. Би хүн байна аа, битгий айгаарай гээд очихоор л царай хараад зугтаагаад байх юм.",
    "answer1": "Харин арга хэмжээн дээр баг маань салж унаад, манай найз бид хоёр яараад супер цавуу түрхэж байгаад янзалсан юм аа. Тэгсэн цавуу нь бүр бие, нүүртэй маань наалдчихаж.",
    "answer1_part2": "Энэ харин ам дагаж хөдөлдөг баг юм аа.",
    "answer1_part3": "Нээрээ. Намайг оруулж энэ багийг тайлахад туслаач.",
    "answer2": "Ёо, та анимэ үздэггүй юм уу даа. Харваас ойлгомжтой байгаа биз дээ. Яагаав, Naruto дээр гардаг шүү дээ. Яагаав, НАРУТО ШИППҮҮДЭН. Кагэ башин но жицү.",
    "answer3": "Энэ жинхэнэ цус биш ээ. Cosplay үзүүлбэрт ашигласан будаг шүү дээ. Та сайн хар л даа. Үнэртэх ч үгүй байгаа биз дээ. Ахаа, би яг өлсөж үхлээ. Оръё л доо.",
    "aim": "Больё оо, агаа. Байя, агаа.",
}

# Source-clock windows. Split answer-one clips seek within the same WebM.
define MARGAD_SPEECH_WINDOWS = {
    "intro": (0.000, 20.772),
    "answer1": (1.073, 11.525),
    "answer1_part2": (13.140, 16.414),
    "answer1_part3": (17.740, 22.040),
    "answer2": (1.231, 15.934),
    "answer3": (0.886, 8.965),
    "aim": (1.273, 4.022),
}

define MARGAD_SUPPLIED_PLAYER_VOICES = {
    "question1": ("audio/margad/margad asuult1 1heseg.wav", 0.090, 2.884),
    "question1_part2": ("audio/margad/margad asuult1 2heseg.wav", 0.101, 2.608),
    "question1_part3": ("audio/margad/margad asuult1 3heseg.wav", 0.101, 2.163),
    "question2": ("audio/margad/margad asuult2.wav", 0.000, 3.396),
    "question3": ("audio/margad/margad asuult3.wav", 0.082, 1.418),
}
