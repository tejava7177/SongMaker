# # 진입점 : CLI or API 트리거
#
# from music21 import environment
# from ai_song_maker import song_maker
# from app.notation_generator import generate_abc_notation
# from app.planner import interpret_genre_emotion
# from datetime import datetime
#
# # MuseScore 경로 설정
# us = environment.UserSettings()
# us['musicxmlPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
#
# # 사용자 요청
# user_request = {
#     "chords": ["Cmaj7", "Am7", "Dm7", "G7"],
#     "bpm": 100,
#     "genre": "jazz",
#     "emotion": "relaxed",
#     "instruments": ["Piano", "Bass"]
# }
#
# # 스타일 추론
# style_info = interpret_genre_emotion(
#     user_request["genre"],
#     user_request["emotion"]
# )
#
# # ABC 생성
# abc_notation = generate_abc_notation(
#     user_request["chords"],
#     user_request["bpm"],
#     style_info
# )
#
# instrument_map = style_info["instrument_map"]
#
# # 출력 경로
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# musicxml_path = f"output/generated_{timestamp}.xml"
# midi_path = f"output/generated_{timestamp}.mid"
#
# # MIDI & MusicXML 생성
# try:
#     parts_data, score_data = song_maker.process_abc(
#         abc_notation, instrument_map, musicxml_path, midi_path
#     )
#     print("✅ MIDI 파일 생성 완료:", midi_path)
# except Exception as e:
#     print("❌ 오류 발생:", e)


# 📄 File: main.py

from chord_ai.predictor import predict_next_chords
from chord_ai.style_converter import apply_style, clean_chord_format
from chord_ai.predictor import chord_to_index

print("🔎 지원 코드 목록:")
for chord in sorted(chord_to_index.keys()):
    print("-", chord)

# 🎯 사용자 입력 (CLI 기반)
print("🎼 코드 진행 예측기 - SongMaker 버전")
print("예시 입력: C Major G Major A Minor D Minor")
print("🔤 시작 코드 4개를 입력하세요 (예: C Major G Major A Minor D Minor):")
user_input = input("> ")
tokens = user_input.strip().split()

if len(tokens) < 8:
    raise ValueError("❗ 최소 4개의 코드(8개의 단어)를 입력해야 합니다.")

input_chords = [f"{tokens[i]} {tokens[i+1]}" for i in range(0, len(tokens), 2)]
seed_chords = input_chords[:4]

# 🎵 장르 선택
print("🎷 사용할 스타일을 선택하세요: jazz, blues, rock, punk, rnb")
style = input("🎨 장르: ").lower()
if style not in ["jazz", "blues", "rock", "punk", "rnb"]:
    raise ValueError("❗ 지원되지 않는 스타일입니다.")

# 🤖 코드 예측 수행
predicted_chords = predict_next_chords(seed_chords, num_predictions=12, temperature=1.2)

# 🎨 스타일 적용 및 포맷 정리
styled_chords = apply_style(predicted_chords, style)
cleaned_output = [clean_chord_format(c) for c in styled_chords]

# ✅ 결과 출력
print("\n🎼 AI가 생성한 코드 진행 (스타일 적용):")
print(" → ".join(cleaned_output))
