import tkinter as tk
from tkinter import ttk

class HomeScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="🎸 Welcome to C.B.B", font=("Helvetica", 24, "bold"), anchor="center").pack(pady=30)
        ttk.Label(self, text="AI 기반 코드 진행 & 백킹 트랙 생성 시스템", font=("Helvetica", 14)).pack(pady=10)

        ttk.Button(
            self,
            text="✍️ 코드 입력 (텍스트)",
            command=lambda: self.controller.show_frame_by_name("ChordInputView")
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="🎸 코드 입력 (기타)",
            command=lambda: self.controller.show_frame_by_name("ChordFromGuitarView")
        ).pack(pady=10, ipadx=10, ipady=5)

        ttk.Button(
            self,
            text="🎨 스타일 선택 화면만 보기",
            command=lambda: self.controller.show_frame_by_name("StyleSelectionView")
        ).pack(pady=20, ipadx=10, ipady=5)