import os
import tkinter as tk
from config import CONFIG
from utils import Utils
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog


class FileHelper:
    def __init__(self, navbar=None, parent=None):
        self.navbar = navbar
        self.parent = parent

        self.filename = CONFIG['DEFAULT_NAME']
        self.font_family = CONFIG['DEFAULT_FONT_FAMILY']
        self.font_size = CONFIG['DEFAULT_FONT_SIZE']
        
        self.is_modified = False
        self.is_saved = False

    def on_mousewheel(self, e):
        self.parent.textarea.yview_scroll(int(-1 * (e.delta / 10)), "units")
        self.parent.linenumberingarea.yview_scroll(int(-1 * (e.delta / 10)), "units")

    def yscroll(self, *args):
        self.parent.textarea.vbar.set(*args)

    def yview(self, *args):
        self.parent.textarea.yview(*args)
        self.parent.linenumberingarea.yview(*args)

    def text_modified(self, e=None):
        self.is_modified = True
        self._update_title(f'*{Utils.get_filename_from_path(self.filename)}')
        self.navbar.file_menu.entryconfig(2, state='normal')

        lines = self.parent.textarea.get("1.0", 'end').count('\n')

        self.parent.linenumberingarea.config(state='normal')
        self.parent.linenumberingarea.delete('1.0', 'end')
        self.parent.linenumberingarea.insert("1.0", '\n'.join([str(x + 1) for x in range(lines)]), 'line')
        self.parent.linenumberingarea.config(state='disabled', width=int(len(str(lines))))
        self.parent.linenumberingarea.yview_moveto(self.parent.textarea.vbar.get()[0])

    def scroll_horizontaly(self, e):
        self.parent.textarea.xview_scroll(int(e.delta / 120), "units")

    def new_file(self):
        self.close_file()

    def exit_from_app(self):
        self.close_file()
        self.parent.root.destroy()

    def close_file(self):
        if self.is_modified:
            ans = messagebox.askyesnocancel(title='Save changes', message='Save current changes?')
            if ans:
                self.save_file()
            elif ans == False:
                self._clear_textarea()
        else:
            self._clear_textarea()

    def open_file(self):
        ans = filedialog.askopenfilename(parent=self.parent.root)
        if ans:
            self.filename = ans
            self.parent.textarea.delete('1.0', 'end')
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    self.parent.textarea.insert('1.0', f.read())
                    self.text_modified()
                    self._update_title(Utils.get_filename_from_path(self.filename))
                    self.is_modified = False
                    self.parent.textarea.see('1.0')
                    self.parent.linenumberingarea.see('1.0')
                except:
                    messagebox.showerror(title='Wrong file', message='You can not open this file')

    def save_file(self):
        if not self.is_saved:
            self.is_saved = True
            return self.save_as_file()
        self._write_to_file()

    def save_as_file(self):
        ans = filedialog.asksaveasfilename(parent=self.parent, defaultextension='.txt', filetypes=CONFIG['DEFAULT_FILETYPES'], initialfile=self.filename)
        if ans:
            self.filename = ans
            self._write_to_file()

    def _write_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.parent.textarea.get('1.0', 'end')[:-1])
            f.close()
            self._update_title(Utils.get_filename_from_path(self.filename))
            self.is_modified = False

    def _update_title(self, filename):
        self.parent.root.title(f'{filename} - {CONFIG["APP_NAME"]}')

    def _clear_textarea(self):
        self.parent.textarea.delete('1.0', 'end')
        self.is_modified = False
        self.navbar.file_menu.entryconfig(2, state='disabled')
        self.filename = CONFIG['DEFAULT_NAME']
        self._update_title(CONFIG['DEFAULT_NAME'])
    