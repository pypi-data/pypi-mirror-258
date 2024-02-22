"""Module to test the OqDateTime object."""
from onequant.util.datetime import OqDateTime


def test_timestamp_to_string():
    """Test the conversion of timestamp to string."""
    timestamp = 1627660800  # 2021-07-31 00:00:00
    expected_result = '2021-07-31 00:00:00'
    assert OqDateTime.timestamp_to_string(timestamp) == expected_result


def test_string_to_timestamp():
    """Test the conversion of string to timestamp."""
    date_string = '2021-07-31 00:00:00'
    expected_result = 1627660800  # 2021-07-31 00:00:00
    assert OqDateTime.string_to_timestamp(date_string) == expected_result


def test_string_to_ms_timestamp():
    """Test the conversion of string to milliseconds timestamp."""
    date_string = '2021-07-31 00:00:00'
    expected_result = 1627660800000  # 2021-07-31 00:00:00 in milliseconds
    assert OqDateTime.string_to_ms_timestamp(date_string) == expected_result
