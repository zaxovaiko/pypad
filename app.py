import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from navbar import Navbar


class App(tk.Frame):
    FONT_SIZE = 13
    FONT_FAMILY = 'Consolas'
    DEFAULT_NAME = 'Untitled'

    def __init__(self, root):
        self.width = 600
        self.height = 400
        self.min_width = 400
        self.min_height = 300

        # TODO: Save to user's settings file
        self.font_family = self.FONT_FAMILY
        self.font_size = self.FONT_SIZE

        super().__init__(root)
        self.root = root

        root.title('PyPad')
        root.geometry(f'{self.width}x{self.height}')
        root.minsize(width=self.min_width, height=self.min_height)

        # Main textarea
        self.textarea = scrolledtext.ScrolledText(root, font=(
            self.font_family, self.font_size), borderwidth=0, highlightthickness=0)
        self.textarea.grid(row=0, column=1, sticky='nsew')

        self.textarea.config(yscrollcommand=self.yscroll)
        self.textarea.vbar.config(command=self.yview)

        # Line numbering area
        self.linenumberingarea = tk.Text(root, font=(
            self.font_family, self.font_size), borderwidth=0, background='#f0f0f0', foreground='#888', width=1, padx=5)
        self.linenumberingarea.grid(row=0, column=0, sticky='ns')
        self.linenumberingarea.insert('1.0', '1')
        self.linenumberingarea.config(state='disabled')

        self.linenumberingarea.tag_configure('line', justify='right')
        self.linenumberingarea.tag_add('line', '1.0', 'end')

        self.navbar = Navbar(self)
        self.shortcut_binding()

        root.grid_columnconfigure(0, weight=0)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

    def on_mousewheel(self, e):
        pass

    def yscroll(self, *args):
        self.textarea.vbar.set(*args)
        self.linenumberingarea.yview_moveto(args[1])
        # FIXME: It should be done after linenumber was changed

    def yview(self, *args):
        self.textarea.yview(*args)
        self.linenumberingarea.yview(*args)

    def text_modified(self, e):
        # self.on_mousewheel(e)
        lines = self.textarea.get("1.0", 'end').count('\n')

        self.linenumberingarea.config(state='normal')
        self.linenumberingarea.delete('1.0', 'end')
        self.linenumberingarea.insert("1.0", '\n'.join(
            [str(x + 1) for x in range(lines)]), 'line')
        self.linenumberingarea.config(
            state='disabled', width=int(len(str(lines))))

    def shortcut_binding(self):
        self.root.bind("<Control-=>", self.increase_fontsize)
        self.root.bind("<Control-minus>", self.decrease_fontsize)
        self.root.bind("<Control-0>", self.reset_fontsize)

        self.textarea.bind('<KeyRelease>', self.text_modified)
        # self.textarea.bind('<MouseWheel>', self.on_mousewheel)

    def __update_font(self):
        self.textarea.config(font=(self.font_family, self.font_size))
        self.linenumberingarea.config(font=(self.font_family, self.font_size))

    def increase_fontsize(self, e):
        self.font_size += 1
        self.__update_font()

    def decrease_fontsize(self, e):
        self.font_size -= 1
        self.__update_font()

    def reset_fontsize(self, e):
        self.font_size = self.FONT_SIZE
        self.__update_font()

    def show_version(self):
        messagebox.showinfo('Version', 'v0.0.1')

    def show_about(self):
        messagebox.showinfo(
            'About', 'PyPad\nProject for Języki Skryptowe\nBased on Tkinter')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
