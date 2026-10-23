# Naraa - civilian encounter. Media supplied in game/Video/naraa/.
# Clip durations are not used by the current native/browser playback driver.
# They remain 0.0 until precise durations can be measured from the video files.
define NARAA_CLIPS = {
    "intro": ("Naraa Ehlel.webm", 0.0),
    "answer1": ("Naraa Hariult 1.webm", 0.0),
    "answer2": ("Naraa Hariult 2.1.webm", 0.0),
    "answer2_part2": ("Naraa Hariult 2.2.webm", 0.0),
    "answer3": ("Naraa Hariult 3.webm", 0.0),
    "aim": ("Naraa Buu gargahad hooloi.webm", 0.0),
    "lower": ("Naraa Buu Buulgah.webm", 0.0),
    "shoot": ("Naraa buuduulah.webm", 0.0),
    "admit": ("Naraa Oruulah.webm", 0.0),
    "reject": ("Naraa yavuulah.webm", 0.0),
}

# Player question captions. Naraa's exact spoken lines are preserved in the video
# soundtrack and intentionally not fabricated as text subtitles.
define NARAA_QUESTIONS = [
    "Чамд юу тохиолдоо вэ?",
    "Чамайг яагаад би оруулах ёстой вэ?",
    "Цүнхэнд чинь юу байгаа вэ?",
]
# Two separate player lines around Naraa's split second response.
define NARAA_QUESTION2_PART1 = "Чамайг яагаад би оруулах ёстой вэ?"
define NARAA_QUESTION2_PART2 = "Тиймээ гэхдээ би чамайг энгийн хүн гэж яагаад итгэх ёстой гэж?"

# Exact spoken content as supplied; video soundtracks remain the audio source.
define NARAA_LINES = {
    "answer2": "Наадах чинь хорогдох байр юм бишүү. Орж хорогдоё лдоо",
    "answer2_part2": "Би тиймч энгийн хүн биш лдээ. Заа лдаа ийм сайхан хүүхнийг үх гээд орхино гэж үү? Намайг оруулбал би хариуг чинь барина шүү. Яаж гэдгийг нь чи мэдэж байгаа биз дээ айн? кк",
}
define NARAA_SPEECH_WINDOWS = {}

# Naraa's question recordings are registered in player_voices.rpy.
