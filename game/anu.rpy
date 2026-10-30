# anu encounter data: clips, dialogue and player speech.
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

define ANU_SUPPLIED_PLAYER_VOICES = {
    'question1': ('audio/anu/anu asuult1.wav', 0.255, 2.102),
    'question2': ('audio/anu/anu asuult2.wav', 0.104, 1.998),
    'question3': ('audio/anu/anu asuult3.wav', 0.165, 1.296),
    'drawing': ('audio/anu/anu zurag asuuh.wav', 0.213, 1.179),
}

init 1 python:
    shelter_register_visitor("anu", roster_position=4, civilian=False,
        clips=ANU_CLIPS, questions=ANU_QUESTIONS, lines=ANU_LINES,
        windows=ANU_SPEECH_WINDOWS, supplied_voices=ANU_SUPPLIED_PLAYER_VOICES,
        stills="frames", idle_still="idle",
        still_aliases={"arrival": "arrival_start", "enter": "admit", "leave": "reject"},
        monster_ending="Ану чөтгөр болон хувирч, тан руу дайрлаа.")
