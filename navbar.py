import tkinter as tk
from tkinter import messagebox


class Navbar(tk.Frame):
    def __init__(self, parent):
        navbar = tk.Menu(parent.root)
        parent.root.config(menu=navbar)

        file_menu = tk.Menu(navbar, tearoff=0)
        file_menu.add_command(label="New", accelerator='Ctrl+N')
        file_menu.add_command(label="Open", accelerator='Ctrl+O', command=parent.open_file)
        file_menu.add_command(label="Close", state='disabled', command=parent.close_file)
        file_menu.add_command(label="Save ", accelerator='Ctrl+S', command=parent.save_file)
        file_menu.add_command(label="Save As", accelerator='Ctrl+Shift+S')
        file_menu.add_separator()
        file_menu.add_command(label="Exit")

        edit_menu = tk.Menu(navbar, tearoff=0)
        edit_menu.add_command(label="Cut", accelerator='Ctrl+X')
        edit_menu.add_command(label="Copy", accelerator='Ctrl+C')
        edit_menu.add_command(label="Paste", accelerator='Ctrl+V')
        edit_menu.add_separator()
        edit_menu.add_command(label="Replace", accelerator='Ctrl+R')
        edit_menu.add_command(label="Find", accelerator='Ctrl+F')

        help_menu = tk.Menu(navbar, tearoff=0)
        help_menu.add_command(label="About", command=parent.show_about)
        help_menu.add_command(label="Version", command=parent.show_version)

        navbar.add_cascade(label='File', menu=file_menu)
        navbar.add_cascade(label='Edit', menu=edit_menu)
        navbar.add_cascade(label='Help', menu=help_menu)

        self.file_menu = file_menu
        self.edit_menu = edit_menu
        self.help_menu = help_menu
