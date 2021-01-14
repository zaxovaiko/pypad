import tkinter as tk


class SecurityMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.add_command(label="Encrypt file")
        self.add_command(label="Descrypt file")