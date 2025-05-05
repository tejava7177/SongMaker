# 📄 app/generate_abc_notation.py
from app.generate_melody_line import generate_melody_line

MIDI_PROGRAMS = {
    "Acoustic Grand Piano": 1,
    "Electric Bass (fingered)": 34,
    "Distortion Guitar": 30,
    "Drawbar Organ": 17,
    "Synth Strings 1": 50,
    "Trumpet": 57,
    "Alto Sax": 66,
    "Flute": 74,
    "Percussion": 1,
}

def generate_drum_pattern(chords: list, swing_feel: bool = False) -> str:
    return ''.join(["| C/ z/ D/ z/ F/ z/ F/ z/ " for _ in chords])

def generate_structured_abc_notation(chords: list, bpm: int, style_info: dict):
    instrument_map = style_info["instrument_map"]
    emotion = style_info["emotion"]
    swing_feel = style_info["swing_feel"]

    instruments = list(instrument_map.keys())
    v1, v2 = instruments[0], instruments[1]
    melody = instruments[2] if len(instruments) > 2 else "Flute"

    v1_prog = MIDI_PROGRAMS[instrument_map[v1]]
    v2_prog = MIDI_PROGRAMS[instrument_map[v2]]
    v3_prog = MIDI_PROGRAMS[instrument_map.get(melody, "Flute")]
    drum_prog = MIDI_PROGRAMS["Percussion"]

    def make_voice_lines(section_chords):
        melo = generate_melody_line(section_chords, total_measures=len(section_chords), emotion=emotion)
        v1_notes = ''.join([f'| "{c}"c\' z c\' z c\' z c\' z ' for c in section_chords])
        v2_notes = ''.join([f'| "{c}"C, z C, z C, z C, z ' for c in section_chords])
        return v1_notes, v2_notes, melo

    sections = [("Intro", chords[:4]), ("Verse", chords[4:12]), ("Chorus", chords[12:16] if len(chords) >= 16 else chords[4:8])]
    abc_sections = [f"\n%% {label} Section\nV:1\n{v1_notes}\n\nV:2\n{v2_notes}\n\nV:3\n{melo}"
                    for label, ch in sections
                    for v1_notes, v2_notes, melo in [make_voice_lines(ch)]]

    header = f"""X:1
T:AI Structured Song
%%score (1 2 3 4)
M:4/4
L:1/8
Q:1/4={bpm}
K:C

V:1 name="{v1}" clef=treble
%%MIDI program {v1_prog}
%%MIDI channel 1

V:2 name="{v2}" clef=bass
%%MIDI program {v2_prog}
%%MIDI channel 2

V:3 name="{melody}" clef=treble
%%MIDI program {v3_prog}
%%MIDI channel 3

V:4 name="Drums" clef=perc
%%MIDI program {drum_prog}
%%MIDI channel 10
"""

    drum = generate_drum_pattern(chords, swing_feel)
    abc_code = header + "\n".join(abc_sections) + f"\n\nV:4\n{drum}"

    return abc_code, {
        "V1": instrument_map[v1],
        "V2": instrument_map[v2],
        "V3": instrument_map.get(melody, "Flute"),
        "V4": "Percussion"
    }