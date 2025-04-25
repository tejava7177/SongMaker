# 📄 File: chord_ai/genre_selector.py

def run_genre_selection():
    genres = ["jazz", "blues", "rock", "punk", "rnb"]
    print("\n🎷 사용할 스타일을 선택하세요:")
    print("  • ".join(genres))

    while True:
        selected = input("🎨 장르 입력: ").strip().lower()
        if selected in genres:
            print(f"✅ 선택된 장르: {selected}")
            return selected
        else:
            print("❗ 지원되지 않는 장르입니다. 다시 입력해주세요.")
