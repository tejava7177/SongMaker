def generate_abc_notation(chords, bpm, style_info):
    swing_feel = style_info.get("swing_feel", False)
    instruments = list(style_info.get("instrument_map", {}).keys())

    v1_name = instruments[0] if len(instruments) > 0 else "Piano"
    v2_name = instruments[1] if len(instruments) > 1 else "Bass"

    if swing_feel:
        # 스윙 feel: 8분음표 4개 → 총 4박자 (L:1/8 기준)
        v1_lines = ''.join([f'| "{chord}"c\' z c\' z ' for chord in chords])
        v2_lines = ''.join([f'| "{chord}"C, G, C, G, ' for chord in chords])
        rhythm_unit = "1/8"
    else:
        # 기본 2분음표 2개 → 총 4박자 (L:1/4 기준)
        v1_lines = ''.join([f'| "{chord}"c\'2 z2 ' for chord in chords])
        v2_lines = ''.join([f'| "{chord}"C,2 G,2 ' for chord in chords])
        rhythm_unit = "1/4"

    return f"""
M:4/4
L:{rhythm_unit}
Q:1/4={bpm}
K:C

V:1 clef=treble name="{v1_name}"
V:2 clef=bass name="{v2_name}"

V:1
{v1_lines}

V:2
{v2_lines}
"""