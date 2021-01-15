import tkinter as tk
from menu.submenu.theme import ThemeSubMenu
from helpers.theme import ThemeHelper


class ThemeMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.navbar = navbar
        self.parent = navbar.parent

        self.theme_helper = ThemeHelper(navbar=navbar, parent=self.parent)
        self.theme_sub_menu = ThemeSubMenu(self)

        self.add_command(label="Color", command=self.theme_helper.show_color_window)
        self.add_command(label="Font", command=self.theme_helper.show_font_window)        
        self.add_cascade(label='Zoom', menu=self.theme_sub_menu)
        