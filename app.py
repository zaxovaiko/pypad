import os
import tkinter as tk
from navbar import Navbar
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog


class App(tk.Frame):
    APP_NAME = 'PyPad'
    FONT_SIZE = 13
    FONT_FAMILY = 'Consolas'
    DEFAULT_FILENAME = 'Untitled'
    DEFAULT_TITLE = f'{DEFAULT_FILENAME} - {APP_NAME}'
    FILETYPES = [("Text file", '*.txt'), ('All files', '*.*')]

    def __init__(self, root):
        self.width = 600
        self.height = 400
        self.min_width = 400
        self.min_height = 300

        self.filename = self.DEFAULT_FILENAME
        self.font_family = self.FONT_FAMILY
        self.font_size = self.FONT_SIZE

        self.is_modified = False
        self.is_saved = False

        super().__init__(root)
        self.root = root

        root.title(self.DEFAULT_TITLE)
        root.geometry(f'{self.width}x{self.height}')
        root.minsize(width=self.min_width, height=self.min_height)

        # Main textarea
        self.textarea = scrolledtext.ScrolledText(root, font=(self.font_family, self.font_size), borderwidth=0, highlightthickness=0, wrap='none')
        self.textarea.grid(row=0, column=1, sticky='nsew')

        self.textarea.config(yscrollcommand=self.yscroll)
        self.textarea.vbar.config(command=self.yview)

        # Line numbering area
        self.linenumberingarea = tk.Text(root, font=(self.font_family, self.font_size), borderwidth=0, background='#f0f0f0', foreground='#888', width=1, padx=5)
        self.linenumberingarea.grid(row=0, column=0, sticky='ns')
        self.linenumberingarea.insert('1.0', '1')
        self.linenumberingarea.config(state='disabled')

        self.linenumberingarea.tag_configure('line', justify='right')
        self.linenumberingarea.tag_add('line', '1.0', 'end')

        self.navbar = Navbar(self)
        self.shortcut_binding()

        root.grid_columnconfigure(0, weight=0)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

    def on_mousewheel(self, e):
        self.textarea.yview_scroll(int(-1 * (e.delta / 120)), "units")
        self.linenumberingarea.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def yscroll(self, *args):
        self.textarea.vbar.set(*args)

    def yview(self, *args):
        self.textarea.yview(*args)
        self.linenumberingarea.yview(*args)

    def text_modified(self, e=None):
        self.is_modified = True
        self.__update_title(f'*{self.__get_filename_from_path(self.filename)}')
        self.navbar.file_menu.entryconfig(2, state='normal')

        lines = self.textarea.get("1.0", 'end').count('\n')

        self.linenumberingarea.config(state='normal')
        self.linenumberingarea.delete('1.0', 'end')
        self.linenumberingarea.insert("1.0", '\n'.join([str(x + 1) for x in range(lines)]), 'line')
        self.linenumberingarea.config(state='disabled', width=int(len(str(lines))))
        self.linenumberingarea.yview_moveto(self.textarea.vbar.get()[0])

    def shortcut_binding(self):
        self.root.bind("<Control-=>", self.increase_fontsize)
        self.root.bind("<Control-minus>", self.decrease_fontsize)
        self.root.bind("<Control-0>", self.reset_fontsize)

        self.textarea.bind('<KeyRelease>', self.text_modified)
        self.textarea.bind('<MouseWheel>', self.on_mousewheel)

    def __update_title(self, filename):
        self.root.title(f'{filename} - {self.APP_NAME}')

    def __update_font(self):
        self.textarea.config(font=(self.font_family, self.font_size))
        self.linenumberingarea.config(font=(self.font_family, self.font_size))

    def __get_filename_from_path(self, path):
        return path.split('/')[-1]

    def increase_fontsize(self, e):
        self.font_size += 1
        self.__update_font()

    def decrease_fontsize(self, e):
        self.font_size -= 1
        self.__update_font()

    def reset_fontsize(self, e):
        self.font_size = self.FONT_SIZE
        self.__update_font()

    def new_file(self):
        self.close_file()

    def __clear_textarea(self):
        self.textarea.delete('1.0', 'end')
        self.is_modified = False
        self.navbar.file_menu.entryconfig(2, state='disabled')
        self.filename = self.DEFAULT_FILENAME
        self.__update_title(self.filename)

    def exit_from_app(self):
        self.close_file()
        self.root.destroy()

    def close_file(self):
        if self.is_modified:
            ans = messagebox.askyesnocancel(title='Save changes', message='Save current changes?')
            if ans:
                self.save_file()
            elif ans == False:
                self.__clear_textarea()
        else:
            self.__clear_textarea()

    def open_file(self):
        # TODO: Scroll cursor to the beggining of the file
        ans = filedialog.askopenfilename(parent=self.root)
        if ans:
            self.filename = ans
            self.textarea.delete('1.0', 'end')
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.textarea.insert('1.0', f.read())
                self.text_modified()
                self.__update_title(self.__get_filename_from_path(self.filename))
                self.is_modified = False

    def save_file(self):
        if not self.is_saved:
            self.is_saved = True
            return self.save_as_file()
        self.__write_to_file()

    def __write_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.textarea.get('1.0', 'end')[:-1])
            f.close()
            self.__update_title(self.__get_filename_from_path(self.filename))
            self.is_modified = False

    def save_as_file(self):
        ans = filedialog.asksaveasfilename(parent=root, defaultextension='.txt', filetypes=self.FILETYPES, initialfile=self.filename)
        if ans:
            self.filename = ans
            self.__write_to_file()

    def show_version(self):
        messagebox.showinfo('Version', 'v0.0.1')

    def show_about(self):
        messagebox.showinfo('About', 'PyPad\nProject for Języki Skryptowe\nBased on Tkinter')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
