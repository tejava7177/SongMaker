from music21 import environment

# MuseScore 경로 설정
us = environment.UserSettings()
us['musicxmlPath'] = '/Applications/MuseScore 4.app/Contents/MacOS/mscore'

# 나머지 임포트
from ai_song_maker import song_maker

# 사용자 입력
chords = ["Cmaj7", "Am7", "Dm7", "G7"]
bpm = 100

# V:1 (Piano)용 ABC 노테이션 라인 생성
v1_lines = ''.join([f'| "{chord}"c\'2 z2 ' for chord in chords])
v2_lines = ''.join([f'| "{chord}"C,2 G,2 ' for chord in chords])

# 최종 ABC 문자열 조합 (f-string 사용 안함)
abc_notation = """
M:4/4
L:1/4
Q:1/4={}
K:C

V:1 clef=treble name="Piano"
V:2 clef=bass name="Bass"

V:1
{}

V:2
{}
""".format(bpm, v1_lines, v2_lines)

# 악기 매핑
instrument_map = {
    "Piano": "Acoustic Grand Piano",
    "Bass": "Acoustic Bass"
}

# 파일 경로
musicxml_path = "generated.xml"
midi_path = "generated.mid"

# MIDI 생성
parts_data, score_data = song_maker.process_abc(
    abc_notation, instrument_map, musicxml_path, midi_path
)

print("✅ MIDI 파일이 생성되었습니다: ", midi_path)