# 📄 app/planner.py
from app.setup_instruments import setup_registry

def interpret_genre_emotion(genre: str, emotion: str, user_instruments: list) -> dict:
    registry = setup_registry()

    # ✅ 우선순위 자동 악기 추천
    auto_instruments = registry.get_priority(genre, emotion)
    merged = list(dict.fromkeys(user_instruments + auto_instruments))  # 순서 보존, 중복 제거

    # ✅ GM 이름으로 변환
    instrument_map = {alias: registry.get_gm_name(alias) for alias in merged}

    # ✅ 스윙 여부
    swing_feel = genre == "jazz" and emotion in ["relaxed", "hopeful"]

    return {
        "swing_feel": swing_feel,
        "instrument_map": instrument_map,
        "emotion": emotion
    }