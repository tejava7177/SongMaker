# 모델 로드 LSTM 모델 + 매핑 불러오기
# 코드 예측 시드 코드 입력 -> 다음 코드 12개 생성


# 📄 File: chord_ai/predictor.py

import numpy as np
import tensorflow as tf
import os

# ✅ 경로 설정 (상위에서 상대경로로 불러올 수 있도록 처리)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model/lstm_chord_model4.h5")
CHORD_MAP_PATH = os.path.join(BASE_DIR, "model/chord_to_index.npy")

# ✅ 모델과 코드 매핑 로드
model = tf.keras.models.load_model(MODEL_PATH)
chord_to_index = np.load(CHORD_MAP_PATH, allow_pickle=True).item()
index_to_chord = {v: k for k, v in chord_to_index.items()}

SEQUENCE_LENGTH = 4
NUM_FEATURES = len(chord_to_index)

# 🔥 Temperature Sampling

def sample_with_temperature(predictions, temperature=1.5):
    predictions = np.where(predictions == 0, 1e-8, predictions)
    predictions = np.log(predictions) / temperature
    exp_preds = np.exp(predictions)
    probabilities = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(probabilities), p=probabilities)

# 🎼 코드 인덱스를 원-핫 인코딩으로 변환
def one_hot_encode(sequence, num_features):
    encoded_sequence = np.zeros((len(sequence), num_features))
    for i, index in enumerate(sequence):
        encoded_sequence[i, index] = 1
    return encoded_sequence

# 🤖 다음 코드 예측 함수
def predict_next_chords(seed_chords, num_predictions=12, temperature=1.2):
    """
    입력: 코드명 리스트 (예: ['C Major', 'G Major', 'A Minor', 'D Minor'])
    출력: 예측된 코드명 리스트
    """
    try:
        seed_indices = [chord_to_index[chord] for chord in seed_chords]
    except KeyError as e:
        raise ValueError(f"존재하지 않는 코드입니다: {str(e)}")

    predicted_chords = seed_chords[:]
    sequence = seed_indices

    for _ in range(num_predictions):
        X_input = one_hot_encode(sequence, NUM_FEATURES).reshape(1, SEQUENCE_LENGTH, NUM_FEATURES)
        pred = model.predict(X_input, verbose=0)[0]
        next_index = sample_with_temperature(pred, temperature)
        next_chord = index_to_chord[next_index]
        predicted_chords.append(next_chord)
        sequence = sequence[1:] + [next_index]  # 슬라이딩 윈도우 적용

    return predicted_chords
