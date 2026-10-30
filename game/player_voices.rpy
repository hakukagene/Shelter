# Supplied player speech, keyed by visitor and the actual choice it belongs to.
# Registered visitors pass their recordings to shelter_register_visitor();
# unreleased visitors are listed here without inventing missing encounters.

define SHELTER_DEFAULT_PLAYER_VOICES = {
    "reject": ("audio/Chingune/MaralHuuh.wav", 0.344, 1.605),
    "admit": ("audio/Chingune/ChinbaOruulah.wav", 0.356, 0.815),
}

init 2 python:
    # Recordings for visitors whose encounters are not supplied yet.
    SHELTER_UNRELEASED_PLAYER_VOICES = {
        'baatra': {
            'question1': ('audio/baatra/baatra asuult1.wav', 0, 1.118),
            'question2': ('audio/baatra/baatra asuult2.wav', 0, 1.18),
            'question3': ('audio/baatra/baatra asuult3.wav', 0, 1.567),
        },
        'hulan': {
            'question1': ('audio/hulan/hulan asuult1.wav', 0, 2.608),
            'question2': ('audio/hulan/hulan asuult2.wav', 0, 1.643),
            'question3': ('audio/hulan/hulan asuult3.wav', 0, 2.182),
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
    }

    # Every supplied recording; tests and the fallback lookup read this table.
    SHELTER_SUPPLIED_PLAYER_VOICES = dict(SHELTER_UNRELEASED_PLAYER_VOICES, **{
        visitor: data["supplied_voices"] for visitor, data in SHELTER_VISITORS.items()
        if data["supplied_voices"]})

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
