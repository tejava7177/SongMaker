import tkinter as tk
from tkinter import ttk, messagebox

class ChordInputView:
    def __init__(self, parent, on_submit_callback):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.on_submit_callback = on_submit_callback

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.frame, text="🎼 코드 진행 입력", font=("Helvetica", 18, "bold")).pack(pady=20)

        ttk.Label(self.frame, text="쉼표로 구분된 코드 진행을 입력하세요 (예: C, G, Am, F)").pack(pady=5)

        self.chord_entry = ttk.Entry(self.frame, width=50)
        self.chord_entry.pack(pady=10)

        submit_button = ttk.Button(self.frame, text="다음으로", command=self.submit)
        submit_button.pack(pady=10)

    def submit(self):
        chord_text = self.chord_entry.get()
        if not chord_text.strip():
            messagebox.showwarning("입력 오류", "코드 진행을 입력하세요.")
            return

        chords = [c.strip() for c in chord_text.split(",") if c.strip()]
        if not chords:
            messagebox.showwarning("입력 오류", "유효한 코드가 없습니다.")
            return

        self.on_submit_callback(chords)