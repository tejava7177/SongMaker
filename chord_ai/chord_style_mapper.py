# 📄 chord_ai/chord_style_mapper.py

import random

EMOTION_CODE_TYPES = {
    "relaxed":    ["maj7", "m7", "add9"],
    "romantic":   ["maj7", "m7", "9", "sus2"],
    "excited":    ["7", "9", "sus4", "aug"],
    "sad":        ["m", "m7", "dim"],
    "dark":       ["m", "dim", "m6", "sus2"],
    "hopeful":    ["maj7", "6", "add9"],
    "mysterious": ["m7", "sus2", "dim7", "m9"]
}

GENRE_CODE_FILTERS = {
    "jazz":     ["maj7", "m7", "9", "13", "dim7", "7", "6", "m9"],
    "blues":    ["7", "9", "dim", "aug"],
    "rock":     ["5", "sus4", "7", "m"],
    "punk":     ["5", "m", "dim"],
    "rnb":      ["maj9", "m9", "add9", "sus2"],
    "folk":     ["maj", "m", "7"],
    "classical": ["maj", "min", "dim", "aug", "sus2"]
}

def map_root_to_chord(root: str, genre: str, emotion: str) -> str:
    base_types = EMOTION_CODE_TYPES.get(emotion, ["maj"])
    genre_filter = GENRE_CODE_FILTERS.get(genre, [])

    # 교집합 우선 사용, 없으면 감정 우선
    combined = [t for t in base_types if t in genre_filter] or base_types or ["maj"]

    suffix = random.choice(combined)
    return f"{root}{suffix}"