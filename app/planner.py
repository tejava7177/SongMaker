# 악기 / 장르 기반 구조 기획

# /app/planner.py

def interpret_genre_emotion(genre: str, emotion: str) -> dict:
    """
    장르와 감정에 따라 스타일 정보를 리턴하는 해석 함수
    """
    # 기본 악기 세트
    default_instruments = {
        "Piano": "Acoustic Grand Piano",
        "Bass": "Acoustic Bass"
    }

    # 장르 + 감정 조합으로 스타일 해석
    if genre == "jazz":
        if emotion == "relaxed":
            return {
                "swing_feel": True,
                "instrument_map": default_instruments
            }
        elif emotion == "dark":
            return {
                "swing_feel": False,
                "instrument_map": {
                    "Piano": "Electric Piano 2",
                    "Bass": "Acoustic Bass"
                }
            }

    elif genre == "rock":
        return {
            "swing_feel": False,
            "instrument_map": {
                "Piano": "Electric Guitar (jazz)",
                "Bass": "Electric Bass (finger)"
            }
        }

    elif genre == "pop":
        return {
            "swing_feel": False,
            "instrument_map": {
                "Piano": "Bright Acoustic Piano",
                "Bass": "Electric Bass (pick)"
            }
        }

    # 기본 fallback
    return {
        "swing_feel": False,
        "instrument_map": default_instruments
    }