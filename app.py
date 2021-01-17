import tkinter as tk
from frames.frame_textarea import FrameTextarea


def main():
    root = tk.Tk()
    app = FrameTextarea(root)
    app.mainloop()


if __name__ == '__main__':
    main()
