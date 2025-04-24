from music21 import converter, environment, note, stream, chord
import os

def midi_to_musicxml(midi_path: str, output_path: str):
    us = environment.UserSettings()
    us['musicxmlPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    score = converter.parse(midi_path)
    score.makeMeasures(inPlace=True)

    # ✅ 멜로디 노트만 추출
    filtered_score = stream.Score()
    for part in score.parts:
        new_part = stream.Part()
        for elem in part.flat.notesAndRests:
            # 1. 일반 음표 or 코드
            if isinstance(elem, (note.Note, chord.Chord)):
                new_part.append(elem)
            # 2. rest 도 유지
            elif isinstance(elem, note.Rest):
                new_part.append(elem)
            # 3. 드럼(PercussionChord, Unpitched)은 제외
        if len(new_part.notes) > 0:
            filtered_score.insert(0, new_part)

    # 🧱 마디 채우기
    for part in filtered_score.parts:
        for measure in part.getElementsByClass('Measure'):
            dur = measure.duration.quarterLength
            bar_dur = measure.barDuration.quarterLength
            if dur < bar_dur:
                rest_duration = bar_dur - dur
                measure.append(note.Rest(quarterLength=rest_duration))

    filtered_score.write('musicxml', fp=output_path)
    print(f"✅ MusicXML 생성 완료 (노트 기준 필터링 적용): {output_path}")

if __name__ == "__main__":
    midi_file = "/Users/simjuheun/Desktop/myProject/SongMaker/midi/testinput2.mid"
    xml_output = "/Users/simjuheun/Desktop/myProject/SongMaker/output/testinput2.musicxml"
    midi_to_musicxml(midi_file, xml_output)