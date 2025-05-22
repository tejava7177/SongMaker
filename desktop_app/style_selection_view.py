import tkinter as tk
from tkinter import ttk, messagebox

class StyleSelectionView:
    def __init__(self, parent, on_submit_callback):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.on_submit_callback = on_submit_callback

        self.selected_genre = tk.StringVar()
        self.selected_emotion = tk.StringVar()
        self.selected_instruments = []

        self.genres = ["jazz", "rock", "blues", "pop", "punk", "rnb"]
        self.emotions = ["relaxed", "excited", "sad", "romantic", "dark", "hopeful", "mysterious"]
        self.instruments = ["Piano", "Bass", "Strings", "Guitar", "Synth", "Organ", "Trumpet", "Saxophone"]

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.frame, text="🎨 스타일 선택", font=("Helvetica", 18, "bold")).pack(pady=20)

        # 장르 선택
        ttk.Label(self.frame, text="장르를 선택하세요:").pack()
        genre_menu = ttk.Combobox(self.frame, textvariable=self.selected_genre, values=self.genres, state="readonly")
        genre_menu.pack(pady=5)
        genre_menu.current(0)

        # 감정 선택
        ttk.Label(self.frame, text="감정을 선택하세요:").pack()
        emotion_menu = ttk.Combobox(self.frame, textvariable=self.selected_emotion, values=self.emotions, state="readonly")
        emotion_menu.pack(pady=5)
        emotion_menu.current(0)

        # 악기 선택
        ttk.Label(self.frame, text="사용할 악기를 선택하세요:").pack(pady=10)
        self.instrument_vars = {}
        for instrument in self.instruments:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.frame, text=instrument, variable=var)
            chk.pack(anchor="w")
            self.instrument_vars[instrument] = var

        ttk.Button(self.frame, text="선택 완료", command=self.submit).pack(pady=20)

    def submit(self):
        selected_instruments = [inst for inst, var in self.instrument_vars.items() if var.get()]
        if not selected_instruments:
            messagebox.showwarning("입력 오류", "최소 하나의 악기를 선택해주세요.")
            return

        result = {
            "genre": self.selected_genre.get(),
            "emotion": self.selected_emotion.get(),
            "instruments": selected_instruments
        }
        self.on_submit_callback(result)