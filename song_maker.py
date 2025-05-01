# 📄 File: song_maker.py (리팩토링 + 디버깅용 코드 트랙 분리 포함)

from music21 import stream, metadata, tempo, instrument, harmony, note, environment
from datetime import datetime
import os
from chord.CHORD_SYMBOL_MAP import CHORD_SYMBOL_MAP

def convert_to_chord_symbol(raw_name):
    """
    사용자 코드명(CMajor, GMinor 등)을 music21이 이해할 수 있는 코드명(C, Gm 등)으로 변환
    """
    return CHORD_SYMBOL_MAP.get(raw_name, raw_name)

def process_user_request(state: dict, output_dir="output"):
    """
    사용자 상태(state)를 바탕으로 다중 악기 트랙이 포함된 MusicXML 및 MIDI 파일 생성
    """
    us = environment.UserSettings()
    us['musicxmlPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'

    os.makedirs(output_dir, exist_ok=True)

    chords = state["predicted"]
    bpm = state["bpm"]
    instruments_list = state.get("instruments", ["Piano"])

    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = "AI Composition"

    tempo_mark = tempo.MetronomeMark(number=bpm)
    score.insert(0, tempo_mark)

    for inst_name in instruments_list:
        part = stream.Part()
        part.id = inst_name

        # 실제 악기 클래스가 존재하는지 확인 후 할당
        inst_class = getattr(instrument, inst_name, instrument.Piano)
        part.append(inst_class())

        for i, chord_name in enumerate(chords):
            m = stream.Measure(number=i + 1)

            # 코드 변환 및 디버깅 출력
            symbol = convert_to_chord_symbol(chord_name)
            try:
                cs = harmony.ChordSymbol(symbol)
                m.insert(0, cs)
            except Exception as e:
                print(f"⚠️ 코드 변환 실패: '{chord_name}' → '{symbol}' | 오류: {e}")
                continue

            # 디버깅용 음표 삽입
            base_note = note.Note(cs.root(), quarterLength=4.0)
            m.append(base_note)

            part.append(m)

        score.append(part)

    # 출력 경로 및 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_path = os.path.join(output_dir, f"generated_{timestamp}.musicxml")
    midi_path = os.path.join(output_dir, f"generated_{timestamp}.mid")

    try:
        score.write("musicxml", fp=xml_path)
        score.write("midi", fp=midi_path)
        print("\n✅ MIDI 및 악보 생성 완료:")
        print(f"🎵 MIDI → {midi_path}")
        print(f"📄 MusicXML → {xml_path}")
    except Exception as e:
        print("❌ 파일 저장 실패:", e)
        return None, None, None

    return None, midi_path, xml_path
