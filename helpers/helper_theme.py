from tkinter import colorchooser
from tkinter import messagebox
from utils import rgb_to_hex
from config import CONFIG
from state import State
from frames.frame_color import FrameColor
from frames.frame_font import FrameFont


class ThemeHelper:
    def __init__(self, navbar=None, parent=None):
        self.navbar = navbar
        self.parent = parent

        self.parent.textarea.bind('<Control-=>', self.increase_fontsize)
        self.parent.textarea.bind('<Control-minus>', self.decrease_fontsize)
        self.parent.textarea.bind('<Control-0>', self.reset_fontsize)

    def show_color_window(self):
        self.frame_color = FrameColor(root=self.parent.root, helper=self)
        self.frame_color.run()

    def show_font_window(self):
        self.frame_font = FrameFont(root=self.parent.root, helper=self)
        self.frame_font.run()

    def choose_background_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            State.background_color = color[1]
            State.linenumbering_color = rgb_to_hex([int(abs(i - 30)) for i in color[0]])
            self.frame_color.body_color_label.config(text=f'Background color: {State.background_color}')

    def reset_theme(self):
        State.background_color = CONFIG['DEFAULT_BACKGROUND_COLOR']
        State.foreground_color = CONFIG['DEFAULT_FOREGROUND_COLOR']
        State.linenumbering_color = CONFIG['DEFAULT_LINENUMBERINGAREA_BACKGROUND_COLOR']

        self.frame_color.body_color_label.config(text=f'Background color: {State.background_color}')
        self.frame_color.text_color_label.config(text=f'Foreground color: {State.foreground_color}')

    def choose_foreground_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            State.foreground_color = color[1]
            self.frame_color.text_color_label.config(text=f'Foreground color: {State.foreground_color}')

    def set_theme(self):
        self.parent.textarea.config(background=State.background_color, foreground=State.foreground_color)
        self.parent.linenumberingarea.config(background=State.linenumbering_color, foreground=State.foreground_color)
        messagebox.showinfo(title='Theme', message='Theme was changed')

    def on_listbox_select(self, e):
        selection = e.widget.curselection()
        if selection:
            State.font_family = e.widget.get(selection[0])
            self.frame_font.fonts_list_label.config(text=f'Font family: {State.font_family}')

    def set_font(self):
        size = self.frame_font.font_size_entry.get()
        try:
            State.font_size = int(size)
            State.font_family = State.font_family

            self.parent.textarea.config(font=(State.font_family, int(size)))
            self.parent.linenumberingarea.config(font=(State.font_family, int(size)))
            messagebox.showinfo(title='Font', message='Font was changed')
        except:
            messagebox.showerror(title='Font', message='Font size must be a number')

    def update_font(self):
        self.parent.textarea.config(font=(State.font_family, State.font_size))
        self.parent.linenumberingarea.config(font=(State.font_family, State.font_size))

    def increase_fontsize(self, e=None, scale=1):
        if State.font_size + scale > 300:
            return messagebox.showerror(title='Font', message='Font can not be greater than 300pt')
        State.font_size += scale
        self.update_font()

    def decrease_fontsize(self, e=None, scale=1):
        if State.font_size - scale < 2:
            return messagebox.showerror(title='Font', message='Font can not be smaller than 2pt')
        State.font_size -= scale
        self.update_font()

    def reset_fontsize(self, e=None):
        State.font_size = CONFIG['DEFAULT_FONT_SIZE']
        self.update_font()
