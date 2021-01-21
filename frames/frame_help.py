import tkinter as tk
from tkinter import ttk


class FrameHelp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent.root)

        self.parent = parent

        self.title('Help')
        self.resizable(0, 0)
        self.focus_force()

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0)

        self.edit_sub_frame = tk.Frame(self.notebook, width=300, height=300)
        self.edit_sub_frame.pack(fill='both', expand=1)

        self.security_sub_frame = tk.Frame(self.notebook, width=300, height=300)
        self.security_sub_frame.pack(fill='both', expand=1)

        self.theme_sub_frame = tk.Frame(self.notebook, width=300, height=300)
        self.theme_sub_frame.pack(fill='both', expand=1)

        # Setting text ----------------------------------------------------
        helper_text = '\nFind window\n\nTo open Find dialog on the top bar click Edit > Find. Then you will see a window with few fields.' \
                      'Enter whatever you want in text entry and click "Find". The program will automatically find the first match in main textarea.' \
                      'After clicking button one more time the program will show every next occurrence. You can also choose an option "Match as regex",' \
                      'which means you will be able to use regular expressions to find what you want. To close the window without finding any text' \
                      'you can click "Cancel" button or just close the entire window.\n\nReplace window\n\nTo open replace window click Edit > Replace of use Ctrl + R hotkey.' \
                      'In first text area enter text which you want to be replaced. Then in second text area enter text which you want to be replaced with.' \
                      'To replace ONLY one occurrence click "Replace". To replace one or more occurrences click "Replace All".'
        self.edit_helper_text = tk.Label(self.edit_sub_frame, text=helper_text, wraplength=300, justify='left')
        self.edit_helper_text.grid(row=0, column=0)

        helper_text = '\nEncrypt window\n\nTo open Encrypt dialog on the top bar click Security > Encrypt. You will see a window with list and two main buttons.' \
                      'In that list you can choose an algorithm you want to use to encode your file. To choose it just click on it\'s name. You will see that text label' \
                      'also changed. Then click on "Choose key" button to choose a key you will encode file with. Or if you want to use another one click on ' \
                      '"New key" to generate a new random binary key. After creating or choosing a key you will see a message action was done successfully.' \
                      'That means you can now encode your file with clicking on "Encrypt file". Don\'t forget a method you were encoding with!' \
                      '\n\nDecrypt window\n\nTo open decrypt window click Security > Decrypt. You will see a similar window with two buttons and list.' \
                      'First step choose an algorithm. Then choose your key. Then choose file to decrypt and click on "Decrypt" button.' \
                      'File will be automatically decrypted. If some errors will occurr you will see a message. After decoding you will see a decoded content of the file' \
                      ' on main text area.'
        self.security_helper_text = tk.Label(self.security_sub_frame, text=helper_text, wraplength=300, justify='left')
        self.security_helper_text.grid(row=0, column=0)

        helper_text = '\nColor window\n\nTo open Color dialog on the top bar click Theme > Color. There you can choose a color of your application.' \
        'After clicking on "Choose background color" button you will be able to choose any color you want. After selection one of them you will see ' \
        'that label changed. Then click "Choose foreground color" to choose font color as well. After saving and setting theme main background of your application'\
        'will be changed. To reset background and font color click "Reset theme". \n\nFont window\n\nTo open Font dialog click Theme > Font.' \
        'You will see a window with list and text entry. To choose a font select it from the list. Then enter a size of font you want set to. And then click "Set font"' \
        ' button to apply changes.\n\nTo save current preferences click Theme > Save preferences at the bottom of menu. The config file will be created.'
        self.theme_helper_text = tk.Label(self.theme_sub_frame, text=helper_text, wraplength=300, justify='left')
        self.theme_helper_text.grid(row=0, column=0)

        self.notebook.add(self.edit_sub_frame, text='Edit')
        self.notebook.add(self.security_sub_frame, text='Security')
        self.notebook.add(self.theme_sub_frame, text='Theme')
