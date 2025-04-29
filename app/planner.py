# 📄 File: app/planner.py

def interpret_genre_emotion(genre: str, emotion: str, instruments: list) -> dict:
    """
    장르, 감정, 사용자가 선택한 악기에 따라 스타일을 해석해서 리턴
    """

    # ✅ 기본 악기 매핑 (General MIDI Program Name)
    instrument_programs = {
        "Piano": "Acoustic Grand Piano",
        "Bass": "Acoustic Bass",
        "Strings": "String Ensemble 1",
        "Guitar": "Electric Guitar (clean)",
        "Synth": "Synth Strings 1",
        "Organ": "Drawbar Organ",
        "Trumpet": "Trumpet",
        "Saxophone": "Alto Sax",
        "Drums": "Standard Drum Kit"  # (드럼은 percussion으로 따로 처리할 수 있음)
    }

    # ✅ 장르 특성 반영해서, 악기 소리를 약간 바꿔줄 수도 있음
    genre_adjustments = {
        "jazz": {
            "Piano": "Electric Piano 1",
            "Bass": "Acoustic Bass",
            "Saxophone": "Tenor Sax"
        },
        "blues": {
            "Guitar": "Electric Guitar (clean)",
            "Organ": "Drawbar Organ"
        },
        "rock": {
            "Guitar": "Distortion Guitar",
            "Bass": "Electric Bass (finger)",
            "Synth": "Lead 1 (square)"
        },
        "punk": {
            "Guitar": "Overdriven Guitar",
            "Bass": "Electric Bass (pick)"
        },
        "rnb": {
            "Piano": "Electric Grand Piano",
            "Bass": "Fretless Bass",
            "Strings": "String Ensemble 2",
            "Synth": "Pad 2 (warm)"
        }
    }

    # ✅ 사용자 선택 악기들을 기반으로 instrument_map 생성
    instrument_map = {}
    for inst in instruments:
        default_sound = instrument_programs.get(inst, "Acoustic Grand Piano")  # fallback
        genre_override = genre_adjustments.get(genre, {}).get(inst)
        instrument_map[inst] = genre_override if genre_override else default_sound

    # ✅ 스윙 적용 여부
    swing_feel = genre == "jazz" and emotion in ["relaxed", "hopeful"]

    return {
        "swing_feel": swing_feel,
        "instrument_map": instrument_map,
        "emotion": emotion
    }