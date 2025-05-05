# 📄 app/setup_instruments.py
from app.instrument_registry import InstrumentRegistry

def setup_registry():
    r = InstrumentRegistry()

    # 🎹 등록
    r.register("Piano", "Acoustic Grand Piano", "Piano")
    r.register("Bass", "Electric Bass (fingered)", "Electric Bass")
    r.register("Guitar", "Distortion Guitar", "Distorted Guitar")
    r.register("Drums", "Percussion", "Unpitched Percussion")
    r.register("Organ", "Drawbar Organ", "Organ")
    r.register("Strings", "Synth Strings 1", "String Ensemble 1")
    r.register("Saxophone", "Alto Sax", "Alto Saxophone")
    r.register("Trumpet", "Trumpet", "Trumpet")
    r.register("Flute", "Flute", "Flute")

    # 🎭 감정 기반 blues 예시 등록
    emotions = ["relaxed", "excited", "sad", "romantic", "dark", "hopeful", "mysterious"]
    blues_combo = {
        "relaxed": ["Guitar", "Organ", "Drums"],
        "excited": ["Guitar", "Drums", "Trumpet"],
        "sad": ["Guitar", "Bass", "Drums"],
        "romantic": ["Organ", "Saxophone", "Piano"],
        "dark": ["Guitar", "Drums", "Strings"],
        "hopeful": ["Guitar", "Piano", "Trumpet"],
        "mysterious": ["Organ", "Strings", "Drums"]
    }

    for emo in emotions:
        r.register_priority("blues", emo, blues_combo.get(emo, ["Guitar", "Bass", "Drums"]))

    return r