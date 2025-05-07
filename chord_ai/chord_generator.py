# 📄 chord_ai/chord_generator.py

from chord_ai.chord_style_mapper import map_root_to_chord
import random

def generate_chord_progression(roots, genre, emotion, total_length=16):
    """
    사용자로부터 받은 4개의 근음을 기반으로, 분위기와 장르에 맞춘 코드 진행을 확장 생성합니다.
    """
    # 기본 코드 후보 생성
    base_chords = [map_root_to_chord(root, genre, emotion) for root in roots]

    progression = base_chords[:]

    # 중복 줄이기 위한 히스토리 관리
    recent_chords = progression[-4:]

    while len(progression) < total_length:
        # 랜덤 루트 선택 (최근과 겹치지 않도록)
        root = random.choice(roots)
        chord = map_root_to_chord(root, genre, emotion)

        # 겹치면 무작위 전환
        attempts = 0
        while chord in recent_chords and attempts < 3:
            chord = map_root_to_chord(root, genre, emotion)
            attempts += 1

        progression.append(chord)
        recent_chords = (recent_chords + [chord])[-4:]

    return progression