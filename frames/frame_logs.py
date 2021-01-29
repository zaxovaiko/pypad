import tkinter as tk
from state import State
from config import CONFIG


class FrameLogs(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root)

        self.parent = parent

        self.cursor_label = tk.Label(self, text='Ln 1, Col 0')
        self.cursor_label.grid(row=0, column=0)

        self.zoom_label = tk.Label(self, text='{:.2f}%'.format(State.font_size * 100 / CONFIG["DEFAULT_FONT_SIZE"]))
        self.zoom_label.grid(row=0, column=1)

        self.encoding_label = tk.Label(self, text='utf-8')
        self.encoding_label.grid(row=0, column=2)

        self.words_label = tk.Label(self, text='Words: 0')
        self.words_label.grid(row=0, column=3)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
