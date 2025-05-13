# 📄 app/instrument_registry.py

class InstrumentRegistry:
    def __init__(self):
        self.alias_to_gm = {}
        self.gm_to_music21 = {}
        self.genre_emotion_priority = {}

    def register(self, alias, gm_name, music21_name=None):
        self.alias_to_gm[alias] = gm_name
        self.gm_to_music21[gm_name] = music21_name or gm_name

    def get_gm_name(self, alias):
        return self.alias_to_gm.get(alias, "Acoustic Grand Piano")

    def get_music21_name(self, gm_name):
        return self.gm_to_music21.get(gm_name, "Piano")

    def register_priority(self, genre: str, emotion: str, aliases: list):
        self.genre_emotion_priority[(genre.lower(), emotion.lower())] = aliases

    def get_priority(self, genre: str, emotion: str):
        return self.genre_emotion_priority.get((genre.lower(), emotion.lower()), ["Piano", "Bass", "Drums"])# 📄 app/instrument_registry.py

class InstrumentRegistry:
    def __init__(self):
        self.alias_to_gm = {}
        self.gm_to_music21 = {}
        self.genre_emotion_priority = {}

    def register(self, alias, gm_name, music21_name=None):
        self.alias_to_gm[alias] = gm_name
        self.gm_to_music21[gm_name] = music21_name or gm_name

    def get_gm_name(self, alias):
        return self.alias_to_gm.get(alias, "Acoustic Grand Piano")

    def get_music21_name(self, gm_name):
        return self.gm_to_music21.get(gm_name, "Piano")

    def register_priority(self, genre: str, emotion: str, aliases: list):
        self.genre_emotion_priority[(genre.lower(), emotion.lower())] = aliases

    def get_priority(self, genre: str, emotion: str):
        return self.genre_emotion_priority.get((genre.lower(), emotion.lower()), ["Piano", "Bass", "Drums"])