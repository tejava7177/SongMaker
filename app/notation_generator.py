def generate_abc_notation(chords, bpm, style_info):
    swing_feel = style_info.get("swing_feel", False)
    instruments = list(style_info.get("instrument_map", {}).keys())
    instrument_map = style_info.get("instrument_map", {})

    # MIDI 프로그램 번호 매핑
    midi_program_map = {
        "Acoustic Grand Piano": 1,
        "Bright Acoustic Piano": 2,
        "Electric Piano 2": 6,
        "Electric Guitar (jazz)": 27,
        "Acoustic Bass": 33,
        "Electric Bass (finger)": 34,
    }

    v1_name = instruments[0] if len(instruments) > 0 else "Piano"
    v2_name = instruments[1] if len(instruments) > 1 else "Bass"

    v1_instr = instrument_map.get(v1_name, "Acoustic Grand Piano")
    v2_instr = instrument_map.get(v2_name, "Acoustic Bass")

    v1_prog = midi_program_map.get(v1_instr, 1)
    v2_prog = midi_program_map.get(v2_instr, 33)

    if swing_feel:
        v1_lines = ''.join([f'| "{chord}"c\' z c\' z ' for chord in chords])
        v2_lines = ''.join([f'| "{chord}"C, G, C, G, ' for chord in chords])
        rhythm_unit = "1/8"
    else:
        v1_lines = ''.join([f'| "{chord}"c\'2 z2 ' for chord in chords])
        v2_lines = ''.join([f'| "{chord}"C,2 G,2 ' for chord in chords])
        rhythm_unit = "1/4"

    return f"""
M:4/4
L:{rhythm_unit}
Q:1/4={bpm}
K:C

V:1 clef=treble name="{v1_name}"
%%MIDI program {v1_prog}

V:2 clef=bass name="{v2_name}"
%%MIDI program {v2_prog}

V:1
{v1_lines}

V:2
{v2_lines}
"""