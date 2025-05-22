import tkinter as tk
from tkinter import ttk, messagebox
from desktop_app.tuner_view import TunerView
from desktop_app.chord_input_view import ChordInputView
from desktop_app.style_selection_view import StyleSelectionView

class SongMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C.B.B - Chord-Based Backing")
        self.root.geometry("600x400")
        self.root.configure(bg="#1e1e1e")

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Helvetica", 16))
        style.configure("TButton", font=("Helvetica", 12))

        # 타이틀
        title_label = ttk.Label(self.root, text="🎸 Welcome to C.B.B", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(40, 10))

        # 부제목
        subtitle_label = ttk.Label(self.root, text="AI 기반 코드 진행 & 백킹 트랙 생성 시스템")
        subtitle_label.pack(pady=(0, 30))

        # 시작 버튼
        start_button = ttk.Button(self.root, text="▶ 코드 생성 시작하기", command=self.open_chord_input_view)
        start_button.pack(pady=10)

        # 튜너로 이동 버튼
        tuner_button = ttk.Button(self.root, text="🎵 기타 튜닝하기", command=self.open_tuner_view)
        tuner_button.pack(pady=10)

    def open_chord_input_view(self):
        chord_window = tk.Toplevel(self.root)
        chord_window.title("코드 입력")
        chord_window.geometry("600x300")
        ChordInputView(chord_window, self.handle_chords)

    def handle_chords(self, chords):
        print("입력된 코드 진행:", chords)
        messagebox.showinfo("입력 확인", f"입력된 코드 진행: {', '.join(chords)}")
        self.open_style_selection_view()  # ⬅ 자동 연결 추가

    def open_tuner_view(self):
        tuner_window = tk.Toplevel(self.root)
        tuner_window.title("기타 튜너")
        tuner_window.geometry("500x400")
        TunerView(tuner_window)

    def open_style_selection_view(self):
        style_window = tk.Toplevel(self.root)
        style_window.title("스타일 선택")
        style_window.geometry("500x600")
        StyleSelectionView(style_window, self.handle_style_selection)

    def handle_style_selection(self, style_data):
        print("선택된 스타일 정보:", style_data)
        messagebox.showinfo("선택 확인",
                            f"장르: {style_data['genre']}\\n감정: {style_data['emotion']}\\n악기: {', '.join(style_data['instruments'])}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SongMakerApp(root)
    root.mainloop()