import pytest
from src.reddit.preprocessing import convert_number_k_format_to_number


def test_invalid_number_k_format():
    with pytest.raises(ValueError):
        convert_number_k_format_to_number("2a")
    with pytest.raises(ValueError):
        convert_number_k_format_to_number("2.5kak")


def test_valid_number_k_format():
    assert convert_number_k_format_to_number("2") == 2
    assert convert_number_k_format_to_number("2k") == 2000
    assert convert_number_k_format_to_number("2.5k") == 2500
    assert convert_number_k_format_to_number("2.5kk") == 2500000
    assert convert_number_k_format_to_number("2.52k") == 2520