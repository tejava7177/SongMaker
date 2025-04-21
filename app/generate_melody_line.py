import random

chord_notes_map = {
    "Cmaj7": ["C", "E", "G", "B"],
    "Am7": ["A", "C", "E", "G"],
    "Dm7": ["D", "F", "A", "C"],
    "G7": ["G", "B", "D", "F"],
    "Fmaj7": ["F", "A", "C", "E"],
    "Em7": ["E", "G", "B", "D"],
    "E7": ["E", "G#", "B", "D"],
    "A7": ["A", "C#", "E", "G"],
}

def format_note(note: str, octave: int = 1) -> str:
    """Convert note to ABC notation with specified octave."""
    accidental = ""
    base = note[0].lower()
    if "#" in note:
        accidental = "^"
    elif "b" in note:
        accidental = "_"
    return accidental + base + ("'" * octave)

def generate_melody_line(chords: list, total_measures: int = 16, emotion: str = "relaxed") -> str:
    melody = ""
    loop_chords = (chords * (total_measures // len(chords) + 1))[:total_measures]

    for chord in loop_chords:
        notes = chord_notes_map.get(chord, ["C", "E", "G"])
        bar_notes = []

        for _ in range(8):  # 8 eighth-notes per bar (L:1/8)
            note = random.choice(notes)

            # Emotion-based modifiers
            if emotion == "relaxed":
                octave = 1
                note = note
            elif emotion == "excited":
                octave = random.choice([1, 2])
                note = random.choice(notes)
            elif emotion == "sad":
                octave = 0
                note = random.choice(notes[:2])
            elif emotion == "romantic":
                octave = 1
                note = sorted(notes)[0]  # favor lower notes
            elif emotion == "dark":
                octave = 0
                note = sorted(notes)[0]
            elif emotion == "hopeful":
                octave = 1 + (_ // 2 % 2)  # gradual rising pattern
                note = notes[_ % len(notes)]
            elif emotion == "mysterious":
                octave = random.choice([0, 1, 2])
                note = random.choice(notes)
            else:
                octave = 1

            note_abc = format_note(note, octave)
            bar_notes.append(note_abc)

        melody += f'| "{chord}"' + " ".join(bar_notes) + " "

    return melody.strip()
