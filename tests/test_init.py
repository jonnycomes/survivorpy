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

@patch("survivorpy.get_table_names", return_value=["castaways", "seasons"])
def test_TABLE_NAMES_attribute(mock_get_names):
    import survivorpy
    assert survivorpy.TABLE_NAMES == ["castaways", "seasons"]

@patch("survivorpy.get_last_synced", return_value="2024-01-01T00:00:00")
def test_LAST_SYNCED_attribute(mock_sync_time):
    import survivorpy
    assert survivorpy.LAST_SYNCED == "2024-01-01T00:00:00"
