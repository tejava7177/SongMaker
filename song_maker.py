# 📄 File: song_maker.py

from app.planner import interpret_genre_emotion
from app.generate_abc_notation import generate_abc_notation
from music21 import converter, environment
from datetime import datetime
import os

# 고정 출력 경로
OUTPUT_DIR = "/Users/simjuheun/Desktop/myProject/SongMaker/output"

def process_user_request(state: dict) -> tuple[str, str, str] | tuple[None, None, None]:
    """
    사용자 상태를 기반으로 ABC → MIDI → XML 파일 생성

    Returns:
        (abc_notation, midi_path, musicxml_path)
    """

    # 💡 MuseScore 경로 설정
    us = environment.UserSettings()
    us['musicxmlPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 🔍 스타일 추론
    style_info = interpret_genre_emotion(
        genre=state["genre"],
        emotion=state["emotion"],
        instruments=state["instruments"]
    )

    # 🎼 ABC 코드 생성
    abc_string = generate_abc_notation(
        chords=state["predicted"],
        bpm=state["bpm"],
        style_info=style_info
    )

    # 🕒 타임스탬프 파일 경로
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    midi_path = os.path.join(OUTPUT_DIR, f"generated_{timestamp}.mid")
    musicxml_path = os.path.join(OUTPUT_DIR, f"generated_{timestamp}.musicxml")

    # 🎯 MIDI 및 MusicXML 파일 생성
    try:
        score = converter.parse(abc_string, format='abc')
        score.write("midi", fp=midi_path)
        score.write("musicxml", fp=musicxml_path)
        print(f"\n✅ MIDI 및 악보 생성 완료:")
        print(f"🎵 MIDI → {midi_path}")
        print(f"📄 MusicXML → {musicxml_path}")
    except Exception as e:
        print("❌ 생성 실패:", e)
        return None, None, None

    return abc_string, midi_path, musicxml_path