import pygame


def get_string_of_ascii(value) -> str:
    if 32 < value < 127:
        return chr(value).upper()
    else:
        return "a"


def check_key_down(event, key) -> bool:
    return event.type == pygame.KEYDOWN and event.key == key


def remove_spaces(text_hot_key) -> str:
    return text_hot_key.replace(" ", "")


def is_convertible_to_int(string) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False
