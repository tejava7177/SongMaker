# 📄 File: rhythm/generate_strumming.py

import random
from music21 import stream, chord

# ① 스트로크 리듬 패턴 정의
STRUM_PATTERNS = [
    [1, 0.5, 0.5, 1],  # Down Up Up Down
    [0.5, 0.5, 1, 1],
    [1, 1, 0.5, 0.5],
    [0.25, 0.25, 0.5, 1, 1],
    [0.75, 0.75, 0.75, 0.75],  # 균등 스트럼
]

# ② 코드 구성음 예시 (더 확장 가능)
CHORD_NOTE_MAP = {
    "C": ["C4", "E4", "G4"],
    "Gm": ["G3", "Bb3", "D4"],
    "F": ["F3", "A3", "C4"],
    "Dm": ["D4", "F4", "A4"],
    "Csus4": ["C4", "F4", "G4"],
    "Edim": ["E4", "G4", "Bb4"],
    "Fsus4": ["F4", "Bb4", "C5"],
    "Cdim": ["C4", "Eb4", "Gb4"],
    "Bdim": ["B3", "D4", "F4"],
    "Daug": ["D4", "F#4", "A#4"]
}


# ③ 스트로크 마디 생성 함수
def generate_strumming_measure(chord_name: str) -> stream.Measure:
    pattern = random.choice(STRUM_PATTERNS)
    chord_notes = CHORD_NOTE_MAP.get(chord_name, ["C4", "E4", "G4"])

    m = stream.Measure()
    for duration in pattern:
        selected = random.sample(chord_notes, k=random.randint(2, len(chord_notes)))
        ch = chord.Chord(selected)
        ch.quarterLength = duration
        m.append(ch)
    return m