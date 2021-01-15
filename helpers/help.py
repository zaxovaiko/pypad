from tkinter import messagebox

class HelpHelper:
    @staticmethod
    def show_version():
        messagebox.showinfo('Version', 'v0.0.1')

    @staticmethod
    def show_about():
        messagebox.showinfo('About', 'PyPad\nProject for Języki Skryptowe\nBased on Tkinter')