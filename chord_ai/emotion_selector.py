# 📄 File: chord_ai/emotion_selector.py


def run_emotion_selection() -> str:
    emotions = ["relaxed", "excited", "sad", "romantic", "dark", "hopeful", "mysterious"]

    print("\n🎭 사용할 감정을 선택하세요:")
    print("  • " + "  • ".join(emotions))

    emotion = input("감정 입력: ").lower()

    while emotion not in emotions:
        print("❗ 지원되지 않는 감정입니다. 다시 선택해주세요.")
        emotion = input("감정 입력: ").lower()

    print(f"✅ 선택된 감정: {emotion}")
    return emotion