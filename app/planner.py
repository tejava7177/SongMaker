from app.setup_instruments import setup_registry

def interpret_genre_emotion(genre: str, emotion: str, instruments: list, bpm: int) -> dict:
    """
    장르/감정/악기/BPM 정보를 기반으로 스타일 분석 결과를 반환
    """
    # ✅ 내부 GM 이름 매핑
    instrument_map = setup_registry(genre, emotion, instruments)

    # 🎷 스윙 조건 판단
    swing_feel = (
        genre == "jazz" or
        (genre == "blues" and bpm < 100) or
        (emotion in ["relaxed", "hopeful", "romantic"] and genre in ["jazz", "rnb", "folk"])
    )

    return {
        "swing_feel": swing_feel,
        "instrument_map": instrument_map,
        "emotion": emotion,
        "genre": genre
    }