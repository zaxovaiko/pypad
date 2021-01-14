import tkinter as tk
from menu.help import HelpMenu
from menu.file import FileMenu
from menu.edit import EditMenu
from menu.theme import ThemeMenu
from menu.security import SecurityMenu


class Navbar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root)

        self.navbar = tk.Menu(parent.root)
        self.parent = parent
        self.parent.root.config(menu=self.navbar)

        self.file_menu = FileMenu(self)
        self.edit_menu = EditMenu(self)
        self.security_menu = SecurityMenu(self)
        self.theme_menu = ThemeMenu(self)
        self.help_menu = HelpMenu(self)

        self.navbar.add_cascade(label='File', menu=self.file_menu)
        self.navbar.add_cascade(label='Edit', menu=self.edit_menu)
        self.navbar.add_cascade(label='Security', menu=self.security_menu)
        self.navbar.add_cascade(label='Theme', menu=self.theme_menu)
        self.navbar.add_cascade(label='Help', menu=self.help_menu)
        