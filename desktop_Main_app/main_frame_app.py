import tkinter as tk
from tkinter import ttk
from desktop_Main_app.view.home_screen import HomeScreen
from desktop_Main_app.view.chordInputView import ChordInputView
from desktop_Main_app.view.chordFromGuitarView import ChordFromGuitarView
from desktop_Main_app.view.styleSelectionView import StyleSelectionView
from desktop_Main_app.view.tuner_view import TunerView

class SongMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C.B.B - Chord-Based Backing")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")

        self.container = ttk.Frame(root)
        self.container.pack(fill='both', expand=True)

        self.frames = {}

        self.page_classes = {
            "HomeScreen": HomeScreen,
            "ChordInputView": ChordInputView,
            "ChordFromGuitarView": ChordFromGuitarView,
            "StyleSelectionView": StyleSelectionView,
            "TunerView": TunerView
        }

        for name, PageClass in self.page_classes.items():
            frame = PageClass(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame_by_name("HomeScreen")

    def show_frame_by_name(self, name):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

    def pass_chords_to_style(self, chords):
        print("입력된 코드:", chords)
        style_view = self.frames.get("StyleSelectionView")
        if style_view:
            style_view.receive_chords(chords)
        self.show_frame_by_name("StyleSelectionView")

if __name__ == "__main__":
    root = tk.Tk()
    app = SongMakerApp(root)
    root.mainloop()