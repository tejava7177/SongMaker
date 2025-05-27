import tkinter as tk
from tkinter import ttk, messagebox

class ChordInputView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="🎼 코드 진행 입력", font=("Helvetica", 18, "bold")).pack(pady=30)

        ttk.Label(self, text="쉼표로 구분된 코드 진행을 입력하세요 (예: C, G, Am, F)").pack(pady=5)

        self.entry = ttk.Entry(self, width=50)
        self.entry.pack(pady=10)

        submit_btn = ttk.Button(self, text="다음으로", command=self.submit)
        submit_btn.pack(pady=20)

    def submit(self):
        raw = self.entry.get()
        if not raw.strip():
            messagebox.showwarning("입력 오류", "코드 진행을 입력해주세요.")
            return

        chords = [c.strip() for c in raw.split(",") if c.strip()]
        if not chords:
            messagebox.showwarning("입력 오류", "유효한 코드가 없습니다.")
            return

        self.controller.pass_chords_to_style(chords)