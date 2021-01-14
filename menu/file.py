import tkinter as tk


class FileMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.navbar = navbar
        self.add_command(label="New", accelerator='Ctrl+N', command=self.navbar.parent.new_file)
        self.add_command(label="Open", accelerator='Ctrl+O', command=self.navbar.parent.open_file)
        self.add_command(label="Close", state='disabled', command=self.navbar.parent.close_file)
        self.add_command(label="Save ", accelerator='Ctrl+S', command=self.navbar.parent.save_file)
        self.add_command(label="Save As", accelerator='Ctrl+Shift+S', command=self.navbar.parent.save_as_file)
        self.add_separator()
        self.add_command(label="Exit", command=self.navbar.parent.exit_from_app)
