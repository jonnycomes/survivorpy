import pytest
from unittest.mock import patch

def test_getattr_returns_dataframe():
    import survivorpy
    with patch("survivorpy.load", return_value="MOCK"), \
         patch("survivorpy.TABLE_NAMES", ["castaways"]):
        assert survivorpy.castaways == "MOCK"

def test_getattr_invalid_raises():
    import survivorpy
    with patch("survivorpy.TABLE_NAMES", ["castaways"]):
        with pytest.raises(AttributeError):
            _ = survivorpy.invalid_name
