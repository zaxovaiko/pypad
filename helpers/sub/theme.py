from config import CONFIG
from tkinter import messagebox
from helpers.theme import ThemeHelper


class ThemeSubHelper(ThemeHelper):
    def __init__(self, navbar=None, parent=None):
        super().__init__(navbar, parent)

    def update_font(self):
        self.parent.textarea.config(font=(self.font_family, self.font_size))
        self.parent.linenumberingarea.config(font=(self.font_family, self.font_size))

    def increase_fontsize(self, e=None, scale=1):
        if self.font_size + scale > 300:
            return messagebox.showerror(title='Font', message='Font can not be greater than 300pt')
        self.font_size += scale
        self.update_font()

    def decrease_fontsize(self, e=None, scale=1):
        if self.font_size - scale < 2:
            return messagebox.showerror(title='Font', message='Font can not be smaller than 2pt')
        self.font_size -= scale
        self.update_font()

    def reset_fontsize(self, e=None):
        self.font_size = CONFIG['DEFAULT_FONT_SIZE']
        self.update_font()