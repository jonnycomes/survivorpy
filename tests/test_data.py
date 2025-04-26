import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from survivorpy import data
import os
import json

def test_get_table_names_from_cache(tmp_path):
    cache_path = tmp_path / "table_names.json"
    tables = ["castaways", "seasons"]
    cache_path.write_text(json.dumps(tables))

    with patch("survivorpy.data._CACHE_TABLE_NAME_PATH", str(cache_path)):
        result = data.get_table_names()
        assert result == tables

@patch("survivorpy.data.get_table_names", return_value=["castaways"])
@patch("os.path.exists", return_value=True)
@patch("pandas.read_parquet")
def test_load_uses_local_file(mock_read, mock_exists, mock_table_names):
    df_mock = pd.DataFrame({"name": ["Richard", "Kelly"]})
    mock_read.return_value = df_mock

    result = data.load("castaways")
    assert result.equals(df_mock)

def test_load_invalid_table_raises():
    with patch("survivorpy.data.get_table_names", return_value=["castaways"]):
        with pytest.raises(ValueError):
            data.load("aliens")
