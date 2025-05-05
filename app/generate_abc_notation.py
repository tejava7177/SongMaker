from app.generate_melody_line import generate_melody_line

# ✅ MIDI program map
MIDI_PROGRAMS = {
    "Electric Guitar (distortion)": 30,
    "Electric Bass (fingered)": 34,
    "Flute": 74,
    "Percussion": 1,
    "Acoustic Grand Piano": 1,
    "Acoustic Bass": 33,
    "Drawbar Organ": 17,
    "Synth Strings 1": 50,
    "Trumpet": 57,
    "Alto Sax": 66
}

# ✅ User-friendly alias map
USER_INSTRUMENT_ALIAS = {
    "Piano": "Acoustic Grand Piano",
    "Guitar": "Electric Guitar (distortion)",
    "Bass": "Electric Bass (fingered)",
    "Drums": "Percussion",
    "Organ": "Drawbar Organ",
    "Strings": "Synth Strings 1",
    "Saxophone": "Alto Sax",
    "Trumpet": "Trumpet"
}

def generate_drum_pattern(chords: list, swing_feel: bool = False) -> str:
    return ''.join(["| C/ z/ D/ z/ F/ z/ F/ z/ " for _ in chords])

def generate_structured_abc_notation(chords: list, bpm: int, style_info: dict):
    emotion = style_info.get("emotion", "relaxed")
    swing_feel = style_info.get("swing_feel", False)

    raw_instruments = style_info.get("instrument_map", {})
    resolved_map = {
        part: USER_INSTRUMENT_ALIAS.get(part, "Acoustic Grand Piano")
        for part in raw_instruments
    }

    instruments = [i for i in resolved_map if i.lower() != "drums"]
    v1_name = instruments[0] if len(instruments) > 0 else "Piano"
    v2_name = instruments[1] if len(instruments) > 1 else "Bass"

    # ✨ 멜로디 악기 자동 선택
    melody_name_candidates = [i for i in instruments if i not in [v1_name, v2_name]]
    melody_name = melody_name_candidates[0] if melody_name_candidates else "Flute"
    melody_instr = resolved_map.get(melody_name, "Flute")

    v1_instr = resolved_map.get(v1_name, "Acoustic Grand Piano")
    v2_instr = resolved_map.get(v2_name, "Acoustic Bass")
    melody_prog = MIDI_PROGRAMS.get(melody_instr, 74)
    drum_prog = MIDI_PROGRAMS["Percussion"]

    unit = "1/8"

    # ✅ Split sections
    intro = chords[:4]
    verse = chords[4:12]
    chorus = chords[12:16] if len(chords) >= 16 else chords[4:8]

    def make_voice_lines(section_chords):
        melody = generate_melody_line(section_chords, total_measures=len(section_chords), emotion=emotion)
        v1 = ''.join([f'| "{c}"c\' z c\' z c\' z c\' z ' for c in section_chords])
        v2 = ''.join([f'| "{c}"C, z C, z C, z C, z ' for c in section_chords])
        return v1, v2, melody

    abc_sections = []
    full_chords = []

    for label, section_chords in [("Intro", intro), ("Verse", verse), ("Chorus", chorus)]:
        v1, v2, melody = make_voice_lines(section_chords)
        abc_sections.append(f"""
%% {label} Section
V:1
{v1}

V:2
{v2}

V:3
{melody}
""")
        full_chords += section_chords

    drum_line = generate_drum_pattern(full_chords, swing_feel=swing_feel)

    header = f"""X:1
T:AI Structured Song
%%score (1 2 3 4)
M:4/4
L:{unit}
Q:1/4={bpm}
K:C

V:1 name="{v1_name}" clef=treble
%%MIDI program {MIDI_PROGRAMS.get(v1_instr, 1)}
%%MIDI channel 1

V:2 name="{v2_name}" clef=bass
%%MIDI program {MIDI_PROGRAMS.get(v2_instr, 33)}
%%MIDI channel 2

V:3 name="{melody_name}" clef=treble
%%MIDI program {melody_prog}
%%MIDI channel 3

V:4 name="Drums" clef=perc
%%MIDI program {drum_prog}
%%MIDI channel 10
"""

    abc_code = header + "\n".join(abc_sections) + f"\n\nV:4\n{drum_line}"

    # 🎯 함께 instrument map도 반환
    ordered_instruments = {
        "V1": v1_instr,
        "V2": v2_instr,
        "V3": melody_instr,
        "V4": "Percussion"
    }

    return abc_code, ordered_instruments