import pytest
from src.reddit.preprocessing import convert_numk2int 


def test_invalid_number_k_format():
    with pytest.raises(ValueError):
        convert_numk2int("2a")
    with pytest.raises(ValueError):
        convert_numk2int("2.5kak")


def test_valid_number_k_format():
    assert convert_numk2int("2")[0] == 2
    assert convert_numk2int("2k")[0] == 2000
    assert convert_numk2int("2.5k")[0] == 2500
    assert convert_numk2int("2.5kk")[0] == 2500000
    assert convert_numk2int("2.52k")[0] == 2520