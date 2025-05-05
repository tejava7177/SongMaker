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
}

# 🧑‍🎤 사용자 친화 이름 → 내부 표준 이름 (ABC)
USER_ALIAS_TO_INTERNAL = {
    "Piano": "Acoustic Grand Piano",
    "Guitar": "Electric Guitar (distortion)",
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
    "Electric Guitar (distortion)": "Distortion Guitar",
    "Electric Bass (fingered)": "Electric Bass",
    "Flute": "Flute",
    "Percussion": "Percussion",
    "Acoustic Bass": "Acoustic Bass",
    "Drawbar Organ": "Organ",
    "Synth Strings 1": "String Ensemble 1",
    "Trumpet": "Trumpet",
    "Alto Sax": "Alto Saxophone",
}


def get_internal_name(user_friendly_name: str) -> str:
    return USER_ALIAS_TO_INTERNAL.get(user_friendly_name, "Acoustic Grand Piano")


def get_abc_program_number(internal_name: str) -> int:
    return ABC_MIDI_PROGRAMS.get(internal_name, 1)


def get_music21_name(internal_name: str) -> str:
    return INTERNAL_TO_MUSIC21.get(internal_name, "Piano")


def resolve_all(state_instruments: list[str]) -> dict:
    """사용자 선택 악기 리스트 → ABC와 music21을 위한 전체 매핑"""
    result = {}
    for i, part in enumerate(["V1", "V2", "V3", "V4"]):
        if i < len(state_instruments):
            alias = state_instruments[i]
            internal = get_internal_name(alias)
            result[part] = get_music21_name(internal)
        elif part == "V4":  # 기본적으로 드럼 채널
            result["V4"] = get_music21_name("Percussion")
    return result