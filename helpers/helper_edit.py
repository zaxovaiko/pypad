import re
from config import CONFIG
from utils import get_cursor_position
from tkinter import messagebox
from frames.frame_replace import FrameReplace
from frames.frame_find import FrameFind
from state import State
from datetime import datetime


class EditHelper:
    def __init__(self, navbar=None, parent=None):
        self.navbar = navbar
        self.parent = parent

        self.parent.textarea.bind('<Button-1>', self.on_mouse_click)
        self.parent.textarea.bind('<Control-r>', lambda e: self.show_replace_window())
        self.parent.textarea.bind('<Control-f>', lambda e: self.show_find_window())
        self.parent.textarea.bind('<F5>', lambda e: self.insert_time_and_date())

    def show_replace_window(self):
        self.frame_replace = FrameReplace(root=self.parent.root, helper=self)

    def show_find_window(self):
        self.frame_find = FrameFind(root=self.parent.root, helper=self)

    def insert_time_and_date(self):
        self.parent.textarea.insert('insert', datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

    def find_replace(self, replace_all=False):
        occurrences = re.findall(self.frame_replace.find_v.get(), self.parent.textarea.get('1.0', 'end'), flags=re.M) \
            if self.frame_replace.c_reg_v.get() == 1 \
            else self.parent.textarea.get('1.0', 'end').count(self.frame_replace.find_v.get())

        if self.frame_replace.find_v.get() == '':
            return messagebox.showerror(title=CONFIG['REPLACE_WINDOW_TITLE'], message='String can not be empty')

        if occurrences == 0 or occurrences == []:
            return messagebox.showerror(title=CONFIG['REPLACE_WINDOW_TITLE'], message='No match was found')

        repl = re.sub(self.frame_replace.find_v.get(), self.frame_replace.repl_v.get(), self.parent.textarea.get('1.0', 'end'), len(occurrences) if replace_all else 1, flags=re.M) \
            if self.frame_replace.c_reg_v.get() == 1 \
            else self.parent.textarea.get('1.0', 'end').replace(self.frame_replace.find_v.get(), self.frame_replace.repl_v.get(), occurrences if replace_all else 1)

        self.parent.textarea.delete('1.0', 'end')
        self.parent.textarea.insert('1.0', repl)

        messagebox.showinfo(title=CONFIG['REPLACE_WINDOW_TITLE'], message=f'{(occurrences if type(occurrences) != list else len(occurrences)) if replace_all else 1} matches were replaced')

    def on_mouse_click(self, e):
        self.parent.textarea.tag_remove('highlightline', get_cursor_position(*State.find_position[0]), get_cursor_position(*State.find_position[1]))

    def find(self):
        if self.frame_find.find_v.get() == '':
            return messagebox.showerror(title='Find', message='String can not be empty')

        self.parent.textarea.tag_remove('highlightline', get_cursor_position(*State.find_position[0]), get_cursor_position(*State.find_position[1]))

        text = self.parent.textarea.get('1.0', 'end-1c')
        word_to_find = self.frame_find.find_v.get()

        # Reset if we are looking for new word
        if State.find_word != word_to_find:
            State.find_word_regex_counter = 0
            State.find_position = CONFIG['DEFAULT_START_POSITION']

        for counter, word in enumerate(re.findall(word_to_find, text) if self.frame_find.c_reg_v.get() == 1 else [word_to_find]):
            if self.frame_find.c_reg_v.get() == 1 and counter < State.find_word_regex_counter:
                continue

            for i, ln in enumerate(text.split('\n')):
                if word in ln:
                    line = i + 1
                    adn = 0 if State.find_position[1][1] < 0 else State.find_position[1][1]

                    try:
                        # TODO: Check last word in sequence
                        if word not in ln[adn:]:
                            State.find_position = ((State.find_position[0][0] + 1, 0), (State.find_position[1][0] + 1, -1))
                            adn = 0 if State.find_position[1][1] < 0 else State.find_position[1][1]

                        column = ln[adn:].index(word) + adn
                        if (line == State.find_position[0][0] and column >= State.find_position[1][1]) or (line > State.find_position[0][0]):
                            State.find_word_regex_counter = counter + 1
                            State.find_position = ((line, column), (line, column + len(word)))
                            State.find_word = word_to_find

                            self.parent.textarea.tag_add('highlightline', get_cursor_position(*State.find_position[0]), get_cursor_position(*State.find_position[1]))
                            self.parent.textarea.see(get_cursor_position(*State.find_position[0]))
                            self.parent.linenumberingarea.see(f'{line}.0')
                            return None
                    except:
                        State.find_position = ((State.find_position[0][0] + 1, 0), (State.find_position[1][0] + 1, -1))

        State.find_word_regex_counter = 0
        State.find_word = word_to_find
        State.find_position = CONFIG['DEFAULT_START_POSITION']
        messagebox.showerror(title=CONFIG['FIND_WINDOW_TITLE'], message='Substring was not found')
