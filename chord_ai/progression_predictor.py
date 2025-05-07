# 📄 chord_ai/progression_predictor.py

from chord_ai.chord_style_mapper import map_root_to_chord
from chord_ai.predictor import predict_next_chords
from chord_ai.style_converter import clean_chord_format


def generate_chord_progression_from_roots(roots, genre, emotion, num_predictions=12):
    """
    사용자로부터 받은 근음 리스트와 장르/감정에 따라 분위기 있는 코드 진행을 생성한다.

    1. 각 근음에 적합한 스타일 코드 적용 (예: C → Cm7)
    2. LSTM 모델로 자연스러운 코드 진행 예측
    3. 불필요한 텍스트 제거 및 포맷 정리

    Returns: 리스트[str] 예: ['Cm7', 'F7', 'Bbmaj7', ...]
    """
    # 1. 코드 스타일화 (감정/장르 적용)
    seed_chords = [map_root_to_chord(root, genre, emotion) for root in roots]

    # 2. LSTM으로 코드 예측
    predicted_chords = predict_next_chords(seed_chords, num_predictions=num_predictions)

    # 3. 포맷 정리
    cleaned = [clean_chord_format(ch) for ch in predicted_chords]

    return cleaned