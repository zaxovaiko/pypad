import tkinter as tk
from helpers.file import FileHelper


class FileMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.navbar = navbar
        self.parent = navbar.parent

        self.file_helper = FileHelper(navbar=navbar, parent=self.parent)

        self.add_command(label="New", accelerator='Ctrl+N', command=self.file_helper.new_file)
        self.add_command(label="Open", accelerator='Ctrl+O', command=self.file_helper.open_file)
        self.add_command(label="Close", state='disabled', command=self.file_helper.close_file)
        self.add_command(label="Save ", accelerator='Ctrl+S', command=self.file_helper.save_file)
        self.add_command(label="Save As", accelerator='Ctrl+Shift+S', command=self.file_helper.save_as_file)
        self.add_separator()
        self.add_command(label="Exit", command=self.file_helper.exit_from_app)
