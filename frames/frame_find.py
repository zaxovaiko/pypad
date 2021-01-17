import tkinter as tk
from config import CONFIG


class FrameFind(tk.Toplevel):
    def __init__(self, root=None, helper=None):
        super().__init__(root)

        self.root = root
        self.helper = helper

        self.title(CONFIG['FIND_WINDOW_TITLE'])
        self.resizable(0, 0)
        self.focus_force()

        self.find_v = tk.StringVar()
        self.c_reg_v = tk.IntVar()

        self.find_label = tk.Label(self, text='Find what:')
        self.find_label.grid(row=0, column=0, sticky='e', padx=10, pady=(10, 0))

        self.find_entry = tk.Entry(self, textvariable=self.find_v)
        self.find_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=(10, 0))

        self.repl_btn = tk.Button(self, text='Find', command=self.helper.find)
        self.repl_btn.grid(row=0, column=2, sticky='nsew', padx=10, pady=(10, 0))

        self.checkbox_regex = tk.Checkbutton(self, text='Match as regex', variable=self.c_reg_v, onvalue=1, offvalue=0)
        self.checkbox_regex.grid(row=2, column=1, sticky='e', padx=10, pady=10)

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.destroy())
        self.cancel_btn.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)

        self.grid_columnconfigure(1, weight=1)
    
    def run(self):
        self.mainloop()
