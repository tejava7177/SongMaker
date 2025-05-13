# 📄 File: app/patterns/piano.py


def generate_piano_comping(chords: list, genre: str, emotion: str, swing: bool = False) -> str:
    patterns = []
    for chord in chords:
        if swing:
            # 🎵 스윙: 쿼터-셋잇단 feel (long-short pattern)
            bar = f'| "{chord}"c\'3/ c\'/ c\'3/ c\'/ '
        else:
            # 🎵 일반: 균등한 8분음표
            bar = f'| "{chord}"c\' z c\' z c\' z c\' z '
        patterns.append(bar)
    return ''.join(patterns)


def _jazz_romantic_pattern(chords):
    """
    syncopated comping pattern for jazz + romantic feel
    | "Cmaj7" z/ c' z/ c' z/ z/ c' c' |
    """
    abc_lines = []
    for chord in chords:
        abc = f'| "{chord}" z/ c\' z/ c\' z/ z/ c\' c\' '
        abc_lines.append(abc)
    return "\n".join(abc_lines)


def _default_block_chords(chords):
    """
    fallback block chord style
    | "Cmaj7" c' z c' z c' z c' z |
    """
    return "\n".join([f'| "{ch}" c\' z c\' z c\' z c\' z ' for ch in chords])



def generate_piano_scale_line(chords: list, emotion: str = "relaxed") -> str:
    """
    감정 기반으로 오른손 스케일 연주를 생성합니다.
    - 각 마디에 8분음표로 스케일 진행을 넣습니다.
    - 추후 감정에 따라 스케일 종류 변경도 가능하게 설계합니다.
    """
    # 기본 스케일 틀 (메이저 중심, 감정 따라 분기 가능)
    scale_templates = {
        "relaxed": ["c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''"],
        "excited": ["c'", "e'", "g'", "b'", "a'", "f'", "d'", "c''"],  # 5도 점프 느낌
        "dark":    ["c'", "d'", "e♭'", "f'", "g'", "a♭'", "b♭'", "c''"],
        "sad":     ["c'", "d'", "e♭'", "f'", "g'", "a♭'", "b'", "c''"],
        "hopeful": ["c'", "d'", "e'", "g'", "a'", "b'", "c''", "d''"]
    }

    template = scale_templates.get(emotion, scale_templates["relaxed"])
    abc = ""

    for chord in chords:
        notes = " ".join([f'"{chord}"{n}/' for n in template])
        abc += f"| {notes} "

    return abc