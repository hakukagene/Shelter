# chinba encounter data: clips, dialogue and player speech.
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

define CHINBA_SUPPLIED_PLAYER_VOICES = {
    'question2': ('audio/Chingune/ChinbaAsuult2.wav', 0.686, 1.889),
}

init 1 python:
    # Reference-matched frames extracted from the source videos (not the supplied PNGs).
    # idle: Chinbaa hariult 3, first frame; aim: Chinbaa buuduulah, first frame.
    shelter_register_visitor("Chinba", roster_position=0, civilian=True,
        clips=CHINBA_CLIPS, questions=CHINBA_QUESTIONS, lines=CHINBA_LINES,
        windows=CHINBA_SPEECH_WINDOWS, voices=CHINBA_PLAYER_VOICES,
        supplied_voices=CHINBA_SUPPLIED_PLAYER_VOICES,
        stills="frames", idle_still="idle",
        frame_clips=("intro", "answer1", "answer2", "answer3", "aim", "lower",
            "arrival", "shoot", "admit", "reject"),
        first_still="arrival")
