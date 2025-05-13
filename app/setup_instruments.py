from app.instrument_registry import InstrumentRegistry


def setup_registry(genre: str, emotion: str, user_instruments: list) -> dict:
    r = InstrumentRegistry()

    # 기본 악기 등록
    r.register("Piano", "Acoustic Grand Piano", "Piano")
    r.register("Bass", "Electric Bass (fingered)", "Electric Bass")

    # ✅ Guitar는 장르 기반으로 등록
    if genre in ["rock", "punk"]:
        r.register("Guitar", "Electric Guitar (distortion)", "Distorted Guitar")
    elif genre in ["folk", "classical"]:
        r.register("Guitar", "Acoustic Guitar (nylon)", "Acoustic Guitar")
    else:
        r.register("Guitar", "Electric Guitar (clean)", "Electric Guitar")

    r.register("Drums", "Percussion", "Unpitched Percussion")
    r.register("Organ", "Drawbar Organ", "Organ")
    r.register("Strings", "Synth Strings 1", "String Ensemble 1")
    r.register("Saxophone", "Alto Sax", "Alto Saxophone")
    r.register("Trumpet", "Trumpet", "Trumpet")
    r.register("Flute", "Flute", "Flute")

    # 🎭 감정 기반 우선순위 등록 (블루스 예시)
    blues_combo = {
        "relaxed": ["Guitar", "Organ", "Drums"],
        "excited": ["Guitar", "Drums", "Trumpet"],
        "sad": ["Guitar", "Bass", "Drums"],
        "romantic": ["Organ", "Saxophone", "Piano"],
        "dark": ["Guitar", "Drums", "Strings"],
        "hopeful": ["Guitar", "Piano", "Trumpet"],
        "mysterious": ["Organ", "Strings", "Drums"]
    }
    for emo, combo in blues_combo.items():
        r.register_priority("blues", emo, combo)

    # ✅ 실제 사용 악기 매핑
    instrument_map = {}
    for alias in user_instruments:
        gm = r.get_gm_name(alias)
        instrument_map[alias] = gm

    return instrument_map