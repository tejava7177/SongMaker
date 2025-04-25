# 📄 File: main.py

from chord_ai.chord_predictor import run_chord_prediction
from chord_ai.style_converter import apply_style, clean_chord_format
from chord_ai.genre_selector import run_genre_selection
from chord_ai.emotion_selector import run_emotion_selection
from chord_ai.instrument_selector import run_instrument_selection

# 🎯 상태 초기화
state = {
    "seed": [],
    "predicted": [],
    "genre": None,
    "emotion": None,
    "instruments": None
}

# ✅ 1단계: 코드 예측
state["seed"], state["predicted"] = run_chord_prediction()
# ✅ 2단계: 장르 설정
state["genre"] = run_genre_selection()
# ✅ 3단계: 감정 설정
state["emotion"] = run_emotion_selection()
# ✅ 4단계: 악기 설정
state["instruments"] = run_instrument_selection()


# 🧼 포맷 정리
formatted = [clean_chord_format(ch) for ch in state["predicted"]]

# 📋 진행 상황 출력
print("\n📋 현재 설정 상태:")
print("🎼 진행 코드:", " → ".join(state["seed"]))
print("🎷 장르:", state["genre"] or "아직 선택되지 않음")
print("🎭 감정:", state["emotion"] or "아직 선택되지 않음")
print("🎹 악기:", ", ".join(state["instruments"]) if state["instruments"] else "아직 선택되지 않음")

# 🎵 예측 결과 출력
print("\n🎼 AI가 예측한 코드 진행:")
print(" → ".join(formatted))