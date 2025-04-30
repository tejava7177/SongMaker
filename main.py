# 📄 File: main.py

from chord_ai.chord_predictor import run_chord_prediction
from chord_ai.style_converter import apply_style, clean_chord_format
from chord_ai.genre_selector import run_genre_selection
from chord_ai.emotion_selector import run_emotion_selection
from chord_ai.instrument_selector import run_instrument_selection
from chord_ai.bpm_selector import run_bpm_selection
from song_maker import process_user_request

# -----------------------------------------------------
# 🎯 상태 초기화
state = {
    "seed": [],
    "predicted": [],
    "genre": None,
    "emotion": None,
    "instruments": None,
    "bpm": None
}

# -----------------------------------------------------
# ✅ 사용자 입력 단계
state["seed"], state["predicted"] = run_chord_prediction()
state["genre"] = run_genre_selection()
state["emotion"] = run_emotion_selection()
state["instruments"] = run_instrument_selection(state["genre"])
state["bpm"] = run_bpm_selection()

# -----------------------------------------------------
# 🧼 포맷 정리
formatted = [clean_chord_format(ch) for ch in state["predicted"]]

# 📋 사용자 입력 요약 출력
print("\n📋 현재 설정 상태:")
print("🎼 진행 코드:", " → ".join(state["seed"]))
print("🎷 장르:", state["genre"])
print("🎭 감정:", state["emotion"])
print("🎹 악기:", ", ".join(state["instruments"]))
print("⏱️ BPM:", state["bpm"])

# 🎵 코드 예측 출력
print("\n🎼 AI가 예측한 코드 진행:")
print(" → ".join(formatted))

# -----------------------------------------------------
# 🎼 MIDI & 악보 생성
abc_code, midi_path, xml_path = process_user_request(state)

# ✅ 결과 출력
if abc_code:
    print("\n🎉 모든 프로세스 완료! 음악 생성 성공!")
else:
    print("⚠️ 음악 생성에 실패했습니다.")