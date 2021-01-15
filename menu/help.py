import tkinter as tk
from helpers.help import HelpHelper


class HelpMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.add_command(label="About", command=HelpHelper.show_about)
        self.add_command(label="Version", command=HelpHelper.show_version)
