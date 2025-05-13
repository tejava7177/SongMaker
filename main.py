# 📄 main.py
from chord_ai.chord_generator import generate_chord_progression
from chord_ai.genre_selector import run_genre_selection
from chord_ai.emotion_selector import run_emotion_selection
from chord_ai.instrument_selector import run_instrument_selection
from chord_ai.bpm_selector import run_bpm_selection
from app.planner import interpret_genre_emotion
from app.generate_abc_notation import generate_structured_abc_notation
from app.instrument_mapper import resolve_all
from ai_song_maker import song_maker

import os
from datetime import datetime

# ---------------------------------------------------
# 🎹 사용자 코드 근음 입력
user_roots = input("🎹 코드의 근음을 4개 입력하세요 (쉼표로 구분): ").split(",")
user_roots = [r.strip().capitalize() for r in user_roots if r.strip()][:4]

# ---------------------------------------------------
# 🎷 장르 / 감정 / 악기 / 템포 설정
genre = run_genre_selection()
emotion = run_emotion_selection()
instruments = run_instrument_selection(genre)
bpm = run_bpm_selection()

# ---------------------------------------------------
# 🎼 AI 코드 진행 생성 (LSTM + 감정/장르 스타일)
chords = generate_chord_progression(user_roots, genre, emotion)

# ---------------------------------------------------
# 📋 설정 요약 출력
print("\n📋 설정 요약")
print("🎼 근음:", " → ".join(user_roots))
print("🎷 장르:", genre)
print("🎭 감정:", emotion)
print("🎹 악기:", ", ".join(instruments))
print("⏱️ BPM:", bpm)
print("\n🎼 생성된 코드 진행:")
print(" → ".join(chords))

# ---------------------------------------------------
# 🎨 스타일 해석 및 ABC 코드 생성
style_info = interpret_genre_emotion(genre, emotion, instruments, bpm)
abc_code, ordered_internal_instruments = generate_structured_abc_notation(chords, bpm, style_info)

# ---------------------------------------------------
# 🎹 music21 악기 매핑
ordered_instruments = resolve_all(instruments, genre)

# ---------------------------------------------------
# 💾 출력 경로 생성
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("output", exist_ok=True)
xml_path = os.path.join("output", f"song_{timestamp}.musicxml")
midi_path = os.path.join("output", f"song_{timestamp}.mid")

# ---------------------------------------------------
# 🎶 음원 생성
parts_data, score_data = song_maker.process_abc(abc_code, ordered_instruments, xml_path, midi_path)


# ---------------------------------------------------
# ✅ 결과 출력
if abc_code:
    print("\n✅ 음악 생성 완료!")
    print(f"🎧 MIDI: {midi_path}")
    print(f"📄 악보: {xml_path}")
    print(f"🎛️ 최종 악기 매핑: {ordered_instruments}")
else:
    print("⚠️ 음악 생성에 실패했습니다.")