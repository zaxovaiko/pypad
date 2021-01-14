import os
import re
import tkinter as tk
from navbar import Navbar
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog


class App(tk.Frame):
    # TODO: Add to config file
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
        self.prev_occurence = 0

        super().__init__(root)
        self.root = root

        root.title(self.DEFAULT_TITLE)
        root.geometry(f'{self.width}x{self.height}')
        root.minsize(width=self.min_width, height=self.min_height)

        # Horizontal scrollbar
        self.scrollbar_h = tk.Scrollbar(root, orient='horizontal')
        self.scrollbar_h.grid(row=1, column=1, sticky='ew')

        # Main textarea
        self.textarea = scrolledtext.ScrolledText(root, font=(
            self.font_family, self.font_size), borderwidth=0, highlightthickness=0, wrap='none', xscrollcommand=self.scrollbar_h.set)
        self.textarea.grid(row=0, column=1, sticky='nsew')

        self.textarea.tag_configure(
            'highlightline', background='#0078d7', relief='raised', foreground='white')
        self.textarea.config(yscrollcommand=self.yscroll)
        self.scrollbar_h.config(command=self.textarea.xview)
        self.textarea.vbar.config(command=self.yview)

        # Line numbering area
        self.linenumberingarea = tk.Text(root, font=(
            self.font_family, self.font_size), borderwidth=0, background='#f0f0f0', foreground='#888', width=1, padx=5)
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
        # FIXME: Fix mouse scroll
        self.textarea.yview_scroll(int(-1 * (e.delta / 10)), "units")
        self.linenumberingarea.yview_scroll(int(-1 * (e.delta / 10)), "units")

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
        self.linenumberingarea.insert("1.0", '\n'.join(
            [str(x + 1) for x in range(lines)]), 'line')
        self.linenumberingarea.config(
            state='disabled', width=int(len(str(lines))))
        self.linenumberingarea.yview_moveto(self.textarea.vbar.get()[0])

    def copy_event(self):
        self.textarea.event_generate("<<Copy>>")

    def cut_event(self):
        self.textarea.event_generate("<<Cut>>")

    def paste_event(self):
        self.textarea.event_generate("<<Paste>>")

    def on_mouse_click(self, e):
        if hasattr(self, 'find_position'):
            self.textarea.tag_remove('highlightline', self._get_cursor_position(*self.find_position[0]), self._get_cursor_position(*self.find_position[1]))

    def shortcut_binding(self):
        self.textarea.bind('<KeyRelease>', self.text_modified)
        self.textarea.bind('<MouseWheel>', self.on_mousewheel)
        self.textarea.bind('<Shift-MouseWheel>', self.scroll_horizontaly)
        self.textarea.bind('<Button-1>', self.on_mouse_click)

        self.textarea.bind('<Control-=>', self.increase_fontsize)
        self.textarea.bind('<Control-minus>', self.decrease_fontsize)
        self.textarea.bind('<Control-0>', self.reset_fontsize)
        self.textarea.bind('<Control-n>', lambda e: self.new_file())
        self.textarea.bind('<Control-o>', lambda e: self.open_file())
        self.textarea.bind('<Control-s>', lambda e: self.save_file())
        self.textarea.bind('<Control-r>', lambda e: self.replace_window())
        self.textarea.bind('<Control-f>', lambda e: self.find_window())
        self.textarea.bind('<Control-Shift-s>', lambda e: self.save_as_file())

    def scroll_horizontaly(self, e):
        self.textarea.xview_scroll(int(e.delta / 120), "units")

    def __update_title(self, filename):
        self.root.title(f'{filename} - {self.APP_NAME}')

    def __update_font(self):
        self.textarea.config(font=(self.font_family, self.font_size))
        self.linenumberingarea.config(
            font=(self.font_family, self.font_size))

    def __get_filename_from_path(self, path):
        # FIXME: Add to helpers
        return path.split('/')[-1]

    def increase_fontsize(self, e=None, scale=1):
        self.font_size += scale
        self.__update_font()

    def decrease_fontsize(self, e=None, scale=1):
        self.font_size -= scale
        self.__update_font()

    def reset_fontsize(self, e=None):
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
            ans = messagebox.askyesnocancel(
                title='Save changes', message='Save current changes?')
            if ans:
                self.save_file()
            elif ans == False:
                self.__clear_textarea()
        else:
            self.__clear_textarea()

    def find_replace(self, replaceAll=False):
        TITLE = 'Find and Replace'

        # Count occurences depending on checkbox value
        try:
            if self.c_reg_v.get() == 1:
                occurences = re.findall(
                    self.find_v.get(), self.textarea.get('1.0', 'end'), flags=re.M)
            else:
                occurences = self.textarea.get(
                    '1.0', 'end').count(self.find_v.get())
        except:
            return messagebox.showerror(title=TITLE, message='Wrong pattern')

        if self.find_v.get() == '':
            # TODO: Or disable buttons
            return messagebox.showerror(title=TITLE, message='String can not be empty')

        if occurences == 0:
            return messagebox.showerror(title=TITLE, message='No match was found')

        # TODO: Rewrite in prettier way
        if self.c_reg_v.get() == 1:
            if replaceAll:
                repl = re.sub(self.find_v.get(), self.repl_v.get(),
                              self.textarea.get('1.0', 'end'), flags=re.M)
            else:
                repl = re.sub(self.find_v.get(), self.repl_v.get(),
                              self.textarea.get('1.0', 'end'), 1, flags=re.M)
        else:
            if replaceAll:
                repl = self.textarea.get('1.0', 'end').replace(
                    self.find_v.get(), self.repl_v.get())
            else:
                repl = self.textarea.get('1.0', 'end').replace(
                    self.find_v.get(), self.repl_v.get(), 1)

        self.textarea.delete('1.0', 'end')
        self.textarea.insert('1.0', repl)

        messagebox.showinfo(title=TITLE,
                            message=f'{occurences if type(occurences) != list else len(occurences) if replaceAll else 1} matches were replaced')

    def replace_window(self):
        t = tk.Toplevel(self.root)
        t.title('Replace')
        t.resizable(0, 0)
        t.focus_force()

        self.find_v = tk.StringVar()
        self.repl_v = tk.StringVar()
        self.c_reg_v = tk.IntVar()

        # first row
        self.find_label = tk.Label(t, text='Find what:')
        self.find_label.grid(row=0, column=0, sticky='e',
                             padx=10, pady=(10, 0))

        self.find_enty = tk.Entry(t, textvariable=self.find_v)
        self.find_enty.grid(row=0, column=1, sticky='ew',
                            padx=10, pady=(10, 0))

        self.repl_btn = tk.Button(t, text='Replace', command=self.find_replace)
        self.repl_btn.grid(row=0, column=2, sticky='nsew',
                           padx=10, pady=(10, 0))

        # second row
        self.repl_label = tk.Label(t, text='Replace with:')
        self.repl_label.grid(row=1, column=0, sticky='e', padx=10, pady=10)

        self.repl_entry = tk.Entry(t, textvariable=self.repl_v)
        self.repl_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)

        self.repl_all_btn = tk.Button(
            t, text='Replace all', command=lambda: self.find_replace(replaceAll=True))
        self.repl_all_btn.grid(
            row=1, column=2, sticky='nsew', padx=10, pady=10)

        # third row
        self.checkbox_regex = tk.Checkbutton(
            t, text='Match as regex', variable=self.c_reg_v, onvalue=1, offvalue=0)
        self.checkbox_regex.grid(
            row=2, column=1, sticky='e', padx=10, pady=(0, 10))

        self.cancel_btn = tk.Button(
            t, text='Cancel', command=lambda: t.destroy())
        self.cancel_btn.grid(row=2, column=2,
                             sticky='nsew', padx=10, pady=(0, 10))

        t.grid_columnconfigure(1, weight=1)
        t.mainloop()

    def _get_cursor_position(self, ln, col):
        return f'{ln}.{col}'

    def find(self):
        if self.c_reg_v.get() == 1:
            pass
        else:
            if hasattr(self, 'find_position'):
                self.textarea.tag_remove('highlightline', self._get_cursor_position(*self.find_position[0]), self._get_cursor_position(*self.find_position[1]))

            text = self.textarea.get('1.0', 'end-1c')
            was_found = False

            for i, ln in enumerate(text.split('\n')):
                if (not hasattr(self, 'find_position')) or ((i + 1) > self.find_position[0][0] and self.find_v.get() in ln):
                    line = i + 1
                    column = ln.index(self.find_v.get())
                    was_found = True
                    break

            if not was_found:
                self.find_position = ((0, 0), (0, 0))
                return messagebox.showerror(title='Find', message='Substring was not found')

            self.find_position = ((line, column), (line, column + len(self.find_v.get())))
            self.textarea.tag_add('highlightline', self._get_cursor_position(*self.find_position[0]), self._get_cursor_position(*self.find_position[1]))
            
            self.textarea.see(self._get_cursor_position(*self.find_position[0]))
            self.linenumberingarea.see(f'{line}.0')
        
    def find_window(self):
        t = tk.Toplevel(self.root)
        t.title('Find')
        t.resizable(0, 0)
        t.focus_force()

        self.find_v = tk.StringVar()
        self.c_reg_v = tk.IntVar()

        # first row
        self.find_label = tk.Label(t, text='Find what:')
        self.find_label.grid(row=0, column=0, sticky='e',
                             padx=10, pady=(10, 0))

        self.find_enty = tk.Entry(t, textvariable=self.find_v)
        self.find_enty.grid(row=0, column=1, sticky='ew',
                            padx=10, pady=(10, 0))

        self.repl_btn = tk.Button(t, text='Find', command=self.find)
        self.repl_btn.grid(row=0, column=2, sticky='nsew',
                           padx=10, pady=(10, 0))

        # second row
        self.checkbox_regex = tk.Checkbutton(
            t, text='Match as regex', variable=self.c_reg_v, onvalue=1, offvalue=0)
        self.checkbox_regex.grid(
            row=2, column=1, sticky='e', padx=10, pady=10)

        self.cancel_btn = tk.Button(
            t, text='Cancel', command=lambda: t.destroy())
        self.cancel_btn.grid(row=2, column=2,
                             sticky='nsew', padx=10, pady=10)

        t.grid_columnconfigure(1, weight=1)
        t.mainloop()

    def open_file(self):
        # TODO: Scroll cursor to the beggining of the file
        ans = filedialog.askopenfilename(parent=self.root)
        if ans:
            self.filename = ans
            self.textarea.delete('1.0', 'end')
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    self.textarea.insert('1.0', f.read())
                    self.text_modified()
                    self.__update_title(
                        self.__get_filename_from_path(self.filename))
                    self.is_modified = False
                except:
                    messagebox.showerror(
                        title='Wrong file', message='You can not open this file')

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
        ans = filedialog.asksaveasfilename(
            parent=root, defaultextension='.txt', filetypes=self.FILETYPES, initialfile=self.filename)
        if ans:
            self.filename = ans
            self.__write_to_file()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
