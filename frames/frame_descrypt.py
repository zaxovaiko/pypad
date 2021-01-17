import tkinter as tk
from config import CONFIG
from state import State


class FrameDecrypt(tk.Toplevel):
    def __init__(self, root=None, helper=None):
        super().__init__(root)

        self.root = root
        self.helper = helper

        self.title(CONFIG['DECRYPT_WINDOW_TITLE'])
        self.minsize(CONFIG["ENCRYPT_WINDOW_WIDTH"], CONFIG["ENCRYPT_WINDOW_HEIGHT"])
        self.resizable(0, 0)
        self.focus_force()

        self.key_label = tk.Label(self, text=f'Key: {State.encrypt_method}')
        self.key_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky='w')

        self.key_btn = tk.Button(self, text='Choose key')
        self.key_btn.grid(row=1, column=0, padx=10, columnspan=4, pady=(5, 10), sticky='nsew')

        self.encrypted_file_label = tk.Label(self, text=f'File to decrypt: {State.encrypt_method}')
        self.encrypted_file_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(10, 0), sticky='w')

        self.methods_list = tk.Button(self, text='Choose file to decrypt')
        self.methods_list.grid(row=3, column=0, padx=10, columnspan=4, pady=(5, 10), sticky='nsew')

        self.encrypt_btn = tk.Button(self, text='Decrypt file', command=self.helper.encrypt_file)
        self.encrypt_btn.grid(row=4, column=2, pady=(0, 10), sticky='we')

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.destroy())
        self.cancel_btn.grid(row=4, column=3, padx=(5, 10), pady=(0, 10), sticky='we')

        self.grid_columnconfigure(0, weight=1)

    def run(self):
        self.mainloop()
