# 📄 File: chord_ai/chord_predictor.py

from chord_ai.predictor import predict_next_chords, chord_to_index
from chord_ai.style_converter import clean_chord_format

def run_chord_prediction():
    print("🔎 지원 코드 목록:")
    for chord in sorted(chord_to_index.keys()):
        print("-", chord)

    print("🎼 코드 진행 예측기 - SongMaker 버전")
    print("예시 입력: CMajor GMinor FMajor DMinor")
    print("🔤 시작 코드 4개를 입력하세요 (띄어쓰기 없이 코드명만 입력):")
    user_input = input("> ")
    seed_chords = user_input.strip().split()

    if len(seed_chords) < 4:
        raise ValueError("❗ 최소 4개의 코드를 입력해주세요.")

    predicted_chords = predict_next_chords(seed_chords, num_predictions=12, temperature=1.2)
    return seed_chords, predicted_chords