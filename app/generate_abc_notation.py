from app.generate_melody_line import generate_melody_line

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

def generate_drum_pattern(chords: list, swing_feel: bool = False) -> str:
    pattern = ""
    for _ in chords:
        pattern += "| C/ z/ D/ z/ F/ z/ F/ z/ " if swing_feel else "| C/ z/ D/ z/ F/ z/ F/ z/ "
    return pattern

def generate_structured_abc_notation(chords: list, bpm: int, style_info: dict) -> str:
    emotion = style_info.get("emotion", "relaxed")
    swing_feel = style_info.get("swing_feel", False)

    instrument_map = style_info.get("instrument_map", {})
    instruments = [i for i in instrument_map if i.lower() != "drums"]
    v1_name = instruments[0] if len(instruments) > 0 else "Piano"
    v2_name = instruments[1] if len(instruments) > 1 else "Bass"

    v1_instr = instrument_map.get(v1_name, "Acoustic Grand Piano")
    v2_instr = instrument_map.get(v2_name, "Acoustic Bass")

    v1_prog = MIDI_PROGRAMS.get(v1_instr, 1)
    v2_prog = MIDI_PROGRAMS.get(v2_instr, 33)
    melody_prog = MIDI_PROGRAMS["Flute"]
    drum_prog = MIDI_PROGRAMS["Percussion"]

    unit = "1/8"
    beat_unit = 8

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
%%MIDI program {v1_prog}
%%MIDI channel 1

V:2 name="{v2_name}" clef=bass
%%MIDI program {v2_prog}
%%MIDI channel 2

V:3 name="Melody" clef=treble
%%MIDI program {melody_prog}
%%MIDI channel 3

V:4 name="Drums" clef=perc
%%MIDI program {drum_prog}
%%MIDI channel 10
"""

    return header + "\n".join(abc_sections) + f"""

V:4
{drum_line}
"""