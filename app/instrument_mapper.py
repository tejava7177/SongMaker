# app/instrument_mapper.py

# 🎹 General MIDI Program Numbers (ABC 용)
ABC_MIDI_PROGRAMS = {
    "Electric Guitar (distortion)": 30,
    "Electric Bass (fingered)": 34,
    "Flute": 74,
    "Percussion": 1,
    "Acoustic Grand Piano": 1,
    "Acoustic Bass": 33,
    "Drawbar Organ": 17,
    "Synth Strings 1": 50,
    "Trumpet": 57,
    "Alto Sax": 66,
    "Acoustic Guitar (nylon)": 24,
}

# 🧑‍🎤 사용자 친화 이름 → 내부 표준 이름 (ABC)
USER_ALIAS_TO_INTERNAL = {
    "Piano": "Acoustic Grand Piano",
    "Guitar": "Acoustic Guitar (nylon)",  # ✅ 변경
    #"Guitar": "Electric Guitar (distortion)",
    "Bass": "Electric Bass (fingered)",
    "Drums": "Percussion",
    "Organ": "Drawbar Organ",
    "Strings": "Synth Strings 1",
    "Saxophone": "Alto Sax",
    "Trumpet": "Trumpet"
}

# 🧠 내부 이름 → music21 인식 이름
INTERNAL_TO_MUSIC21 = {
    "Acoustic Grand Piano": "Piano",
    # INTERNAL_TO_MUSIC21:
    "Electric Guitar (distortion)": "Distorted Guitar",  # 하나로만!
    "Electric Guitar (clean)": "Electric Guitar",
    "Electric Bass (fingered)": "Electric Bass",
    "Flute": "Flute",
    "Percussion": "Unpitched Percussion",
    "Acoustic Bass": "Acoustic Bass",
    "Drawbar Organ": "Organ",
    "Synth Strings 1": "String Ensemble 1",
    "Trumpet": "Trumpet",
    "Alto Sax": "Alto Saxophone",
    "Acoustic Guitar (nylon)": "Acoustic Guitar",
}


def get_internal_name(user_friendly_name: str, genre: str = None) -> str:
    if user_friendly_name == "Guitar":
        if genre in ["rock", "punk"]:
            return "Electric Guitar (distortion)"
        elif genre in ["folk", "classical"]:
            return "Acoustic Guitar (nylon)"
        else:
            return "Acoustic Guitar (nylon)"
    return USER_ALIAS_TO_INTERNAL.get(user_friendly_name, "Acoustic Grand Piano")


def get_abc_program_number(internal_name: str) -> int:
    return ABC_MIDI_PROGRAMS.get(internal_name, 1)


def get_music21_name(internal_name: str) -> str:
    return INTERNAL_TO_MUSIC21.get(internal_name, "Piano")


def resolve_all(state_instruments: list[str], genre: str = None) -> dict:
    result = {}
    for i, part in enumerate(["V1", "V2", "V3", "V4"]):
        if i < len(state_instruments):
            alias = state_instruments[i]
            internal = get_internal_name(alias, genre)
            result[part] = get_music21_name(internal)
        elif part == "V4":
            result["V4"] = get_music21_name("Percussion")
    return result