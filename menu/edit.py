import tkinter as tk
from helpers.edit import EditHelper


class EditMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.navbar = navbar
        self.parent = navbar.parent

        self.edit_helper = EditHelper(navbar=navbar, parent=self.parent)

        self.add_command(label="Cut", accelerator='Ctrl+X', command=lambda: self.parent.textarea.event_generate("<<Cut>>"))
        self.add_command(label="Copy", accelerator='Ctrl+C', command=lambda: self.parent.textarea.event_generate("<<Copy>>"))
        self.add_command(label="Paste", accelerator='Ctrl+V', command=lambda: self.parent.textarea.event_generate("<<Paste>>"))
        self.add_separator()
        self.add_command(label="Replace", accelerator='Ctrl+R', command=self.edit_helper.replace_window)
        self.add_command(label="Find", accelerator='Ctrl+F', command=self.edit_helper.find_window)
