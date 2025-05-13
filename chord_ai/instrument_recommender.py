# 📄 File: chord_ai/instrument_recommender.py

genre_instrument_recommendations = {
    "jazz": ["Piano", "Guitar", "Bass", "Saxophone", "Trumpet", "Drums"],
    "blues": ["Guitar", "Piano", "Bass", "Organ", "Trumpet", "Saxophone","Drums"],
    "rock": ["Guitar", "Bass", "Synth", "Piano", "Drums"],
    "punk": ["Guitar", "Bass", "Synth", "Drums"],
    "rnb": ["Piano", "Bass", "Strings", "Synth", "Drums"]
}

instrument_replacement_map = {
    # 악기 → 기본 추천 악기로 교체
    "Strings": "Guitar",
    "Organ": "Piano",
    "Synth": "Piano",    # (Jazz, Blues일 경우만)
    "Harp": "Piano",
    "Flute": "Saxophone",
    "Clarinet": "Saxophone",
    "Vibraphone": "Piano",
}