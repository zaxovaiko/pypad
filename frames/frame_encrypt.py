import tkinter as tk
from config import CONFIG
from state import State


class FrameEncrypt(tk.Toplevel):
    def __init__(self, root=None, helper=None):
        super().__init__(root)

        self.iconbitmap(r'icon.ico')
        self.root = root
        self.helper = helper

        self.title(CONFIG['ENCRYPT_WINDOW_TITLE'])
        self.minsize(CONFIG["ENCRYPT_WINDOW_WIDTH"], CONFIG["ENCRYPT_WINDOW_HEIGHT"])
        self.resizable(0, 0)
        self.focus_force()

        self.methods_list_label = tk.Label(self, text=f'Method to encrypt with: {State.encrypt_method}')
        self.methods_list_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky='w')

        self.methods_list = tk.Listbox(self, height=4)
        self.methods_list.grid(row=1, column=0, padx=10, columnspan=4, pady=(5, 10), sticky='nsew')

        self.methods_list.bind('<<ListboxSelect>>', self.helper.on_listbox_select)
        for i, m in enumerate(CONFIG['ENCRYPTION_METHODS']):
            self.methods_list.insert(i, m)

        self.key_label = tk.Label(self, text=f'Key: {State.generated_key_filename or ""}')
        self.key_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 0), sticky='w')

        self.key_btn = tk.Button(self, text='New key', command=self.helper.generate_random_key)
        self.key_btn.grid(row=3, column=0, columnspan=2, padx=(10, 5), pady=(0, 10), sticky='we')

        self.choose_key_btn = tk.Button(self, text='Choose key', command=self.helper.choose_key)
        self.choose_key_btn.grid(row=3, column=2, columnspan=2, padx=(0, 10), pady=(0, 10), sticky='we')

        self.encrypt_btn = tk.Button(self, text='Encrypt file', command=self.helper.encrypt_file)
        self.encrypt_btn.grid(row=4, column=2, pady=(0, 10), sticky='we')

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.destroy())
        self.cancel_btn.grid(row=4, column=3, padx=(5, 10), pady=(0, 10), sticky='we')

        self.grid_columnconfigure(0, weight=1)

    def run(self):
        self.mainloop()
