class Utils:
    @staticmethod
    def get_cursor_position(ln, col):
        return f'{ln}.{col}'

    @staticmethod
    def get_filename_from_path(path):
        return path.split('/')[-1]

    @staticmethod
    def rgb_to_hex(rgb):
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'