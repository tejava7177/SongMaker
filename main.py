# 진입점 : CLI or API 트리거

from music21 import environment
from ai_song_maker import song_maker
from app.notation_generator import generate_abc_notation
from app.planner import interpret_genre_emotion


# MuseScore 경로 설정
us = environment.UserSettings()
us['musicxmlPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'

# 사용자 요청
user_request = {
    "chords": ["Cmaj7", "Am7", "Dm7", "G7"],
    "bpm": 100,
    "genre": "jazz",
    "emotion": "relaxed",
    "instruments": ["Piano", "Bass"]
}

# 스타일 추론
style_info = interpret_genre_emotion(
    user_request["genre"],
    user_request["emotion"]
)

# ABC 생성
abc_notation = generate_abc_notation(
    user_request["chords"],
    user_request["bpm"],
    style_info
)


instrument_map = style_info["instrument_map"]

# 출력 경로
musicxml_path = "output/generated.xml"
midi_path = "output/generated.mid"

# MIDI & MusicXML 생성
parts_data, score_data = song_maker.process_abc(
    abc_notation, instrument_map, musicxml_path, midi_path
)

print("✅ MIDI 파일 생성 완료:", midi_path)