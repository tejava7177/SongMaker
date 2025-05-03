from chord_ai.chord_predictor import run_chord_prediction
from chord_ai.style_converter import apply_style, clean_chord_format
from chord_ai.genre_selector import run_genre_selection
from chord_ai.emotion_selector import run_emotion_selection
from chord_ai.instrument_selector import run_instrument_selection
from chord_ai.bpm_selector import run_bpm_selection
from app.planner import interpret_genre_emotion
from app.generate_abc_notation import generate_structured_abc_notation
from ai_song_maker import song_maker

import os

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

print("\n🎼 AI가 예측한 코드 진행:")
print(" → ".join(formatted))

# -----------------------------------------------------
# 🎼 ABC Notation 생성
style_info = interpret_genre_emotion(state["genre"], state["emotion"], state["instruments"])
abc_code = generate_structured_abc_notation(formatted, state["bpm"], style_info)

# 🎹 악기 이름 → MIDI 악기 맵
ordered_instruments = {
    "V1": style_info["instrument_map"][state["instruments"][0]],
    "V2": style_info["instrument_map"][state["instruments"][1]],
    "V3": "Flute",
    "V4": "Standard Kit"
}

# 출력 경로
os.makedirs("output", exist_ok=True)
xml_path = os.path.join("output", "generated123.musicxml")
midi_path = os.path.join("output", "generated123.mid")

# -----------------------------------------------------
# 🎶 MIDI 생성
parts_data, score_data = song_maker.process_abc(abc_code, ordered_instruments, xml_path, midi_path)

# ✅ 결과 출력
if abc_code:
    print("\n🎉 모든 프로세스 완료! 음악 생성 성공!")
    print(f"🎧 MIDI 파일: {midi_path}")
    print(f"📄 악보 파일: {xml_path}")
else:
    print("⚠️ 음악 생성에 실패했습니다.")