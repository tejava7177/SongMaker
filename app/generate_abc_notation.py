# 음원 생성 (ABC + MIDI)


from app.generate_melody_line import generate_melody_line

# General MIDI 프로그램 넘버 매핑
MIDI_PROGRAMS = {
    "Acoustic Grand Piano": 1,
    "Electric Piano 2": 6,
    "Electric Guitar (jazz)": 27,
    "Bright Acoustic Piano": 2,
    "Electric Bass (finger)": 34,
    "Acoustic Bass": 33,
    "Flute": 74,
    "Synth Strings 1": 50,
    "Drawbar Organ": 17,
    "Trumpet": 57,
    "Saxophone": 66,
    "Guitar (nylon)": 24,
    "Vibraphone": 11,
    "Clarinet": 72,
    "Harp": 46,
    "Strings": 49
}


def generate_abc_notation(chords: list, bpm: int, style_info: dict) -> str:
    swing_feel = style_info.get("swing_feel", False)
    instrument_map = style_info.get("instrument_map", {})
    emotion = style_info.get("emotion", "relaxed")

    instruments = list(instrument_map.keys())
    v1_name = instruments[0] if len(instruments) > 0 else "Piano"
    v2_name = instruments[1] if len(instruments) > 1 else "Bass"

    v1_instr = instrument_map.get(v1_name, "Acoustic Grand Piano")
    v2_instr = instrument_map.get(v2_name, "Acoustic Bass")

    v1_prog = MIDI_PROGRAMS.get(v1_instr, 1)
    v2_prog = MIDI_PROGRAMS.get(v2_instr, 33)

    # 전체 마디 수 계산
    total_measures = (len(chords) * 4) if swing_feel else len(chords)

    # 🎵 감정 기반 멜로디 라인 생성
    melody_line = generate_melody_line(chords, total_measures=total_measures, emotion=emotion)

    # 코드 반복 시퀀스 (리듬 트랙, 베이스 트랙에 사용)
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

V:3 clef=treble name="Melody"
%%MIDI program 74

V:1
{v1_lines}

V:2
{v2_lines}

V:3
{melody_line}
"""