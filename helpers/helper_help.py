from tkinter import messagebox
from frames.frame_help import FrameHelp


class HelpHelper:
    @staticmethod
    def show_version():
        messagebox.showinfo('Version', 'v0.0.1')

    @staticmethod
    def show_about(root):
        FrameHelp(root)
