#
# test_validate.py
#

import pytest

from connect_four.validate import validate_dimension, validate_token

def test_validate_dimension():
    assert validate_dimension(4) is None
    assert validate_dimension(8) is None
    with pytest.raises(TypeError):
        validate_dimension("4")
    with pytest.raises(ValueError):
        validate_dimension(3)

def test_validate_token():
    assert validate_token("O") is None
    assert validate_token("X") is None
    with pytest.raises(ValueError):
        validate_token("A")
