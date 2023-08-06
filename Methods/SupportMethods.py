import pygame


def get_string_of_ascii(value: int) -> str:
    if 32 < value < 127:
        return chr(value).upper()
    else:
        raise ValueError("Invalid Hotkey value")


def check_key_down(event: pygame.event, key: pygame.key) -> bool:
    return event.type == pygame.KEYDOWN and event.key == key


def remove_spaces(text_hot_key: str) -> str:
    return text_hot_key.replace(" ", "")


def is_convertible_to_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False
