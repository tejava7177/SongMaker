# 📄 File: chord_ai/bpm_selector.py

def run_bpm_selection() -> int:
    while True:
        try:
            bpm = int(input("🎼 원하는 BPM을 입력하세요 (60 ~ 200 권장): "))
            if 30 <= bpm <= 300:
                print(f"✅ 선택된 BPM: {bpm}")
                return bpm
            else:
                print("❗ BPM은 30~300 사이로 입력해주세요.")
        except ValueError:
            print("❗ 숫자로 입력해주세요.")