import json
from unittest import mock
from unittest.mock import patch, mock_open

import pytest

from Methods.ViewMethods import check_date_is_legal, get_start_month, get_start_day, get_start_year, \
    over_write_standard_day


def test_get_start_month():
    # Define the mock data for the JSON configuration
    mock_json_data = {
        "StartTime": {
            "Month": {
                "value": 8
            }
        }
    }

    # Convert the mock data to a JSON string
    mock_json_string = json.dumps(mock_json_data)

    # Use patch to mock the behavior of opening the JSON file and loading the data
    with patch("builtins.open", mock_open(read_data=mock_json_string)) as mock_file:
        # Call the function under test
        result = get_start_month()

    # Assert that the function returns the expected result
    assert result == 8


def test_get_start_day():
    # Define the mock data for the JSON configuration
    mock_json_data = {
        "StartTime": {
            "Day": {
                "value": 15
            }
        }
    }

    # Convert the mock data to a JSON string
    mock_json_string = json.dumps(mock_json_data)

    # Use patch to mock the behavior of opening the JSON file and loading the data
    with patch("builtins.open", mock_open(read_data=mock_json_string)) as mock_file:
        # Call the function under test
        result = get_start_day()

    # Assert that the function returns the expected result
    assert result == 15

def test_get_start_year():
    # Define the mock data for the JSON configuration
    mock_json_data = {
        "StartTime": {
            "Year": {
                "value": 1997
            }
        }
    }

    # Convert the mock data to a JSON string
    mock_json_string = json.dumps(mock_json_data)

    # Use patch to mock the behavior of opening the JSON file and loading the data
    with patch("builtins.open", mock_open(read_data=mock_json_string)) as mock_file:
        # Call the function under test
        result = get_start_year()

    # Assert that the function returns the expected result
    assert result == 1997


@pytest.mark.parametrize("day, month, year, expected_result", [
    (1, 1, 2023, True),    # Test case with a valid date
    (29, 2, 2024, True),   # Test case with a leap year, valid date
    (31, 12, 2023, True),  # Test case with a valid date
    (30, 4, 2023, True),
    (21, 2, 2023, True),
    (29, 2, 2100, True),   # Test case with a leap year, valid date
    # Add more valid test cases as needed
])
def test_valid_check_date_is_legal(day, month, year, expected_result):
    assert check_date_is_legal(day, month, year) == expected_result


@pytest.mark.parametrize("day, month, year, expected_result", [
    (31, 4, 2023, False),   # April has only 30 days (invalid date)
    (29, 2, 2023, False),   # Not a leap year, February 29 is invalid
    (32, 12, 2023, False),  # December has only 31 days (invalid date)
    (0, 1, 2023, False),    # Day cannot be 0 (invalid date)
    (1, 13, 2023, False),   # Month cannot be greater than 12 (invalid date)
    (30, 2, 2024, False),
    # Add more invalid test cases as needed
])
def test_invalid_check_date_is_legal(day, month, year, expected_result):
    assert check_date_is_legal(day, month, year) == expected_result


def test_over_write_standard_day():
    # Define the mock JSON data with the day value set to 212
    mock_json_data = '{"StartTime": {"Day": {"value": 212}}}'

    # Use patch to mock the behavior of opening the JSON file and reading the data
    with patch("builtins.open", mock_open(read_data=mock_json_data)) as mock_file:
        # Use side_effect to return a mocked file object for writing
        mock_file_handle = mock_file()
        mock_file_handle.write = mock.Mock()

        # Use patch to mock the behavior of json.dump
        with patch("json.dump") as mock_dump:
            # Call the function under test
            over_write_standard_day()

    # Assert that the file is opened in read-write mode ('r+')
    mock_file.assert_called_with("./Globals/RocketConfig/CurrentRocketConfig.json", "r+")

    # Assert that json.dump is called once with the modified data
    mock_dump.assert_called_once_with(
        {"StartTime": {"Day": {"value": 28}}},
        mock_file_handle,
        indent=4,
        ensure_ascii=False
    )

    # Assert that the file is closed after the write operation
    mock_file_handle.close.assert_called_once()