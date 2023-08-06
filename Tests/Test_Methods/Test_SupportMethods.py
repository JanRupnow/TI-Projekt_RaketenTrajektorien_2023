import unittest

import pygame
import pytest

from Methods.SupportMethods import get_string_of_ascii, remove_spaces, check_key_down, is_convertible_to_int


@pytest.mark.parametrize("ascii_value, expected_output", [
    (65, 'A'),  # Test case with uppercase 'A'
    (97, 'A'),  # Test case with lowercase 'a' (should return 'A')
    (122, 'Z'),  # Test case with lowercase 'z' (should return 'Z')
    # Limit tests
    (33, '!'),  # Test case with exclamation mark '!'
    (126, '~'),  # Test case with tilde '~'
])
def test_valid_ascii_value(ascii_value, expected_output) -> None:
    assert get_string_of_ascii(ascii_value) == expected_output


def test_invalid_ascii_value() -> None:
    with pytest.raises(ValueError):
        get_string_of_ascii(32)  # ASCII value 32 is below the valid range (should raise ValueError)
    with pytest.raises(ValueError):
        get_string_of_ascii(127)  # ASCII value 127 is above the valid range (should raise ValueError)
    with pytest.raises(ValueError):
        get_string_of_ascii(29)  # ASCII value 32 is below the valid range (should raise ValueError)


@pytest.mark.parametrize("input_str, expected_output", [
    ("t e   s   t", "test"),  # Test case with multiple spaces
    ("test", "test"),  # Test case with no spaces
    ("t E sss T", "tEsssT"),  # Test case with mixed case and spaces
    ("   ", ""),  # Test case with only spaces (should return empty string)
    ("   a b c  ", "abc"),  # Test case with spaces at the beginning and end
    ("     ", ""),  # Test case with multiple spaces (should return empty string)
    ("123 456 789", "123456789"),  # Test case with digits and spaces
    (" Hello  World ", "HelloWorld"),  # Test case with spaces around words
])
def test_remove_spaces(input_str, expected_output) -> None:
    assert remove_spaces(input_str) == expected_output


@pytest.mark.parametrize("event_type, event_key, key, expected_result", [
    (pygame.KEYDOWN, pygame.K_a, pygame.K_a, True),  # Keydown event with matching key
    (pygame.KEYUP, pygame.K_a, pygame.K_a, False),  # Keyup event with matching key (should return False)
    (pygame.KEYDOWN, pygame.K_a, pygame.K_b, False),  # Keydown event with non-matching key (should return False)
    (pygame.KEYUP, pygame.K_a, pygame.K_b, False),  # Keyup event with non-matching key (should return False)
    (pygame.KEYDOWN, pygame.K_a, pygame.K_a + 1, False)  # Keydown event with similar key code (should return False)
])
def test_check_key_down(event_type, event_key, key, expected_result) -> None:
    event = pygame.event.Event(event_type, key=event_key)
    assert check_key_down(event, key) == expected_result


@pytest.mark.parametrize("input_value, expected_result", [
    ("123", True),  # Test case with a valid integer string
    ("-45", True),  # Test case with a valid negative integer string
    ("0", True),  # Test case with a valid zero string
    ("3.14", False),  # Test case with a float string (not convertible)
    ("abc", False),  # Test case with an alphabetic string (not convertible)
    ("123abc", False),  # Test case with an alphanumeric string (not convertible)
    ("", False),  # Test case with an empty string (not convertible)
])
def test_is_convertible_to_int(input_value, expected_result) -> None:
    assert is_convertible_to_int(input_value) == expected_result


