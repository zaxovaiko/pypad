import tkinter as tk
from tkinter import font
from state import State


class FrameFont(tk.Toplevel):
    def __init__(self, root=None, helper=None):
        super().__init__(root)

        self.root = root
        self.helper = helper

        self.title('Font')
        self.resizable(0, 0)

        font_size_v = tk.StringVar()

        self.fonts_list_label = tk.Label(self, text=f'Font family: {State.font_family}')
        self.fonts_list_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky='w')

        self.fonts_list_select = tk.Listbox(self)
        self.fonts_list_select.grid(row=1, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')

        self.fonts_list_select.bind('<<ListboxSelect>>', self.helper.on_listbox_select)
        for i, fm in enumerate(font.families()):
            self.fonts_list_select.insert(i, fm)

        self.font_size_label = tk.Label(self, text=f'Font size: {State.font_size}pt')
        self.font_size_label.grid(row=2, column=0, padx=10, sticky='w')

        self.font_size_entry = tk.Entry(self, text='Choose text color', textvariable=font_size_v)
        self.font_size_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')

        self.set_font_btn = tk.Button(self, text='Set font', command=self.helper.set_font)
        self.set_font_btn.grid(row=4, column=1, pady=(0, 10), sticky='we')

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.destroy())
        self.cancel_btn.grid(row=4, column=2, padx=(5, 10), pady=(0, 10), sticky='we')

    def run(self):
        self.mainloop()
