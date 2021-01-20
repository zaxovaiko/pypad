from config import CONFIG
from utils import get_filename_from_path
from tkinter import messagebox
from tkinter import filedialog
from state import State


class FileHelper:
    def __init__(self, navbar=None, parent=None):
        self.navbar = navbar
        self.parent = parent

        self.parent.textarea.bind('<Control-n>', self.new_file)
        self.parent.textarea.bind('<Control-o>', self.open_file)
        self.parent.textarea.bind('<Control-s>', self.save_file)
        self.parent.textarea.bind('<Control-Shift-s>', self.save_as_file)

        self.parent.textarea.bind('<KeyRelease>', self.text_modified)
        self.parent.textarea.bind('<ButtonRelease>', self.set_cursor_position)
        self.parent.textarea.bind('<MouseWheel>', self.on_mousewheel)
        self.parent.textarea.bind('<Shift-MouseWheel>', self.scroll_horizontaly)

    def on_mousewheel(self, e):
        self.parent.textarea.yview_scroll(int(-1 * (e.delta / 10)), "units")
        self.parent.linenumberingarea.yview_scroll(int(-1 * (e.delta / 10)), "units")

    def yscroll(self, *args):
        self.parent.textarea.vbar.set(*args)

    def set_cursor_position(self, e=None):
        l, c = self.parent.textarea.index('insert').split('.')
        self.parent.logs_area.cursor_label.config(text=f'Ln {l}, Col {c}')

    def yview(self, *args):
        self.parent.textarea.yview(*args)
        self.parent.linenumberingarea.yview(*args)
    
    def text_modified(self, e=None):
        self.set_cursor_position(e)

        State.is_modified = True
        self.update_title(f'*{get_filename_from_path(State.filename)}')
        self.navbar.file_menu.entryconfig(2, state='normal')

        lines = self.parent.textarea.get("1.0", 'end').count('\n')

        self.parent.linenumberingarea.config(state='normal')
        self.parent.linenumberingarea.delete('1.0', 'end')
        self.parent.linenumberingarea.insert("1.0", '\n'.join([str(x + 1) for x in range(lines)]), 'line')
        self.parent.linenumberingarea.config(state='disabled', width=int(len(str(lines))))
        self.parent.linenumberingarea.yview_moveto(self.parent.textarea.vbar.get()[0])
    
    def scroll_horizontaly(self, e):
        self.parent.textarea.xview_scroll(int(e.delta / 120), "units")

    def new_file(self, e=None):
        self.close_file()

    def exit_from_app(self):
        self.close_file()
        self.parent.root.destroy()

    def close_file(self):
        if State.is_modified:
            ans = messagebox.askyesnocancel(title='Save changes', message='Save current changes?')
            if ans:
                self.save_file()
            elif ans == False:
                self.clear_textarea()
        else:
            self.clear_textarea()

    def open_file(self, e=None):
        ans = filedialog.askopenfilename(parent=self.parent.root)
        if ans:
            State.filename = ans
            self.parent.textarea.delete('1.0', 'end')
            with open(State.filename, 'r', encoding='utf-8') as f:
                try:
                    self.parent.textarea.insert('1.0', f.read())
                    self.text_modified()
                    self.update_title(get_filename_from_path(State.filename))
                    State.is_modified = False
                    self.parent.textarea.see('1.0')
                    self.parent.linenumberingarea.see('1.0')
                except:
                    messagebox.showerror(title='Wrong file', message='You can not open this file')

    def save_file(self, e=None):
        if not State.is_saved:
            State.is_saved = True
            return self.save_as_file()
        self.write_to_file()

    def save_as_file(self, e=None):
        ans = filedialog.asksaveasfilename(parent=self.parent, defaultextension='.txt', filetypes=CONFIG['DEFAULT_FILETYPES'], initialfile=get_filename_from_path(State.filename))
        if ans:
            State.filename = ans
            self.write_to_file()

    def write_to_file(self):
        with open(State.filename, 'w', encoding='utf-8') as f:
            f.write(self.parent.textarea.get('1.0', 'end-1c'))
            f.close()
            State.is_modified = False
            self.update_title(get_filename_from_path(State.filename))
    
    def update_title(self, filename):
        self.parent.root.title(f'{filename} - {CONFIG["APP_NAME"]}')

    def clear_textarea(self):
        self.parent.textarea.delete('1.0', 'end')
        self.navbar.file_menu.entryconfig(2, state='disabled')
        State.is_modified = False
        State.filename = CONFIG['DEFAULT_NAME']
        self.update_title(CONFIG['DEFAULT_NAME'])
