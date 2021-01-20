import tkinter as tk
from config import CONFIG
from state import State
from utils import get_filename_from_path


class FrameDecrypt(tk.Toplevel):
    def __init__(self, root=None, helper=None):
        super().__init__(root)

        self.root = root
        self.helper = helper

        self.title(CONFIG['DECRYPT_WINDOW_TITLE'])
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
        self.key_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(10, 0), sticky='w')

        self.key_btn = tk.Button(self, text='Choose key', command=self.helper.choose_key)
        self.key_btn.grid(row=3, column=0, padx=10, columnspan=4, pady=(5, 10), sticky='nsew')

        self.encrypted_file_label = tk.Label(self, text=f'File to decrypt: {get_filename_from_path(State.filename) or ""}')
        self.encrypted_file_label.grid(row=4, column=0, columnspan=4, padx=10, pady=(10, 0), sticky='w')

        self.choose_file_btn = tk.Button(self, text='Choose file to decrypt', command=self.helper.choose_file_to_decrypt)
        self.choose_file_btn.grid(row=5, column=0, padx=10, columnspan=4, pady=(5, 10), sticky='nsew')

        self.decrypt_btn = tk.Button(self, text='Decrypt file', command=self.helper.decrypt_file)
        self.decrypt_btn.grid(row=6, column=2, pady=(0, 10), sticky='we')

        self.cancel_btn = tk.Button(self, text='Cancel', command=lambda: self.destroy())
        self.cancel_btn.grid(row=6, column=3, padx=(5, 10), pady=(0, 10), sticky='we')

        self.grid_columnconfigure(0, weight=1)

    def run(self):
        self.mainloop()
