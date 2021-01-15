import os
import re
import tkinter as tk
from config import CONFIG
from utils import Utils
from navbar import Navbar
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog


class App(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.width = CONFIG['DEFAULT_WIDTH']
        self.height = CONFIG['DEFAULT_HEIGHT']
        self.min_width = CONFIG['MIN_APP_WINDOW_WIDTH']
        self.min_height = CONFIG['MIN_APP_WINDOW_HEIGHT']

        self.filename = CONFIG['DEFAULT_NAME']
        self.font_family = CONFIG['DEFAULT_FONT_FAMILY']
        self.font_size = CONFIG['DEFAULT_FONT_SIZE']

        self.is_modified = False
        self.is_saved = False

        root.title(CONFIG['DEFAULT_TITLE'])
        root.geometry(f'{self.width}x{self.height}')
        root.minsize(width=self.min_width, height=self.min_height)

        # Horizontal scrollbar
        self.scrollbar_h = tk.Scrollbar(root, orient='horizontal')
        self.scrollbar_h.grid(row=1, column=1, sticky='ew')

        # Main textarea
        self.textarea = scrolledtext.ScrolledText(root, font=(self.font_family, self.font_size), borderwidth=0, highlightthickness=0, wrap='none', xscrollcommand=self.scrollbar_h.set)
        self.textarea.grid(row=0, column=1, sticky='nsew')
        self.textarea.tag_configure('highlightline', background=CONFIG['DEFAULT_HIGHLIGHTLINE_BACKGROUND'], relief='raised', foreground=CONFIG['DEFAULT_HIGHLIGHTLINE_FOREGROUND'])

        # Line numbering area
        self.linenumberingarea = tk.Text(root, font=(self.font_family, self.font_size), borderwidth=0, background=CONFIG['DEFAULT_LINENUMBERINGAREA_BACKGROUND_COLOR'], foreground=CONFIG['DEFAULT_LINENUMBERINGAREA_FOREGROUND_COLOR'], width=1, padx=5)
        self.linenumberingarea.grid(row=0, column=0, sticky='ns')
        self.linenumberingarea.insert('1.0', '1')
        self.linenumberingarea.config(state='disabled')

        self.linenumberingarea.tag_configure('line', justify='right')
        self.linenumberingarea.tag_add('line', '1.0', 'end')

        root.grid_columnconfigure(0, weight=0)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self.navbar = Navbar(self)
        self.shortcut_binding()

        self.textarea.config(yscrollcommand=self.navbar.file_menu.file_helper.yscroll)
        self.scrollbar_h.config(command=self.textarea.xview)
        self.textarea.vbar.config(command=self.navbar.file_menu.file_helper.yview)

    def shortcut_binding(self):
        self.textarea.bind('<KeyRelease>', self.navbar.file_menu.file_helper.text_modified)
        self.textarea.bind('<MouseWheel>', self.navbar.file_menu.file_helper.on_mousewheel)
        self.textarea.bind('<Shift-MouseWheel>', self.navbar.file_menu.file_helper.scroll_horizontaly)
        
        self.textarea.bind('<Control-=>', self.navbar.theme_menu.theme_sub_menu.theme_sub_helper.increase_fontsize)
        self.textarea.bind('<Control-minus>', self.navbar.theme_menu.theme_sub_menu.theme_sub_helper.decrease_fontsize)
        self.textarea.bind('<Control-0>', self.navbar.theme_menu.theme_sub_menu.theme_sub_helper.reset_fontsize)

        self.textarea.bind('<Control-n>', lambda e: self.navbar.file_menu.file_helper.new_file())
        self.textarea.bind('<Control-o>', lambda e: self.navbar.file_menu.file_helper.open_file())
        self.textarea.bind('<Control-s>', lambda e: self.navbar.file_menu.file_helper.save_file())
        self.textarea.bind('<Control-Shift-s>', lambda e: self.navbar.file_menu.file_helper.save_as_file())

        self.textarea.bind('<Button-1>', self.navbar.edit_menu.edit_helper.on_mouse_click)
        self.textarea.bind('<Control-r>', lambda e: self.navbar.edit_menu.edit_helper.replace_window())
        self.textarea.bind('<Control-f>', lambda e: self.navbar.edit_menu.edit_helper.find_window())


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
