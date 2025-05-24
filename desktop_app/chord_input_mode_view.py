import tkinter as tk
from tkinter import ttk

class ChordInputModeView:
    def __init__(self, parent, on_text_mode, on_guitar_mode):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.on_text_mode = on_text_mode
        self.on_guitar_mode = on_guitar_mode

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.frame, text="🎼 코드 입력 방식 선택", font=("Helvetica", 18, "bold")).pack(pady=30)

        ttk.Label(self.frame, text="코드 진행을 입력할 방법을 선택하세요.").pack(pady=10)

        text_btn = ttk.Button(self.frame, text="✍️ 텍스트로 입력하기", command=self.on_text_mode)
        text_btn.pack(pady=10, ipadx=10, ipady=5)

        guitar_btn = ttk.Button(self.frame, text="🎸 기타 소리로 입력하기", command=self.on_guitar_mode)
        guitar_btn.pack(pady=10, ipadx=10, ipady=5)