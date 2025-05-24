import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import threading
import time
import numpy as np
import pyaudio

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
CHANNELS = 1
RATE = 44100
CHUNK = 4096

class ChordFromGuitarView:
    def __init__(self, parent, on_submit_callback):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.on_submit_callback = on_submit_callback
        self.detected_notes = []
        self.selected_notes = []

        self.setup_ui()
        threading.Thread(target=self.capture_notes, daemon=True).start()

    def setup_ui(self):
        ttk.Label(self.frame, text="🎸 기타로 루트음을 입력 중...", font=("Helvetica", 18, "bold")).pack(pady=20)
        self.status_label = ttk.Label(self.frame, text="15초간 입력을 감지하고 있습니다...", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        self.note_frame = ttk.LabelFrame(self.frame, text="결과 확인 및 수정")
        self.note_frame.pack(pady=10)

        self.note_vars = {}

        self.submit_button = ttk.Button(self.frame, text="확인하고 다음으로", command=self.submit, state="disabled")
        self.submit_button.pack(pady=20)

    def update_note_checkboxes(self, top_notes):
        for widget in self.note_frame.winfo_children():
            widget.destroy()

        self.note_vars = {}
        for note in top_notes:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(self.note_frame, text=note, variable=var)
            cb.pack(anchor="w")
            self.note_vars[note] = var

        self.submit_button.config(state="normal")
        self.status_label.config(text="감지된 음을 확인하고 수정할 수 있습니다.")

    def get_closest_note(self, freq):
        return min(NOTE_FREQUENCIES, key=lambda note: abs(freq - NOTE_FREQUENCIES[note]))

    def capture_notes(self):
        p = pyaudio.PyAudio()
        stream = None  # ⬅️ 먼저 선언해두기
        try:
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            start_time = time.time()
            notes = []

            while time.time() - start_time < 15:
                data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
                mono = np.mean(data.reshape(-1, 2), axis=1).astype(np.int16)

                fft = np.fft.fft(mono)
                freqs = np.fft.fftfreq(len(fft), 1 / RATE)
                mags = np.abs(fft)

                pos_freqs = freqs[:len(freqs)//2]
                pos_mags = mags[:len(mags)//2]
                peak = pos_freqs[np.argmax(pos_mags)]

                if 80 <= peak <= 350:
                    note = self.get_closest_note(peak)
                    notes.append(note)

            top = [note for note, _ in Counter(notes).most_common(4)]
            self.detected_notes = top
            self.parent.after(0, lambda: self.update_note_checkboxes(top))

        finally:
            if stream:  # ⬅️ 에러가 나서 stream이 생성되지 않았을 경우 대비
                stream.stop_stream()
                stream.close()
                p.terminate()

    def submit(self):
        self.selected_notes = [note for note, var in self.note_vars.items() if var.get()]
        if not self.selected_notes:
            messagebox.showwarning("입력 오류", "최소 하나의 노트를 선택해주세요.")
            return
        self.on_submit_callback(self.selected_notes)