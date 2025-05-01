# # 📄 File: app/generate_abc_notation.py
#
# from app.generate_melody_line import generate_melody_line
#
# # 🎹 MIDI 프로그램 번호 매핑
# MIDI_PROGRAM_MAP = {
#     "Piano": 1,             # Acoustic Grand Piano
#     "Bass": 34,             # Electric Bass (finger)
#     "Guitar": 27,           # Electric Guitar (jazz)
#     "Strings": 49,          # String Ensemble
#     "Synth": 81,            # Lead 1 (square)
#     "Organ": 19,            # Church Organ
#     "Trumpet": 57,          # Trumpet
#     "Saxophone": 66,        # Alto Sax
#     "Flute": 74,            # Flute
#     "Clarinet": 71,         # Clarinet
#     "Vibraphone": 12,       # Vibraphone
#     "Harp": 47,             # Orchestral Harp
#     "Drums": 1              # 실제로는 Drum은 Channel 10을 쓰지만, 그냥 Piano로 표시
# }
#
# def generate_abc_notation(chords, bpm, style_info):
#     swing_feel = style_info.get("swing_feel", False)
#     emotion = style_info.get("emotion", "relaxed")
#     instruments = style_info.get("instruments", ["Piano", "Bass", "Drums"])
#
#     # 🎵 멜로디용 악기(Flute 고정) 설정
#     melody_instrument = "Flute"
#     melody_program = MIDI_PROGRAM_MAP.get(melody_instrument, 74)
#
#     # 🧩 전체 마디 수
#     total_measures = (len(chords) * 4) if swing_feel else len(chords)
#     melody_line = generate_melody_line(chords, total_measures=total_measures, emotion=emotion)
#     loop_chords = (chords * (total_measures // len(chords) + 1))[:total_measures]
#
#     # 🎛️ 기본 리듬 설정
#     if swing_feel:
#         rhythm_unit = "1/8"
#         base_rhythm = lambda chord: f'| "{chord}"c\' z c\' z c\' z c\' z '
#     else:
#         rhythm_unit = "1/4"
#         base_rhythm = lambda chord: f'| "{chord}"c\'2 z2 '
#
#     # 🎼 각 악기별로 ABC V파트 생성
#     parts_abc = ""
#     for idx, inst in enumerate(instruments):
#         v_num = idx + 1
#         prog_num = MIDI_PROGRAM_MAP.get(inst, 1)
#         parts_abc += f"""
# V:{v_num} clef=treble name="{inst}"
# %%MIDI program {prog_num}
#
# V:{v_num}
# {''.join([base_rhythm(chord) for chord in loop_chords])}
# """
#
#     # 🎼 멜로디 파트 추가 (V: 마지막+1)
#     melody_v_num = len(instruments) + 1
#     parts_abc += f"""
# V:{melody_v_num} clef=treble name="{melody_instrument}"
# %%MIDI program {melody_program}
#
# V:{melody_v_num}
# {melody_line}
# """
#
#     # 🧹 최종 ABC 문자열 반환
#     return f"""
# M:4/4
# L:{rhythm_unit}
# Q:1/4={bpm}
# K:C
# {parts_abc}
# """