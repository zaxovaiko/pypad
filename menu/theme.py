import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import font
from menu.submenu.theme import ThemeSubMenu


class ThemeMenu(tk.Menu):
    def __init__(self, navbar):
        super().__init__(navbar.navbar, tearoff=0)

        self.add_command(label="Color", command=self.show_color_window)
        self.add_command(label="Font", command=self.show_font_window)

        self.navbar = navbar
        self.parent = navbar.parent
        self.theme_menu_sub = ThemeSubMenu(self)
        self.add_cascade(label='Zoom', menu=self.theme_menu_sub)

        self.background_color = '#fff'
        self.foreground_color = '#000'
        self.linenumering_color = '#ddd'

        self.font_size = self.parent.font_size
        self.font_family = self.parent.font_family

    def show_color_window(self):
        top = tk.Toplevel(self.navbar.parent)
        top.title('Theme')
        top.resizable(0, 0)

        self.body_color_label = tk.Label(top, text=f'Background color: {self.background_color}')
        self.body_color_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='w')

        self.body_color_btn = tk.Button(top, text='Choose body color', command=self.choose_background_color)
        self.body_color_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky='nsew')

        self.text_color_label = tk.Label(top, text=f'Foreground color: {self.foreground_color}')
        self.text_color_label.grid(row=2, column=0, padx=10, sticky='w')

        self.text_color_btn = tk.Button(top, text='Choose text color', command=self.choose_foreground_color)
        self.text_color_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10), sticky='nsew')

        self.set_theme_btn = tk.Button(top, text='Set theme', command=self.set_theme)
        self.set_theme_btn.grid(row=4, column=0, pady=(0, 10), sticky='e')

        self.cancel_btn = tk.Button(top, text='Cancel', command=lambda: top.destroy())
        self.cancel_btn.grid(row=4, column=1, padx=(5, 10), pady=(0, 10), sticky='we')

    def _from_rgb(self, rgb):
        # TODO: Add to utils
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'

    def choose_background_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            self.background_color = color[1]
            self.linenumering_color = self._from_rgb([int(abs(i - 30)) for i in color[0]])
            self.body_color_label.config(text=f'Background color: {self.background_color}')

    def choose_foreground_color(self):
        color = colorchooser.askcolor()
        if color[1]:
            self.foreground_color = color[1]
            self.text_color_label.config(text=f'Foreground color: {self.foreground_color}')

    def set_theme(self):
        self.parent.textarea.config(background=self.background_color, foreground=self.foreground_color)
        self.parent.linenumberingarea.config(background=self.linenumering_color, foreground=self.foreground_color)
        messagebox.showinfo(title='Theme', message='Theme was changed')

    def on_listbox_select(self, e):
        selection = e.widget.curselection()
        if selection:
            self.font_family = e.widget.get(selection[0])
            self.fonts_list_label.config(text=f'Font family: {self.parent.font_family}')

    def set_font(self):
        size = self.font_size_entry.get()
        try:
            self.parent.font_size = int(size)
            self.parent.font_family = self.font_family

            self.parent.textarea.config(font=(self.font_family, int(size)))
            self.parent.linenumberingarea.config(font=(self.font_family, int(size)))
            messagebox.showinfo(title='Font', message='Font was changed')
        except:
            messagebox.showerror(title='Font', message='Font size must be a number')

    def show_font_window(self):
        top = tk.Toplevel(self.navbar.parent)
        top.title('Font')
        top.resizable(0, 0)

        font_size_v = tk.StringVar()

        self.fonts_list_label = tk.Label(top, text=f'Font family: {self.font_family}')
        self.fonts_list_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky='w')

        self.fonts_list_select = tk.Listbox(top)
        self.fonts_list_select.grid(row=1, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')

        self.fonts_list_select.bind('<<ListboxSelect>>', self.on_listbox_select)
        for i, fm in enumerate(font.families()):
            self.fonts_list_select.insert(i, fm)

        self.font_size_label = tk.Label(top, text=f'Font size: {self.font_size}pt')
        self.font_size_label.grid(row=2, column=0, padx=10, sticky='w')

        self.font_size_entry = tk.Entry(top, text='Choose text color', textvariable=font_size_v)
        self.font_size_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=(5, 10), sticky='nsew')

        self.set_font_btn = tk.Button(top, text='Set font', command=self.set_font)
        self.set_font_btn.grid(row=4, column=1, pady=(0, 10), sticky='we')

        self.cancel_btn = tk.Button(top, text='Cancel', command=lambda: top.destroy())
        self.cancel_btn.grid(row=4, column=2, padx=(5, 10), pady=(0, 10), sticky='we')