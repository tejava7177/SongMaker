import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import numpy as np
import pyaudio
from collections import Counter

# 전체 기타 음 정의
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


def get_closest_note(frequency):
    return min(NOTE_FREQUENCIES, key=lambda note: abs(frequency - NOTE_FREQUENCIES[note]))


def measure_background_noise(stream, duration=1):
    total_amplitude = 0
    sample_count = int(RATE / CHUNK * duration)

    for _ in range(sample_count):
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        total_amplitude += np.max(np.abs(data))

    background_noise_level = total_amplitude / sample_count
    return background_noise_level


def run_note_detector(device_id, callback, is_running):
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=device_id,
                        frames_per_buffer=CHUNK)

        background_noise_level = measure_background_noise(stream)
        threshold = background_noise_level * 2.0
        prev_freqs = []

        while is_running():
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            mono_data = np.mean(data.reshape(-1, 2), axis=1).astype(np.int16)

            amplitude = np.max(np.abs(mono_data))
            if amplitude < threshold:
                prev_freqs.clear()
                continue

            fft = np.fft.fft(mono_data)
            freqs = np.fft.fftfreq(len(fft), 1 / RATE)
            mags = np.abs(fft)

            positive_freqs = freqs[:len(freqs)//2]
            positive_mags = mags[:len(mags)//2]
            peak_freq = positive_freqs[np.argmax(positive_mags)]

            if not (80 <= peak_freq <= 350):
                prev_freqs.clear()
                continue

            prev_freqs.append(peak_freq)
            if len(prev_freqs) > 3:
                prev_freqs.pop(0)

            if len(set(round(f, 1) for f in prev_freqs)) == 1:
                note = get_closest_note(peak_freq)
                callback(note, peak_freq)
                prev_freqs.clear()

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


class ChordFromGuitarView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.selected_device_index = None
        self.is_running = False
        self.last_detected_time = time.time()
        self.detected_notes = []
        self.note_vars = {}

        self.setup_ui()
        self.populate_input_devices()

    def setup_ui(self):
        ttk.Label(self.frame, text="🎸 기타 음을 입력 중...", font=("Helvetica", 18, "bold")).pack(pady=20)

        self.device_combo = ttk.Combobox(self.frame, state="readonly")
        self.device_combo.pack(pady=5)
        self.device_combo.bind("<<ComboboxSelected>>", self.on_device_selected)

        self.start_button = ttk.Button(self.frame, text="감지 시작", command=self.start_note_detection)
        self.start_button.pack(pady=10)

        self.status_label = ttk.Label(self.frame, text="입력 장치를 선택하고 '감지 시작'을 눌러주세요.", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

    def populate_input_devices(self):
        p = pyaudio.PyAudio()
        self.input_devices = []

        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                self.input_devices.append((i, info["name"]))

        self.device_combo["values"] = [name for _, name in self.input_devices]
        if self.input_devices:
            self.device_combo.current(0)
            self.selected_device_index = self.input_devices[0][0]

        p.terminate()

    def on_device_selected(self, event):
        index = self.device_combo.current()
        self.selected_device_index = self.input_devices[index][0]
        self.status_label.config(text="장치 선택 완료. 감지 시작을 눌러주세요.")

    def start_note_detection(self):
        if self.selected_device_index is None:
            messagebox.showwarning("장치 미선택", "먼저 입력 장치를 선택해주세요.")
            return

        self.status_label.config(text="15초간 감지 중입니다... 콘솔을 확인하세요.")
        self.is_running = True
        self.last_detected_time = time.time()
        self.detected_notes.clear()

        def is_running():
            return self.is_running and (time.time() - self.last_detected_time < 15)

        def callback(note, freq):
            print(f"현재 주파수: {freq:.2f} Hz → {note}")
            self.detected_notes.append(note)
            self.last_detected_time = time.time()

        threading.Thread(
            target=run_note_detector,
            args=(self.selected_device_index, callback, is_running),
            daemon=True
        ).start()

        self.parent.after(15000, self.finalize_detection)

    def finalize_detection(self):
        self.is_running = False

        if not self.detected_notes:
            self.status_label.config(text="감지 실패: 음이 감지되지 않았습니다.")
            return

        counter = Counter(self.detected_notes)
        top_notes = [note for note, _ in counter.most_common(4)]

        self.status_label.config(text="가장 많이 감지된 음을 선택하세요.")
        self.show_note_checkboxes(top_notes)

    def show_note_checkboxes(self, notes):
        if hasattr(self, 'note_frame'):
            self.note_frame.destroy()

        self.note_frame = ttk.LabelFrame(self.frame, text="감지된 음")
        self.note_frame.pack(pady=10)

        self.note_vars = {}
        for note in notes:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(self.note_frame, text=note, variable=var)
            cb.pack(anchor="w")
            self.note_vars[note] = var

        self.submit_button = ttk.Button(self.frame, text="확인하고 다음으로", command=self.submit_selection)
        self.submit_button.pack(pady=20)

    def submit_selection(self):
        selected = [note for note, var in self.note_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("입력 오류", "최소 하나의 음을 선택해주세요.")
            return
        print("✅ 선택된 음:", selected)
        self.status_label.config(text="선택 완료.")


# 실행
if __name__ == "__main__":
    root = tk.Tk()
    root.title("기타 코드 입력 감지기")
    ChordFromGuitarView(root)
    root.mainloop()