import tkinter as tk
from tkinter import ttk, messagebox
import threading
import numpy as np
import pyaudio
from utils import tuner as tuner_module

class TunerView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.running = False
        self.device_id = None
        self.thread = None

        self.current_target_note = None

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.frame, text="🎸 기타 튜너 (Bass)", font=("Helvetica", 18, "bold")).pack(pady=10)

        ttk.Label(self.frame, text="오디오 입력 장치 선택:").pack(pady=5)
        self.device_combobox = ttk.Combobox(self.frame, width=50)
        self.device_combobox.pack(pady=5)
        self.load_devices()

        self.string_buttons_frame = ttk.Frame(self.frame)
        self.string_buttons_frame.pack(pady=10)

        for note in ["E2", "A2", "D3", "G3"]:
            ttk.Button(self.string_buttons_frame, text=note, command=lambda n=note: self.set_target_note(n)).pack(side="left", padx=10)

        self.current_note_label = ttk.Label(self.frame, text="튜닝할 줄을 선택하세요", font=("Helvetica", 14))
        self.current_note_label.pack(pady=10)

        self.highlight_note_label = tk.Label(self.frame, text="-", font=("Helvetica", 32, "bold"))
        self.highlight_note_label.pack(pady=10)

        self.detail_label = ttk.Label(self.frame, text="", font=("Helvetica", 12))
        self.detail_label.pack(pady=5)

        self.start_button = ttk.Button(self.frame, text="튜너 시작", command=self.toggle_tuner)
        self.start_button.pack(pady=10)

        self.status_label = ttk.Label(self.frame, text="상태: 대기 중", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

    def set_target_note(self, note):
        self.current_target_note = note
        self.current_note_label.config(text=f"🎯 {note} 줄을 튜닝합니다")

    def load_devices(self):
        self.p = pyaudio.PyAudio()
        self.device_map = {}
        devices = []

        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                name = f"ID {i}: {info['name']}"
                self.device_map[name] = i
                devices.append(name)

        self.device_combobox["values"] = devices
        if devices:
            self.device_combobox.current(0)

    def toggle_tuner(self):
        if not self.running:
            selected = self.device_combobox.get()
            if selected not in self.device_map:
                messagebox.showerror("오류", "올바른 장치를 선택하세요.")
                return
            if not self.current_target_note:
                messagebox.showwarning("안내", "튜닝할 줄(E/A/D/G)을 선택해주세요.")
                return
            self.device_id = self.device_map[selected]
            self.running = True
            self.start_button.config(text="중지")
            self.thread = threading.Thread(target=self.run_tuner, daemon=True)
            self.thread.start()
        else:
            self.running = False
            self.start_button.config(text="튜너 시작")
            self.status_label.config(text="상태: 중지됨")

    def run_tuner(self):
        def ui_callback(note, freq, status):
            self.status_label.config(text=f"상태: 측정 중…")
            if self.current_target_note and note == self.current_target_note:
                self.highlight_note_label.config(text=note, fg="green")
            else:
                self.highlight_note_label.config(text=note or "-", fg="red")

            target_freq = tuner_module.NOTE_FREQUENCIES.get(self.current_target_note, 0)
            self.detail_label.config(text=f"목표: {target_freq:.2f}Hz / 현재: {freq:.2f}Hz\n{status}")

        tuner_module.run_tuner_with_callback(self.device_id, ui_callback, lambda: self.running)

    def __del__(self):
        if hasattr(self, 'p'):
            self.p.terminate()