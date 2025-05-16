import tkinter as tk
from tkinter import ttk, messagebox
from desktop_app.tuner_view import TunerView

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
        start_button = ttk.Button(self.root, text="▶ 코드 생성 시작하기", command=self.open_main_interface)
        start_button.pack(pady=10)

        # 튜너로 이동 버튼
        tuner_button = ttk.Button(self.root, text="🎵 기타 튜닝하기", command=self.open_tuner_view)
        tuner_button.pack(pady=10)

    def open_main_interface(self):
        messagebox.showinfo("준비 중", "코드 생성 기능은 다음 단계에서 구성됩니다.")

    def open_tuner_view(self):
        tuner_window = tk.Toplevel(self.root)
        tuner_window.title("기타 튜너")
        tuner_window.geometry("500x400")
        TunerView(tuner_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = SongMakerApp(root)
    root.mainloop()
