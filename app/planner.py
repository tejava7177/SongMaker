def interpret_genre_emotion(genre: str, emotion: str) -> dict:
    """
    장르와 감정에 따라 스타일 정보를 리턴하는 해석 함수
    """
    # 기본 악기 세트
    default_instruments = {
        "Piano": "Acoustic Grand Piano",
        "Bass": "Acoustic Bass"
    }

    if genre == "jazz":
        if emotion == "relaxed":
            return {
                "swing_feel": True,
                "instrument_map": default_instruments,
                "emotion": emotion
            }
        elif emotion == "dark":
            return {
                "swing_feel": False,
                "instrument_map": {
                    "Piano": "Electric Piano 2",
                    "Bass": "Acoustic Bass"
                },
                "emotion": emotion
            }

    elif genre == "rock":
        return {
            "swing_feel": False,
            "instrument_map": {
                "Piano": "Electric Guitar (jazz)",
                "Bass": "Electric Bass (finger)"
            },
            "emotion": emotion
        }

    elif genre == "pop":
        return {
            "swing_feel": False,
            "instrument_map": {
                "Piano": "Bright Acoustic Piano",
                "Bass": "Electric Bass (pick)"
            },
            "emotion": emotion
        }

    # 기본 fallback
    return {
        "swing_feel": False,
        "instrument_map": default_instruments,
        "emotion": emotion
    }