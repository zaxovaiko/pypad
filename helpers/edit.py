import re
import tkinter as tk
from utils import Utils
from config import CONFIG
from tkinter import messagebox


class EditHelper:
    def __init__(self, navbar=None, parent=None):
        self.navbar = navbar
        self.parent = parent

        self.background_color = CONFIG['DEFAULT_BACKGROUND_COLOR']
        self.foreground_color = CONFIG['DEFAULT_FOREGROUND_COLOR']
        self.linenumering_color = CONFIG['DEFAULT_LINENUMBERINGAREA_BACKGROUND_COLOR']

        self.font_size = self.parent.font_size
        self.font_family = self.parent.font_family

        self.prev_occurence = 0
        self.find_position = ((0, 0), (0, 0))

    def on_mouse_click(self, e):
        self.parent.textarea.tag_remove('highlightline', Utils.get_cursor_position(*self.find_position[0]), Utils.get_cursor_position(*self.find_position[1]))

    def find_replace(self, replaceAll=False):
        # Count occurences depending on checkbox value
        try:
            if self.c_reg_v.get() == 1:
                occurences = re.findall(self.find_v.get(), self.parent.textarea.get('1.0', 'end'), flags=re.M)
            else:
                occurences = self.parent.textarea.get('1.0', 'end').count(self.find_v.get())
        except:
            return messagebox.showerror(title=CONFIG['REPLACE_WINDOW_TITLE'], message='Wrong pattern')

        if self.find_v.get() == '':
            return messagebox.showerror(title=CONFIG['REPLACE_WINDOW_TITLE'], message='String can not be empty')

        if occurences == 0:
            return messagebox.showerror(title=CONFIG['REPLACE_WINDOW_TITLE'], message='No match was found')

        if self.c_reg_v.get() == 1:
            if replaceAll:
                repl = re.sub(self.find_v.get(), self.repl_v.get(), self.parent.textarea.get('1.0', 'end'), flags=re.M)
            else:
                repl = re.sub(self.find_v.get(), self.repl_v.get(), self.parent.textarea.get('1.0', 'end'), 1, flags=re.M)
        else:
            if replaceAll:
                repl = self.parent.textarea.get('1.0', 'end').replace(self.find_v.get(), self.repl_v.get())
            else:
                repl = self.parent.textarea.get('1.0', 'end').replace(self.find_v.get(), self.repl_v.get(), 1)

        self.parent.textarea.delete('1.0', 'end')
        self.parent.textarea.insert('1.0', repl)

        # FIXME: fix count of matches
        messagebox.showinfo(title=CONFIG['REPLACE_WINDOW_TITLE'], message=f'{occurences if type(occurences) != list else len(occurences) if replaceAll else 1} matches were replaced')

    def replace_window(self):
        t = tk.Toplevel(self.parent.root)
        t.title(CONFIG['REPLACE_WINDOW_TITLE'])
        t.resizable(0, 0)
        t.focus_force()

        self.find_v = tk.StringVar()
        self.repl_v = tk.StringVar()
        self.c_reg_v = tk.IntVar()

        # first row
        self.find_label = tk.Label(t, text='Find what:')
        self.find_label.grid(row=0, column=0, sticky='e',padx=10, pady=(10, 0))

        self.find_enty = tk.Entry(t, textvariable=self.find_v)
        self.find_enty.grid(row=0, column=1, sticky='ew',padx=10, pady=(10, 0))

        self.repl_btn = tk.Button(t, text='Replace', command=self.find_replace)
        self.repl_btn.grid(row=0, column=2, sticky='nsew',padx=10, pady=(10, 0))

        # second row
        self.repl_label = tk.Label(t, text='Replace with:')
        self.repl_label.grid(row=1, column=0, sticky='e', padx=10, pady=10)

        self.repl_entry = tk.Entry(t, textvariable=self.repl_v)
        self.repl_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)

        self.repl_all_btn = tk.Button(t, text='Replace all', command=lambda: self.find_replace(replaceAll=True))
        self.repl_all_btn.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)

        # third row
        self.checkbox_regex = tk.Checkbutton(t, text='Match as regex', variable=self.c_reg_v, onvalue=1, offvalue=0)
        self.checkbox_regex.grid(row=2, column=1, sticky='e', padx=10, pady=(0, 10))

        self.cancel_btn = tk.Button(t, text='Cancel', command=lambda: t.destroy())
        self.cancel_btn.grid(row=2, column=2,sticky='nsew', padx=10, pady=(0, 10))

        t.grid_columnconfigure(1, weight=1)
        t.mainloop()

    def find(self):
        if self.c_reg_v.get() == 1:
            pass
        else:
            self.parent.textarea.tag_remove('highlightline', Utils.get_cursor_position(*self.find_position[0]), Utils.get_cursor_position(*self.find_position[1]))

            text = self.parent.textarea.get('1.0', 'end-1c')
            was_found = False

            for i, ln in enumerate(text.split('\n')):
                if (i + 1) > self.find_position[0][0] and self.find_v.get() in ln:
                    line = i + 1
                    column = ln.index(self.find_v.get())
                    was_found = True
                    break

            if not was_found:
                self.find_position = ((0, 0), (0, 0))
                return messagebox.showerror(title=CONFIG['FIND_WINDOW_TITLE'], message='Substring was not found')

            self.find_position = ((line, column), (line, column + len(self.find_v.get())))
            self.parent.textarea.tag_add('highlightline', Utils.get_cursor_position(*self.find_position[0]), Utils.get_cursor_position(*self.find_position[1]))
            
            self.parent.textarea.see(Utils.get_cursor_position(*self.find_position[0]))
            self.parent.linenumberingarea.see(f'{line}.0')
        
    def find_window(self):
        t = tk.Toplevel(self.parent.root)
        t.title(CONFIG['FIND_WINDOW_TITLE'])
        t.resizable(0, 0)
        t.focus_force()

        self.find_v = tk.StringVar()
        self.c_reg_v = tk.IntVar()

        # first row
        self.find_label = tk.Label(t, text='Find what:')
        self.find_label.grid(row=0, column=0, sticky='e', padx=10, pady=(10, 0))

        self.find_enty = tk.Entry(t, textvariable=self.find_v)
        self.find_enty.grid(row=0, column=1, sticky='ew', padx=10, pady=(10, 0))

        self.repl_btn = tk.Button(t, text='Find', command=self.find)
        self.repl_btn.grid(row=0, column=2, sticky='nsew', padx=10, pady=(10, 0))

        # second row
        self.checkbox_regex = tk.Checkbutton(t, text='Match as regex', variable=self.c_reg_v, onvalue=1, offvalue=0)
        self.checkbox_regex.grid(row=2, column=1, sticky='e', padx=10, pady=10)

        self.cancel_btn = tk.Button(t, text='Cancel', command=lambda: t.destroy())
        self.cancel_btn.grid(row=2, column=2,sticky='nsew', padx=10, pady=10)

        t.grid_columnconfigure(1, weight=1)
        t.mainloop()