import tkinter as tk


class EditMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.navbar = navbar
        self.add_command(label="Cut", accelerator='Ctrl+X', command=self.navbar.parent.cut_event)
        self.add_command(label="Copy", accelerator='Ctrl+C', command=self.navbar.parent.copy_event)
        self.add_command(label="Paste", accelerator='Ctrl+V', command=self.navbar.parent.paste_event)
        self.add_separator()
        self.add_command(label="Replace", accelerator='Ctrl+R', command=self.navbar.parent.replace_window)
        self.add_command(label="Find", accelerator='Ctrl+F', command=self.navbar.parent.find_window)

