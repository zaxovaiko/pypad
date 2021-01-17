import re
from config import CONFIG
from utils import get_cursor_position
from tkinter import messagebox
from frames.frame_replace import FrameReplace
from frames.frame_find import FrameFind
from state import State


class EditHelper:
    def __init__(self, navbar=None, parent=None):
        self.navbar = navbar
        self.parent = parent

        self.parent.textarea.bind('<Button-1>', self.on_mouse_click)
        self.parent.textarea.bind('<Control-r>', lambda e: self.show_replace_window())
        self.parent.textarea.bind('<Control-f>', lambda e: self.show_find_window())

    def show_replace_window(self):
        self.frame_replace = FrameReplace(root=self.parent.root, helper=self)
        self.frame_replace.run()

    def show_find_window(self):
        self.frame_find = FrameFind(root=self.parent.root, helper=self)
        self.frame_find.run()

    def find_replace(self, replace_all=False):
        # Count occurrences depending on checkbox value
        try:
            if self.frame_replace.c_reg_v.get() == 1:
                occurrences = re.findall(self.frame_replace.find_v.get(), self.parent.textarea.get('1.0', 'end'), flags=re.M)
            else:
                occurrences = self.parent.textarea.get('1.0', 'end').count(self.frame_replace.find_v.get())
        except:
            return messagebox.showerror(title=CONFIG['REPLACE_WINDOW_TITLE'], message='Wrong pattern')

        if self.frame_replace.find_v.get() == '':
            return messagebox.showerror(title=CONFIG['REPLACE_WINDOW_TITLE'], message='String can not be empty')

        if occurrences == 0:
            return messagebox.showerror(title=CONFIG['REPLACE_WINDOW_TITLE'], message='No match was found')

        if self.frame_replace.c_reg_v.get() == 1:
            if replace_all:
                repl = re.sub(self.frame_replace.find_v.get(), self.frame_replace.repl_v.get(), self.parent.textarea.get('1.0', 'end'), flags=re.M)
            else:
                repl = re.sub(self.frame_replace.find_v.get(), self.frame_replace.repl_v.get(), self.parent.textarea.get('1.0', 'end'), 1, flags=re.M)
        else:
            if replace_all:
                repl = self.parent.textarea.get('1.0', 'end').replace(self.frame_replace.find_v.get(), self.frame_replace.repl_v.get())
            else:
                repl = self.parent.textarea.get('1.0', 'end').replace(self.frame_replace.find_v.get(), self.frame_replace.repl_v.get(), 1)

        self.parent.textarea.delete('1.0', 'end')
        self.parent.textarea.insert('1.0', repl)

        # FIXME: fix count of matches
        messagebox.showinfo(title=CONFIG['REPLACE_WINDOW_TITLE'], message=f'{occurrences if type(occurrences) != list else len(occurrences) if replace_all else 1} matches were replaced')

    def on_mouse_click(self, e):
        self.parent.textarea.tag_remove('highlightline', get_cursor_position(*State.find_position[0]), get_cursor_position(*State.find_position[1]))

    def find(self):
        if self.frame_find.find_v.get() == '':
            return messagebox.showerror(title='Find', message='String can not be empty')

        if self.frame_find.c_reg_v.get() == 1:
            pass  # TODO: Add if regex
        else:
            self.parent.textarea.tag_remove('highlightline', get_cursor_position(*State.find_position[0]), get_cursor_position(*State.find_position[1]))

            text = self.parent.textarea.get('1.0', 'end-1c')
            to_found = self.frame_find.find_v.get()

            for i, ln in enumerate(text.split('\n')):
                if to_found in ln:
                    line = i + 1
                    adn = 0 if State.find_position[1][1] < 0 else State.find_position[1][1]
                    try:
                        column = ln[adn:].index(to_found) + adn
                        if (line == State.find_position[0][0] and column > State.find_position[1][1]) or (line > State.find_position[0][0]):
                            State.find_position = ((line, column), (line, column + len(to_found)))
                            self.parent.textarea.tag_add('highlightline', get_cursor_position(*State.find_position[0]), get_cursor_position(*State.find_position[1]))
                            self.parent.textarea.see(get_cursor_position(*State.find_position[0]))
                            self.parent.linenumberingarea.see(f'{line}.0')
                            return None
                    except:
                        State.find_position = ((State.find_position[0][0] + 1, 0), (State.find_position[1][0] + 1, -1))

        State.find_position = CONFIG['DEFAULT_START_POSITION']
        messagebox.showerror(title=CONFIG['FIND_WINDOW_TITLE'], message='Substring was not found')
