import tkinter as tk
from config import CONFIG
from state import State


class FrameColor(tk.Toplevel):
    def __init__(self, root=None, helper=None):
        super().__init__(root)

        self.root = root
        self.helper = helper

        self.title(CONFIG['THEME_WINDOW_TITLE'])
        self.resizable(0, 0)

        self.body_color_label = tk.Label(self, text=f'Background color: {State.background_color}')
        self.body_color_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w')

        self.body_color_btn = tk.Button(self, text='Choose body color', command=self.helper.choose_background_color)
        self.body_color_btn.grid(row=1, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')

        self.text_color_label = tk.Label(self, text=f'Foreground color: {State.foreground_color}')
        self.text_color_label.grid(row=2, column=0, padx=10, sticky='w')

        self.text_color_btn = tk.Button(self, text='Choose text color', command=self.helper.choose_foreground_color)
        self.text_color_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')

        self.reset_theme = tk.Button(self, text='Reset', command=self.helper.reset_theme)
        self.reset_theme.grid(row=4, column=0, padx=(0, 5), pady=(0, 10), sticky='e')

        self.set_theme_btn = tk.Button(self, text='Set theme', command=self.helper.set_theme)
        self.set_theme_btn.grid(row=4, column=1, pady=(0, 10), sticky='e')

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.destroy())
        self.cancel_btn.grid(row=4, column=2, padx=(5, 10), pady=(0, 10), sticky='we')

    def run(self):
        self.mainloop()
