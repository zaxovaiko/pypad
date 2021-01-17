from state import State
from config import CONFIG
from utils import get_filename_from_path
from cryptography.fernet import Fernet
from tkinter import filedialog, messagebox


class AES:
    @staticmethod
    def generate_random_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_file():
        pass

    @staticmethod
    def decrypt_file():
        pass