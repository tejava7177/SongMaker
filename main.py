# 📄 File: main.py

# 📄 File: main.py

from chord_ai.predictor import predict_next_chords, chord_to_index
from chord_ai.style_converter import apply_style, clean_chord_format

# 🎹 지원 코드 목록 출력
print("🔎 지원 코드 목록:")
for chord in sorted(chord_to_index.keys()):
    print("-", chord)

print("\n🎼 코드 진행 예측기 - SongMaker 버전")
print("예시 입력: CMajor GMinor FMajor DMinor")
print("🔤 시작 코드 4개를 입력하세요 (띄어쓰기 없이 코드명만 입력):")

# 🎯 사용자 코드 입력
user_input = input("> ").strip()
tokens = user_input.split()

# ✅ 최소 4개 코드 입력 확인
if len(tokens) < 4:
    raise ValueError("❗ 최소 4개의 코드(CMajor, GMinor, ...)를 입력해주세요.")

seed_chords = tokens[:4]

# 🎵 장르 선택
print("\n🎷 사용할 스타일을 선택하세요: jazz, blues, rock, punk, rnb")
style = input("🎨 장르: ").lower()
if style not in ["jazz", "blues", "rock", "punk", "rnb"]:
    raise ValueError("❗ 지원되지 않는 스타일입니다.")

# 🤖 코드 예측
predicted_chords = predict_next_chords(seed_chords, num_predictions=12, temperature=1.2)

# 🎨 스타일 적용 및 포맷 정리
styled_chords = apply_style(predicted_chords, style)
cleaned_output = [clean_chord_format(c) for c in styled_chords]

# ✅ 결과 출력
print("\n🎼 AI가 생성한 코드 진행 (스타일 적용):")
print(" → ".join(cleaned_output))