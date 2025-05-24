import numpy as np
import pyaudio
import time
from collections import Counter

NOTE_FREQUENCIES = {
    "E2": 82.41, "F2": 87.31, "F#2": 92.50, "G2": 98.00,
    "G#2": 103.83, "A2": 110.00, "A#2": 116.54, "B2": 123.47,
    "C3": 130.81, "C#3": 138.59, "D3": 146.83, "D#3": 155.56,
    "E3": 164.81, "F3": 174.61, "F#3": 185.00, "G3": 196.00,
    "G#3": 207.65, "A3": 220.00, "A#3": 233.08, "B3": 246.94,
    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13,
    "E4": 329.63,
}

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 4096

def get_closest_note(freq):
    closest_note = None
    min_diff = float('inf')
    for note, ref in NOTE_FREQUENCIES.items():
        diff = abs(freq - ref)
        if diff < min_diff:
            min_diff = diff
            closest_note = note
    return closest_note

def check_root():
    p = pyaudio.PyAudio()

    print("🎤 사용 가능한 오디오 입력 장치:")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev["maxInputChannels"] > 0:
            print(f"[{i}] {dev['name']}")

    device_id = int(input("🎛 사용할 입력 장치 ID를 선택하세요: "))

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_id,
                    frames_per_buffer=CHUNK)

    print("🎸 15초 동안 기타를 연주하세요 (루트음을 반복적으로 입력해도 좋아요)...")

    note_counts = []
    start_time = time.time()

    try:
        while time.time() - start_time < 15:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            mono_data = np.mean(data.reshape(-1, 2), axis=1).astype(np.int16)

            fft = np.fft.fft(mono_data)
            freqs = np.fft.fftfreq(len(fft), 1 / RATE)
            mags = np.abs(fft)

            pos_freqs = freqs[:len(freqs)//2]
            pos_mags = mags[:len(mags)//2]

            peak_freq = pos_freqs[np.argmax(pos_mags)]

            if 80 <= peak_freq <= 350:
                note = get_closest_note(peak_freq)
                note_counts.append(note)
                print(f"🎵 감지된 주파수: {peak_freq:.2f} Hz → {note}")


    finally:

        stream.stop_stream()

        stream.close()

        p.terminate()



    top_notes = [note for note, _ in Counter(note_counts).most_common(4)]
    print("입력된 음 →", ", ".join(top_notes))


if __name__ == "__main__":
    check_root()