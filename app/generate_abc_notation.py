from app.generate_melody_line import generate_melody_line
#from app.generate_abc_notation import MIDI_PROGRAMS  # ← 필요한 경우 상단에 정의된 딕셔너리로 이동


def generate_drum_pattern(chords: list, swing_feel: bool = False) -> str:
    pattern = ""
    for _ in chords:
        if swing_feel:
            pattern += "| C z D z F z F z "  # 재즈풍 드럼 (8분음표 스윙)
        else:
            pattern += "| C z D z F z F z "  # 락/펑크 기본 리듬
    return pattern

def generate_structured_abc_notation(chords: list, bpm: int, style_info: dict) -> str:
    emotion = style_info.get("emotion", "relaxed")
    swing_feel = style_info.get("swing_feel", False)

    instrument_map = style_info.get("instrument_map", {})
    instruments = list(instrument_map.keys())
    v1_name = instruments[0] if len(instruments) > 0 else "Piano"
    v2_name = instruments[1] if len(instruments) > 1 else "Bass"

    v1_instr = instrument_map.get(v1_name, "Acoustic Grand Piano")
    v2_instr = instrument_map.get(v2_name, "Acoustic Bass")


    v1_prog = MIDI_PROGRAMS.get(v1_instr, 1)
    v2_prog = MIDI_PROGRAMS.get(v2_instr, 33)
    melody_prog = 74  # Flute

    unit = "1/8" if swing_feel else "1/4"
    beat_unit = 8 if swing_feel else 4

    # 1. 섹션 나누기
    intro = chords[:4]
    verse = chords[4:12]
    chorus = chords[12:16] if len(chords) >= 16 else chords[4:8]

    def make_voice_lines(section_chords):
        melody = generate_melody_line(section_chords, total_measures=len(section_chords), emotion=emotion)
        if swing_feel:
            v1 = ''.join([f'| "{c}"c\' z c\' z c\' z c\' z ' for c in section_chords])
            v2 = ''.join([f'| "{c}"C, G, C, G, C, G, C, G, ' for c in section_chords])
        else:
            v1 = ''.join([f'| "{c}"c\'2 z2 ' for c in section_chords])
            v2 = ''.join([f'| "{c}"C,2 G,2 ' for c in section_chords])
        return v1, v2, melody

    abc_sections = []
    full_chords = []

    for label, section_chords in [("Intro", intro), ("Verse", verse), ("Chorus", chorus)]:
        v1, v2, melody = make_voice_lines(section_chords)
        abc_sections.append(f"""
%% {label} Section
V:V1
{v1}

V:V2
{v2}

V:V3
{melody}
""")
        full_chords += section_chords

    # 드럼 라인 생성
    drum_line = generate_drum_pattern(full_chords, swing_feel=swing_feel)

    header = f"""X:1
T:AI Structured Song
%%score (V1 V2 V3 V4)
M:4/4
L:{unit}
Q:1/4={bpm}
K:C

V:V1 name="{v1_name}" clef=treble
%%MIDI program {v1_prog}
%%MIDI channel 1

V:V2 name="{v2_name}" clef=bass
%%MIDI program {v2_prog}
%%MIDI channel 2

V:V3 name="Melody" clef=treble
%%MIDI program {melody_prog}
%%MIDI channel 3

V:V4 name="Drums" clef=perc
%%MIDI program 1
%%MIDI channel 10
"""

    return header + "\n".join(abc_sections) + f"""

V:V4
{drum_line}
"""