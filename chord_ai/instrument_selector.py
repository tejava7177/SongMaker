def run_instrument_selection() -> list:
    supported_instruments = [
        "Piano", "Bass", "Drums", "Strings", "Guitar",
        "Synth", "Organ", "Trumpet", "Saxophone", "Flute",
        "Clarinet", "Vibraphone", "Harp"
    ]

    print("\n🎹 사용할 악기를 선택하세요 (쉼표로 구분, 최소 1개):")
    print("  - " + "\n  - ".join(supported_instruments))

    while True:
        user_input = input("악기 입력: ")
        instruments = [i.strip().capitalize() for i in user_input.split(",")]
        valid_instruments = [i for i in instruments if i in supported_instruments]

        if not valid_instruments:
            print("❗ 최소 1개의 유효한 악기를 선택해야 합니다.")
        else:
            break

    print(f"✅ 선택된 악기: {', '.join(valid_instruments)}")
    return valid_instruments