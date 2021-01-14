import tkinter as tk


class ThemeSubMenu(tk.Menu):
    def __init__(self, menu):
        super().__init__(menu, tearoff=0)

        self.add_command(label="Zoom in", accelerator='Ctrl+Plus', command=lambda: menu.navbar.parent.increase_fontsize(scale=5))
        self.add_command(label="Zoom out", accelerator='Ctrl+Minus', command=lambda: menu.navbar.parent.decrease_fontsize(scale=5))
        self.add_command(label="Zoom reset", accelerator='Ctrl+0', command=lambda: menu.navbar.parent.reset_fontsize())
