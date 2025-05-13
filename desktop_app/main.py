import tkinter as tk
from tkinter import ttk

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
        start_button = ttk.Button(self.root, text="▶ 시작하기", command=self.open_main_interface)
        start_button.pack()

    def open_main_interface(self):
        # 이후 실제 UI 연결 예정
        tk.messagebox.showinfo("준비 중", "기능 연결 예정입니다. 다음 화면 개발 중!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SongMakerApp(root)
    root.mainloop()
