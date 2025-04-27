import pytest
from unittest.mock import patch

@patch("survivorpy.get_table_names", return_value=["castaways", "seasons"])
@patch("survivorpy.load", return_value="MOCK")
def test_getattr_returns_table(mock_load, mock_tables):
    import survivorpy
    assert survivorpy.castaways == "MOCK"
    assert survivorpy.seasons == "MOCK"

@patch("survivorpy.get_table_names", return_value=["castaways"])
def test_getattr_invalid_table_raises(mock_tables):
    import survivorpy
    with pytest.raises(AttributeError):
        _ = survivorpy.invalid_name
