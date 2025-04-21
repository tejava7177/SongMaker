from app.melody_generator import generate_melody_line

def generate_abc_notation(chords, bpm, style_info):
    swing_feel = style_info.get("swing_feel", False)
    instrument_map = style_info.get("instrument_map", {})

    instruments = list(instrument_map.keys())
    v1_name = instruments[0] if len(instruments) > 0 else "Piano"
    v2_name = instruments[1] if len(instruments) > 1 else "Bass"

    v1_instr = instrument_map.get(v1_name, "Acoustic Grand Piano")
    v2_instr = instrument_map.get(v2_name, "Acoustic Bass")

    midi_program_map = {
        "Acoustic Grand Piano": 1,
        "Bright Acoustic Piano": 2,
        "Electric Piano 2": 6,
        "Electric Guitar (jazz)": 27,
        "Acoustic Bass": 33,
        "Electric Bass (finger)": 34,
    }

    v1_prog = midi_program_map.get(v1_instr, 1)
    v2_prog = midi_program_map.get(v2_instr, 33)

    # 전체 마디 수 설정 (ex: 16마디 생성 기준)
    total_measures = (len(chords) * 4) if swing_feel else len(chords)

    # 멜로디 생성
    melody_line = generate_melody_line(chords, total_measures)

    # 반복 코드 시퀀스 생성
    loop_chords = (chords * (total_measures // len(chords) + 1))[:total_measures]

    if swing_feel:
        rhythm_unit = "1/8"
        v1_lines = ''.join([f'| "{chord}"c\' z c\' z c\' z c\' z ' for chord in loop_chords])
        v2_lines = ''.join([f'| "{chord}"C, G, C, G, C, G, C, G, ' for chord in loop_chords])
    else:
        rhythm_unit = "1/4"
        v1_lines = ''.join([f'| "{chord}"c\'2 z2 ' for chord in loop_chords])
        v2_lines = ''.join([f'| "{chord}"C,2 G,2 ' for chord in loop_chords])

    return f"""
M:4/4
L:{rhythm_unit}
Q:1/4={bpm}
K:C

V:1 clef=treble name="{v1_name}"
%%MIDI program {v1_prog}

V:2 clef=bass name="{v2_name}"
%%MIDI program {v2_prog}

V:3 clef=treble name="Flute"
%%MIDI program 74

V:1
{v1_lines}

V:2
{v2_lines}

V:3
{melody_line}
"""