# Supplied Ganbaa recordings; keep their full framing and original soundtrack.
define GANBA_CLIPS = {
    "intro": ("Ehlel.webm", 29.168),
    "answer1": ("Ganbaa Hariult 1.webm", 13.808),
    "answer2": ("Ganbaa Hariult 2.webm", 13.368),
    "answer3": ("Ganbaa Hariult 3.webm", 7.008),
    "aim": ("Ganbaa Buu Gargaj ireed yarih.webm", 8.088),
    "lower": ("Ganbaa Buugaa buulgah.webm", 3.408),
    "shoot": ("Buudah.webm", 3.168),
    "admit": ("Ganbaa Oruulah.webm", 8.608),
    "reject": ("Ganbaa Yavuulah.webm", 9.568),
}
define GANBA_QUESTIONS = [
    "Та хаанаас ирж яваа юм бэ?",
    "Ханцуй дээрх улаан толбо чинь юу вэ?",
    "Тороо нээгээд харуул даа.",
]
define GANBA_LINES = {
    "intro": "Хүү минь, хаалгаа нээгээрэй. Архины үнэр үнэртэж байгааг мэдэж байна, гэхдээ би хэнд ч муу зүйл хийгээгүй. Өдөржин гадуур нуугдлаа, хөл хөлдөх нь ээ. Энэ нэг шил юмныхаа ачаар л хөлдчихөөгүй явна. Ахыгаа оруулбал ах нь хэрэгтэй хүн шүү. Залуудаа Монголд хоёрхон байдаг сөнөөгч онгоцны нисгэгч байлаа шүү дээ. Хэхэ.",
    "answer1": "Захын арын зооринд нуугдаж байгаад энэ нэг айхтар бужигнаан арай намдахаар гараад ирлээ. Нээрээ тэр зооринд зөндөө архи байна лээ. Би нэлээн хэдийг авчирсан шүү. Дуртай л биз дээ, дүү хүү. Хэхэ.",
    "answer2": "Гараа зүссэн нэг залууд тусалсан юм. Тэгсэн харин гэнэт над руу дайрдаг байна шүү дээ, муу моньд чинь. Гэхдээ ах нь харагдаж байгаа шигээ хүн биш ээ. Нэг цохиод л унагасан. Хэхэ.",
    "aim": "За, за! Би зүгээр л дулаан газар хайж явна. Битгий буудаарай.",
    "reject": "Зүгээр ээ, ямар сураагүй биш. Ах нь өөрөө зохицуулчихна.",
    "admit": "Еэ, гялай. Буянаараа дэлгэр. Орж ганц шил юм мултлах уу, цуг?",
}
define GANBA_SPEECH_WINDOWS = {
    "intro": (0.0, 27.50), "answer1": (0.394, 12.365),
    "answer2": (0.965, 12.069), "aim": (2.295, 6.525),
    "reject": (0.370, 3.830), "admit": (0.311, 4.588),
}

define GANBA_SUPPLIED_PLAYER_VOICES = {
    'question1': ('audio/ganba/ganba asuult1.wav', 0.122, 1.315),
    'question2': ('audio/ganba/ganba asuult2.wav', 0, 1.748),
    'question3': ('audio/ganba/ganba asuult3.wav', 0, 1.038),
}

init 1 python:
    shelter_register_visitor("ganba", roster_position=6, civilian=True,
        clips=GANBA_CLIPS, questions=GANBA_QUESTIONS, lines=GANBA_LINES,
        windows=GANBA_SPEECH_WINDOWS, supplied_voices=GANBA_SUPPLIED_PLAYER_VOICES,
        idle_still=("answer1", "start"), subtitle_y=580, subtitle_size=26)
