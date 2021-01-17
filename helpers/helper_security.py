from config import CONFIG
from utils import get_filename_from_path
from tkinter import messagebox
from tkinter import filedialog
from state import State
from frames.frame_encrypt import FrameEncrypt
from frames.frame_descrypt import FrameDecrypt
from cryptography.fernet import Fernet
from methods.AES import AES


class SecurityHelper:
    def __init__(self, navbar=None, parent=None):
        self.navbar = navbar
        self.parent = parent

    def show_encrypt_window(self):
        self.frame_encrypt = FrameEncrypt(root=self.parent.root, helper=self)
        self.frame_encrypt.run()

    def show_decrypt_window(self):
        self.frame_decrypt = FrameDecrypt(root=self.parent.root, helper=self)
        self.frame_decrypt.run()

    def on_listbox_select(self, e=None):
        selection = e.widget.curselection()
        if selection:
            State.encrypt_method = e.widget.get(selection[0])
            self.frame_encrypt.methods_list_label.config(text=f'Method to encrypt with: {State.encrypt_method}')

    def encrypt_file(self):
        if State.generated_key_filename and State.generated_key:
            try:
                f = Fernet(State.generated_key)
                token = f.encrypt(self.parent.textarea.get('1.0', 'end-1c').encode())
            except:
                return messagebox.showerror(title='Key', message='Something went wrong. Try to use another key.')
            
            ans = filedialog.asksaveasfilename(parent=self.parent, defaultextension='.txt', filetypes=CONFIG['DEFAULT_FILETYPES'], initialfile=get_filename_from_path(State.filename))
            if ans:
                State.filename = ans
                with open(State.filename, 'wb') as f:
                    f.write(token)
                    f.close()
                    self.navbar.file_helper.update_title(get_filename_from_path(State.filename))
                    self.frame_decrypt.destroy()
                    messagebox.showwarning(title='Success', message='File was successfully encrypted and saved. Do not lose your key.')
                    State.generated_key_filename = False
                    State.generated_key = False
        else:
            messagebox.showerror(title='Key', message='You need to generate random key first.')

    def choose_key(self):
        ans = filedialog.askopenfilename(parent=self.parent, filetypes=CONFIG["DEFAULT_FILETYPES_SECURE"])
        if ans:
            State.generated_key_filename = ans
            with open(State.generated_key_filename, 'rb') as f:
                State.generated_key = f.read()
                messagebox.showinfo(title='Success', message='Key was successrully read.')

    def generate_random_key(self):
        if State.encrypt_method == 'AES':
            State.generated_key = AES.generate_random_key()
        else:
            pass

        key_filename = filedialog.asksaveasfilename(title="Save as key", defaultextension='key', filetypes=CONFIG["DEFAULT_FILETYPES_SECURE"])
        if key_filename and State.generated_key:
            State.generated_key_filename = key_filename
            self.frame_encrypt.generate_key_label.config(text=f'Key: {get_filename_from_path(State.generated_key_filename)}')
            with open(key_filename, 'wb') as mk:
                mk.write(State.generated_key)
                messagebox.showinfo(title='Success', message='Key was saved successfully. You can now encrypt your file.')
        else:
            messagebox.showwarning(title='Empty key', message='You did not choose right path for key')