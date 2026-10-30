# swat encounter data: clips, dialogue and player speech.
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

define SWAT_SUPPLIED_PLAYER_VOICES = {
    'question1': ('audio/SwatQuestion/asuult1.wav', 0.496, 1.822),
    'question2': ('audio/SwatQuestion/asuult2.wav', 0.435, 3.128),
    'question3': ('audio/SwatQuestion/asuult3.wav', 0.257, 2.678),
    'admit': ('audio/SwatQuestion/oruulah.wav', 0.166, 0.656),
}

init 1 python:
    # Armor stops the bullet: Orgil leaves alive after being shot.
    shelter_register_visitor("Swat", roster_position=2, civilian=True,
        clips=SWAT_CLIPS, questions=SWAT_QUESTIONS, lines=SWAT_LINES,
        windows=SWAT_SPEECH_WINDOWS, supplied_voices=SWAT_SUPPLIED_PLAYER_VOICES,
        stills="frames", idle_still="idle", first_still="arrival",
        subtitle_y=630, subtitle_size=26, nonlethal_shoot=True)
