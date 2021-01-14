import tkinter as tk
from menu.submenu.theme import ThemeSubMenu


class ThemeMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.add_command(label="Color")
        self.add_command(label="Font")

        self.navbar = navbar
        self.parent = navbar.parent
        self.theme_menu_sub = ThemeSubMenu(self)
        self.add_cascade(label='Zoom', menu=self.theme_menu_sub)
