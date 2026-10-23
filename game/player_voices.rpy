# Supplied player speech, keyed by visitor and the actual choice it belongs to.
# Unreleased visitors are registered here without inventing missing encounters.
define SHELTER_SUPPLIED_PLAYER_VOICES = {
    'Swat': SWAT_SUPPLIED_PLAYER_VOICES,
    'anu': ANU_SUPPLIED_PLAYER_VOICES,
    'baatra': {
        'question1': ('audio/baatra/baatra asuult1.wav', 0, 1.118),
        'question2': ('audio/baatra/baatra asuult2.wav', 0, 1.18),
        'question3': ('audio/baatra/baatra asuult3.wav', 0, 1.567),
    },
    'ganba': GANBA_SUPPLIED_PLAYER_VOICES,
    'ganzo': GANZO_SUPPLIED_PLAYER_VOICES,
    'hulan': {
        'question1': ('audio/hulan/hulan asuult1.wav', 0, 2.608),
        'question2': ('audio/hulan/hulan asuult2.wav', 0, 1.643),
        'question3': ('audio/hulan/hulan asuult3.wav', 0, 2.182),
    },
    'margad': {
        'question1_part2': ('audio/margad/margad asuult1 2heseg.wav', 0.106, 2.587),
        'question1': ('audio/margad/margad asuult1.wav', 0.137, 2.859),
        'question2': ('audio/margad/margad asuult2.wav', 0.119, 3.39),
        'question3': ('audio/margad/margad asuult3.wav', 0, 1.408),
    },
    'naraa': {
        'question1': ('audio/naraa/naraa asuult1.wav', 0, 1.354),
        'question2_part1': ('audio/naraa/naraa asuult2 1heseg.wav', 0, 1.407),
        'question2_part2': ('audio/naraa/naraa asuult2 2heseg.wav', 0.103, 4.247),
        'question2': ('audio/naraa/naraa asuult2.wav', 0, 2.006),
        'question3': ('audio/naraa/naraa asuult3.wav', 0.136, 1.502),
    },
    'tsermaa': {
        'question1': ('audio/tsermaa/tsermaa asuult1.wav', 0.101, 1.145),
        'question2': ('audio/tsermaa/tsermaa asuult2.wav', 0.142, 2.122),
        'question3': ('audio/tsermaa/tsermaa asuult3.wav', 0.109, 0.897),
    },
    'tuguldur': {
        'question1': ('audio/tuguldur/tuguldur asuult1.wav', 0, 1.168),
        'question2': ('audio/tuguldur/tuguldur asuult2.wav', 0.116, 1.595),
        'question3': ('audio/tuguldur/tuguldur asuult3.wav', 0, 1.248),
    },
    'undral': {
        'question1': ('audio/undral/undral asuult1.wav', 0, 1.199),
        'question2': ('audio/undral/undral asuult2.wav', 0, 1.848),
        'question3': ('audio/undral/undral asuult3.wav', 0, 0.887),
    },
    'Chinba': CHINBA_SUPPLIED_PLAYER_VOICES,
}

define SHELTER_DEFAULT_PLAYER_VOICES = {
    "reject": ("audio/Chingune/MaralHuuh.wav", 0.344, 1.605),
    "admit": ("audio/Chingune/ChinbaOruulah.wav", 0.356, 0.815),
}

init 1 python:
    for visitor, data in SHELTER_VISITORS.items():
        data["voices"] = dict(data["voices"], **SHELTER_SUPPLIED_PLAYER_VOICES.get(visitor, {}))

    def shelter_player_voice(voice_key, visitor=None):
        visitor = visitor or shelter_visitor
        cue = SHELTER_VISITORS.get(visitor, {}).get("voices", {}).get(voice_key)
        if cue is None:
            cue = SHELTER_SUPPLIED_PLAYER_VOICES.get(visitor, {}).get(voice_key)
        if cue is not None:
            return cue
        # The pair has a dedicated plural rejection. Use a singular fallback
        # after one person has been shot, never replay the pair's wording.
        key = voice_key[len("survivor_"):] if voice_key.startswith("survivor_") else voice_key
        return SHELTER_DEFAULT_PLAYER_VOICES.get(key)
