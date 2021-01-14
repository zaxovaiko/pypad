import tkinter as tk
from tkinter import messagebox


class HelpMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.add_command(label="About", command=self.show_about)
        self.add_command(label="Version", command=self.show_version)

    def show_version(self):
        messagebox.showinfo('Version', 'v0.0.1')

    def show_about(self):
        messagebox.showinfo('About', 'PyPad\nProject for Języki Skryptowe\nBased on Tkinter')
