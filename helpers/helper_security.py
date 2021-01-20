from config import CONFIG
from state import State
from utils import get_filename_from_path
from tkinter import messagebox, filedialog
from frames.frame_encrypt import FrameEncrypt
from frames.frame_decrypt import FrameDecrypt

from Cryptodome.Cipher import AES, DES3, Salsa20
from Cryptodome.Random import get_random_bytes


class SecurityHelper:
    def __init__(self, navbar=None, parent=None):
        self.navbar = navbar
        self.parent = parent

        self.frame_encrypt = None
        self.frame_decrypt = None

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
            string = f'Method to encrypt with: {State.encrypt_method}'
            try:
                self.frame_decrypt.methods_list_label.config(text=string)
            except: pass
            try:
                self.frame_encrypt.methods_list_label.config(text=string)
            except: pass

    def encrypt_file(self):
        to_encrypt = self.parent.textarea.get('1.0', 'end-1c')

        if State.generated_key_filename and State.generated_key:
            if State.encrypt_method == 'AES':
                cipher = AES.new(State.generated_key, AES.MODE_EAX)
                ciphertext, tag = cipher.encrypt_and_digest(to_encrypt.encode())
                token = cipher.nonce + tag + ciphertext
            elif State.encrypt_method == 'Triple DES':
                cipher = DES3.new(State.generated_key, DES3.MODE_CFB)
                token = cipher.iv + cipher.encrypt(to_encrypt.encode())
            elif State.encrypt_method == 'Salsa20':
                cipher = Salsa20.new(key=State.generated_key)
                token = cipher.nonce + cipher.encrypt(to_encrypt.encode())
            else:
                return messagebox.showerror(title='Key', message='Something went wrong. Close the window and try again.')

            ans = filedialog.asksaveasfilename(parent=self.parent, defaultextension='.txt', filetypes=CONFIG['DEFAULT_FILETYPES'], initialfile=get_filename_from_path(State.filename))
            if ans:
                State.filename = ans
                with open(State.filename, 'wb') as f:
                    f.write(token)
                    f.close()
                    self.navbar.file_helper.update_title(get_filename_from_path(State.filename))
                    self.frame_encrypt.destroy()

                    messagebox.showwarning(title='Success', message='File was successfully encrypted and saved. Do not lose your key.')

                    State.is_modified = False
                    State.generated_key_filename = False
                    State.generated_key = False
                    State.encrypt_method = CONFIG['DEFAULT_ENCRYPTION_METHOD']
        else:
            messagebox.showerror(title='Key', message='You need to generate random key first.')

    def decrypt_file(self):
        if State.encrypt_method and State.filename and State.generated_key:
            with open(State.filename, 'rb') as f:
                text = f.read()
                try:
                    if State.encrypt_method == 'AES':
                        cipher = AES.new(State.generated_key, AES.MODE_EAX, text[:16])
                        decoded = cipher.decrypt_and_verify(text[32:], text[16:32])
                    elif State.encrypt_method == 'Triple DES':
                        cipher = DES3.new(State.generated_key, DES3.MODE_CFB)
                        decoded = cipher.decrypt(text)[len(cipher.iv):]
                    elif State.encrypt_method == 'Salsa20':
                        cipher = Salsa20.new(key=State.generated_key, nonce=text[:8])
                        decoded = cipher.decrypt(text[8:])
                    else:
                        return messagebox.showerror(title='Error', message='Choose algorithm to decode with')
                except Exception as e:
                    print(e)
                    return messagebox.showerror(title='Wrong key', message='File can not be decoded with this key. Try another one.')

                self.parent.textarea.delete('1.0', 'end-1c')
                self.parent.textarea.insert('1.0', decoded)
                self.parent.root.navbar.file_helper.text_modified()
                self.parent.textarea.see('1.0')
                self.parent.linenumberingarea.see('1.0')
                messagebox.showinfo(title='Success', message='File was decoded successfully.')
        else:
            messagebox.showerror(title='Error', message='Something went wrong. Try again.')

    def choose_key(self):
        ans = filedialog.askopenfilename(parent=self.parent, filetypes=CONFIG["DEFAULT_FILETYPES_SECURE"])
        if ans:
            State.generated_key_filename = ans
            with open(State.generated_key_filename, 'rb') as f:
                State.generated_key = f.read()
                filename = f'Key: {get_filename_from_path(State.generated_key_filename)}'
                try:
                    self.frame_decrypt.key_label.config(text=filename)
                except: pass
                try:
                    self.frame_encrypt.key_label.config(text=filename)
                except: pass
                messagebox.showinfo(title='Success', message='Key was successfully read.')

    def choose_file_to_decrypt(self):
        ans = filedialog.askopenfilename(parent=self.parent, defaultextension='.txt', filetypes=CONFIG['DEFAULT_FILETYPES'])
        if ans:
            State.filename = ans
            self.frame_decrypt.encrypted_file_label.config(text=f'File to decrypt: {get_filename_from_path(State.filename)}')
            messagebox.showinfo(title='Success', message='File was chosen successfully.')
        else:
            messagebox.showwarning(title='File reading', message='You did not read the file!')

    def generate_random_key(self):
        if State.encrypt_method == 'AES':
            State.generated_key = get_random_bytes(16)
        elif State.encrypt_method == 'Triple DES':
            while True:
                try:
                    State.generated_key = DES3.adjust_key_parity(get_random_bytes(24))
                    break
                except ValueError:
                    pass
        elif State.encrypt_method == 'Salsa20':
            State.generated_key = get_random_bytes(32)

        key_filename = filedialog.asksaveasfilename(title="Save key", defaultextension='key', filetypes=CONFIG["DEFAULT_FILETYPES_SECURE"])
        if key_filename and State.generated_key:
            State.generated_key_filename = key_filename
            self.frame_encrypt.key_label.config(text=f'Key: {get_filename_from_path(State.generated_key_filename)}')
            with open(key_filename, 'wb') as f:
                f.write(State.generated_key)
                messagebox.showinfo(title='Success', message='Key was saved successfully. You can now encrypt your file.')
        else:
            messagebox.showwarning(title='Empty key', message='You did not choose right path for key')
