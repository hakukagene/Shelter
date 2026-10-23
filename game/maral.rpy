# maral encounter data: clips, dialogue and player speech.
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
