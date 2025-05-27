import tkinter as tk
from tkinter import ttk, messagebox

class StyleSelectionView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_chords = []

        self.genre_var = tk.StringVar()
        self.emotion_var = tk.StringVar()
        self.instrument_vars = {}

        self.genres = ["jazz", "rock", "blues", "pop", "punk", "rnb"]
        self.emotions = ["relaxed", "excited", "sad", "romantic", "dark", "hopeful", "mysterious"]
        self.instruments = ["Piano", "Bass", "Strings", "Guitar", "Synth", "Organ", "Trumpet", "Saxophone"]

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="🎨 스타일 선택", font=("Helvetica", 18, "bold")).pack(pady=20)

        self.chord_label = ttk.Label(self, text="코드 진행: 없음", font=("Helvetica", 12))
        self.chord_label.pack(pady=5)

        ttk.Label(self, text="장르 선택:").pack()
        genre_menu = ttk.Combobox(self, textvariable=self.genre_var, values=self.genres, state="readonly")
        genre_menu.pack(pady=5)
        genre_menu.current(0)

        ttk.Label(self, text="감정 선택:").pack()
        emotion_menu = ttk.Combobox(self, textvariable=self.emotion_var, values=self.emotions, state="readonly")
        emotion_menu.pack(pady=5)
        emotion_menu.current(0)

        ttk.Label(self, text="사용할 악기 선택:").pack(pady=10)
        for inst in self.instruments:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self, text=inst, variable=var)
            chk.pack(anchor="w")
            self.instrument_vars[inst] = var

        ttk.Button(self, text="다음으로", command=self.submit).pack(pady=20)

    def receive_chords(self, chords):
        self.selected_chords = chords
        self.chord_label.config(text="코드 진행: " + ", ".join(chords))

    def submit(self):
        selected_instruments = [i for i, var in self.instrument_vars.items() if var.get()]
        if not selected_instruments:
            messagebox.showwarning("입력 오류", "최소 하나의 악기를 선택해주세요.")
            return

        result = {
            "chords": self.selected_chords,
            "genre": self.genre_var.get(),
            "emotion": self.emotion_var.get(),
            "instruments": selected_instruments
        }
        print("🎯 선택된 스타일 정보:", result)
        messagebox.showinfo("선택 완료", "스타일 선택이 완료되었습니다. 다음 단계를 진행하세요.")