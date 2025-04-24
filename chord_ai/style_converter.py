# 장르변환
# 📄 File: chord_ai/style_converter.py

import re

# ✅ 스타일별 코드 변환 매핑
def apply_style(chord_progression, style="punk"):
    """
    주어진 코드 진행을 특정 장르 스타일로 변환
    예: jazz, blues, rock, punk, rnb
    """
    style_map = {
        "jazz": {
            "C Major": "Cmaj7", "G Major": "Gmaj7", "D Major": "Dmaj7",
            "A Minor": "Am7", "E Minor": "Em7", "F Major": "Fmaj7",
            "B Minor": "Bm7"
        },
        "blues": {
            "C Major": "C7", "G Major": "G7", "D Major": "D7",
            "A Major": "A7", "E Major": "E7", "F Major": "F7",
            "B Major": "B7"
        },
        "rock": {
            "C Major": "C5", "G Major": "G5", "D Major": "D5",
            "A Major": "A5", "E Major": "E5", "F Major": "F5"
        },
        "punk": {
            "C Major": "C5", "G Major": "G5", "D Major": "D5",
            "A Minor": "A5", "E Minor": "E5", "F Major": "F5",
            "B Major": "B5", "E Major": "E5", "A Major": "A5"
        },
        "rnb": {
            "C Major": "Cmaj9", "G Major": "G9", "D Major": "D9",
            "A Minor": "Am9", "E Minor": "Em9", "F Major": "Fmaj7",
            "B Major": "Bmaj9", "E Major": "Emaj9", "A Major": "Amaj9"
        }
    }

    styled_chords = [style_map.get(style, {}).get(chord, chord) for chord in chord_progression]
    return adjust_chord_progression(styled_chords, style)

# ✅ 장르별 코드 표현 보정 로직
def adjust_chord_progression(chords, style):
    adjusted_chords = chords[:]

    if style in ["punk", "rock"]:
        for i, chord in enumerate(adjusted_chords):
            if chord.endswith("maj7") or chord.endswith("7") or chord.endswith("9"):
                adjusted_chords[i] = chord[:-1] + "5"
            elif "Minor" in chord or "min" in chord:
                adjusted_chords[i] = chord.replace("Minor", "5").replace("min", "5")

    elif style == "reggae":  # 유지: 혹시 이후 확장 대비 남겨둠
        for i, chord in enumerate(adjusted_chords):
            if "Major" in chord and not chord.endswith("7"):
                adjusted_chords[i] = chord.replace("Major", "maj7")
            elif "Minor" in chord or "min" in chord:
                adjusted_chords[i] = chord.replace("Minor", "m7").replace("min", "m7")
            elif chord.endswith("7"):
                adjusted_chords[i] = chord.replace("7", "9")

    elif style == "rnb":
        for i, chord in enumerate(adjusted_chords):
            if "Major" in chord and not chord.endswith("7"):
                adjusted_chords[i] = chord.replace("Major", "maj9")
            elif "Minor" in chord or "min" in chord:
                adjusted_chords[i] = chord.replace("Minor", "m9").replace("min", "m9")
            elif chord.endswith("7"):
                adjusted_chords[i] = chord.replace("7", "maj7")

    elif style == "jazz":
        for i, chord in enumerate(adjusted_chords):
            if "Major" in chord:
                adjusted_chords[i] = chord.replace("Major", "maj7")
            elif "Minor" in chord:
                adjusted_chords[i] = chord.replace("Minor", "m7")

    elif style == "blues":
        for i, chord in enumerate(adjusted_chords):
            if chord.endswith("maj7"):
                adjusted_chords[i] = chord.replace("maj7", "7")
            elif chord.endswith("9"):
                adjusted_chords[i] = chord.replace("9", "7")

    return adjusted_chords

# ✅ 코드 포맷 정리 함수
def clean_chord_format(chord):
    chord = re.sub(r'(maj){2,}', 'maj', chord)
    chord = re.sub(r'(min){2,}', 'min', chord)
    chord = re.sub(r'\s+', '', chord)
    return chord
