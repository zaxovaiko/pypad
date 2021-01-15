import tkinter as tk
from helpers.sub.theme import ThemeSubHelper


class ThemeSubMenu(tk.Menu):
    def __init__(self, menu):
        super().__init__(menu, tearoff=0)
        
        self.theme_sub_helper = ThemeSubHelper(navbar=menu.navbar, parent=menu.parent)

        self.add_command(label="Zoom in", accelerator='Ctrl+Plus', command=lambda: self.theme_sub_helper.increase_fontsize(scale=5))
        self.add_command(label="Zoom out", accelerator='Ctrl+Minus', command=lambda: self.theme_sub_helper.decrease_fontsize(scale=5))
        self.add_command(label="Zoom reset", accelerator='Ctrl+0', command=lambda: self.theme_sub_helper.reset_fontsize())
