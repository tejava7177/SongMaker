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

def format_note(note: str) -> str:
    if "#" in note:
        return "^" + note.replace("#", "").lower() + "'"
    elif "b" in note:
        return "_" + note.replace("b", "").lower() + "'"
    else:
        return note.lower() + "'"

def generate_melody_line(chords: list, total_measures: int = 16) -> str:
    """
    코드 진행을 기반으로 멜로디 ABC 노테이션을 생성
    각 마디에 8분음표 8개 (L:1/8 기준, 4/4 박자)
    """
    melody = ""
    loop_chords = (chords * (total_measures // len(chords) + 1))[:total_measures]

    for chord in loop_chords:
        notes = chord_notes_map.get(chord, ["C", "E", "G"])
        bar_notes = " ".join([format_note(random.choice(notes)) for _ in range(8)])
        melody += f'| "{chord}"{bar_notes} '

    return melody.strip()