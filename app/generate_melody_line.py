# 📄 File: app/generate_melody_line.py

import random
from chord.chord_map import CHORD_TO_NOTES

def format_note(note: str, octave: int = 1) -> str:
    """노트를 ABC 표기법으로 변환"""
    accidental = ""
    base = note[0].lower()
    if "#" in note:
        accidental = "^"
    elif "b" in note:
        accidental = "_"
    return accidental + base + ("'" * octave)

def generate_melody_line(chords: list, total_measures: int = 16, emotion: str = "relaxed") -> str:
    """
    코드 진행과 감정(emotion)을 기반으로 멜로디 ABC 노테이션 생성
    - L:1/8 기준, 한 마디에 8개의 8분음표
    - 감정에 따라 음정(Octave), 음 선택 로직이 달라짐
    """
    melody = ""
    loop_chords = (chords * (total_measures // len(chords) + 1))[:total_measures]

    for chord in loop_chords:
        notes = CHORD_TO_NOTES.get(chord, ["C", "E", "G"])  # 모르는 코드면 C Major로 fallback
        bar_notes = []

        for idx in range(8):  # 한 마디 8음
            note = random.choice(notes)

            # 🎨 감정별 스타일 적용
            if emotion == "relaxed":
                octave = 1
            elif emotion == "excited":
                octave = random.choice([1, 2])
            elif emotion == "sad":
                octave = 0
                note = random.choice(notes[:2])  # 더 낮은 음 선택
            elif emotion == "romantic":
                octave = 1
                note = sorted(notes)[0]  # 낮은 음 선호
            elif emotion == "dark":
                octave = 0
                note = sorted(notes)[0]  # 낮은 음, 어두운 느낌
            elif emotion == "hopeful":
                octave = 1 + (idx // 4)  # 점진적 상승
                note = notes[idx % len(notes)]
            elif emotion == "mysterious":
                octave = random.choice([0, 1, 2])
            else:
                octave = 1

            note_abc = format_note(note, octave)
            bar_notes.append(note_abc)

        # 🎼 한 마디 완성
        melody += f'| "{chord}" ' + " ".join(bar_notes) + " "

    return melody.strip()