import pickle
import os.path
import tkinter as tk
from config import CONFIG
from state import State
from frames.frame_textarea import FrameTextarea


def main():
    if os.path.exists(CONFIG['PREFERENCES_FILENAME']) and os.path.isfile(CONFIG['PREFERENCES_FILENAME']):
        with open(CONFIG['PREFERENCES_FILENAME'], 'rb') as f:
            state = pickle.load(f)
            for k, v in state.items():
                setattr(State, k, v)

    root = tk.Tk()
    root.iconbitmap(r'icon.ico')
    app = FrameTextarea(root)
    app.mainloop()


if __name__ == '__main__':
    main()
