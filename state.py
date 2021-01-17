from config import CONFIG


class State:
    # TODO: Use instance properties
    filename = CONFIG['DEFAULT_NAME']

    font_family = CONFIG['DEFAULT_FONT_FAMILY']
    font_size = CONFIG['DEFAULT_FONT_SIZE']

    background_color = CONFIG['DEFAULT_BACKGROUND_COLOR']
    foreground_color = CONFIG['DEFAULT_FOREGROUND_COLOR']
    linenumbering_color = CONFIG['DEFAULT_LINENUMBERINGAREA_BACKGROUND_COLOR']

    is_modified = False
    is_saved = False

    find_position = CONFIG['DEFAULT_START_POSITION']

    encrypt_method = 'AES'
    generated_key_filename = False
    generated_key = False
