import tkinter as tk
from tkinter import scrolledtext
from config import CONFIG
from state import State
from frames.frame_navbar import FrameNavbar


class FrameTextarea(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        
        self.root = root
        self.root.title(CONFIG['DEFAULT_TITLE'])
        self.root.geometry('%sx%s' % (CONFIG["DEFAULT_WIDTH"], CONFIG["DEFAULT_HEIGHT"]))
        self.root.minsize(width=CONFIG['MIN_APP_WINDOW_WIDTH'], height=CONFIG['MIN_APP_WINDOW_HEIGHT'])

        # Horizontal scrollbar
        self.scrollbar_h = tk.Scrollbar(root, orient='horizontal')
        self.scrollbar_h.grid(row=1, column=1, sticky='ew')

        # Main textarea
        self.textarea = scrolledtext.ScrolledText(root, font=(State.font_family, State.font_size), borderwidth=0, highlightthickness=0, wrap='none', xscrollcommand=self.scrollbar_h.set)
        self.textarea.grid(row=0, column=1, sticky='nsew')
        self.textarea.tag_configure('highlightline', background=CONFIG['DEFAULT_HIGHLIGHTLINE_BACKGROUND'], relief='raised', foreground=CONFIG['DEFAULT_HIGHLIGHTLINE_FOREGROUND'])

        # Line numbering area
        self.linenumberingarea = tk.Text(root, font=(State.font_family, State.font_size), borderwidth=0, background=CONFIG['DEFAULT_LINENUMBERINGAREA_BACKGROUND_COLOR'], foreground=CONFIG['DEFAULT_LINENUMBERINGAREA_FOREGROUND_COLOR'], width=1, padx=5)
        self.linenumberingarea.grid(row=0, column=0, sticky='ns')
        self.linenumberingarea.insert('1.0', '1')
        self.linenumberingarea.config(state='disabled')

        self.linenumberingarea.tag_configure('line', justify='right')
        self.linenumberingarea.tag_add('line', '1.0', 'end')

        root.grid_columnconfigure(0, weight=0)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self.navbar = FrameNavbar(self)
        self.root.navbar = self.navbar

        self.textarea.config(yscrollcommand=self.navbar.file_helper.yscroll)
        self.scrollbar_h.config(command=self.textarea.xview)
        self.textarea.vbar.config(command=self.navbar.file_helper.yview)
