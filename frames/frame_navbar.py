import tkinter as tk
from helpers.helper_help import HelpHelper
from helpers.helper_file import FileHelper
from helpers.helper_edit import EditHelper
from helpers.helper_theme import ThemeHelper
from helpers.helper_security import SecurityHelper


class FrameNavbar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root)

        self.menu = tk.Menu(parent.root, tearoff=0)
        self.parent = parent
        self.parent.root.config(menu=self.menu)

        # Initiate helpers -----------------------------
        self.file_helper = FileHelper(navbar=self, parent=parent)
        self.edit_helper = EditHelper(navbar=self, parent=parent)
        self.theme_helper = ThemeHelper(navbar=self, parent=parent)
        self.security_helper = SecurityHelper(navbar=self, parent=parent)

        # File menu ------------------------------------
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="New", accelerator='Ctrl+N', command=self.file_helper.new_file)
        self.file_menu.add_command(label="Open", accelerator='Ctrl+O', command=self.file_helper.open_file)
        self.file_menu.add_command(label="Close", state='disabled', command=self.file_helper.close_file)
        self.file_menu.add_command(label="Save ", accelerator='Ctrl+S', command=self.file_helper.save_file)
        self.file_menu.add_command(label="Save As", accelerator='Ctrl+Shift+S', command=self.file_helper.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.file_helper.exit_from_app)

        # Edit menu ------------------------------------
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label="Cut", accelerator='Ctrl+X', command=lambda: self.parent.textarea.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", accelerator='Ctrl+C', command=lambda: self.parent.textarea.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", accelerator='Ctrl+V', command=lambda: self.parent.textarea.event_generate("<<Paste>>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Replace", accelerator='Ctrl+R', command=self.edit_helper.show_replace_window)
        self.edit_menu.add_command(label="Find", accelerator='Ctrl+F', command=self.edit_helper.show_find_window)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Time/Date", accelerator='F5', command=self.edit_helper.insert_time_and_date)

        # Security menu ------------------------------------
        self.security_menu = tk.Menu(self.menu, tearoff=0)
        self.security_menu.add_command(label="Encrypt file", command=self.security_helper.show_encrypt_window)
        self.security_menu.add_command(label="Decrypt file", command=self.security_helper.show_decrypt_window)

        # Theme menu ------------------------------------
        self.theme_menu = tk.Menu(self.menu, tearoff=0)
        self.theme_sub_menu = tk.Menu(self.theme_menu, tearoff=0)

        self.theme_sub_menu.add_command(label="Zoom in", accelerator='Ctrl+Plus', command=lambda: self.theme_helper.increase_fontsize(scale=5))
        self.theme_sub_menu.add_command(label="Zoom out", accelerator='Ctrl+Minus', command=lambda: self.theme_helper.decrease_fontsize(scale=5))
        self.theme_sub_menu.add_command(label="Zoom reset", accelerator='Ctrl+0', command=lambda: self.theme_helper.reset_fontsize())

        self.theme_menu.add_command(label="Color", command=self.theme_helper.show_color_window)
        self.theme_menu.add_command(label="Font", command=self.theme_helper.show_font_window)        
        self.theme_menu.add_cascade(label='Zoom', menu=self.theme_sub_menu)

        # Help menu ------------------------------------
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=HelpHelper.show_about)
        self.help_menu.add_command(label="Version", command=HelpHelper.show_version)

        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.menu.add_cascade(label='Edit', menu=self.edit_menu)
        self.menu.add_cascade(label='Security', menu=self.security_menu)
        self.menu.add_cascade(label='Theme', menu=self.theme_menu)
        self.menu.add_cascade(label='Help', menu=self.help_menu)
