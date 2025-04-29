# 📄 File: chord_ai/instrument_selector.py

from chord_ai.instrument_recommender import genre_instrument_recommendations, instrument_replacement_map

def remove_duplicates_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def run_instrument_selection(genre: str) -> list:
    supported_instruments = [
        "Piano", "Bass", "Strings", "Guitar",
        "Synth", "Organ", "Trumpet", "Saxophone"
    ]

    recommended_instruments = genre_instrument_recommendations.get(genre, supported_instruments)

    print("\n🎯 추천 악기:", ", ".join(recommended_instruments))
    print("🎵 사용 가능한 악기 전체:")
    print("  - " + "\n  - ".join(supported_instruments))

    while True:
        user_input = input("악기 입력: ")
        instruments = [i.strip().capitalize() for i in user_input.split(",")]
        valid_instruments = [i for i in instruments if i in supported_instruments]

        if not valid_instruments:
            print("❗ 최소 1개의 유효한 악기를 선택해야 합니다.")
        else:
            break

    # 🎯 선택된 악기를 장르에 맞게 보정
    corrected_instruments = []
    replaced = []

    for inst in valid_instruments:
        if inst not in recommended_instruments:
            corrected = instrument_replacement_map.get(inst, recommended_instruments[0])
            corrected_instruments.append(corrected)
            replaced.append((inst, corrected))
        else:
            corrected_instruments.append(inst)

    # ✅ 항상 드럼 추가
    corrected_instruments.append("Drums")

    # ✅ 중복 제거 (순서 유지)
    corrected_instruments = remove_duplicates_preserve_order(corrected_instruments)

    # 📋 교체된 악기 알려주기
    if replaced:
        print("\n🔄 악기 자동 교체 안내:")
        for old, new in replaced:
            print(f"  - {old} → {new}")

    print(f"\n✅ 최종 선택된 악기: {', '.join(corrected_instruments)}")

    return corrected_instruments