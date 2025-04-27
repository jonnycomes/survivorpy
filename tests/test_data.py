import pytest
import pandas as pd
import json
from unittest.mock import patch
from survivorpy import data

@patch("survivorpy.data._CACHE_TABLE_NAMES_PATH", new_callable=lambda: "/tmp/mock_table_names.json")
def test_get_table_names_from_cache(mock_path, tmp_path):
    tables = ["castaways", "seasons"]
    cache_file = tmp_path / "mock_table_names.json"
    cache_file.write_text(json.dumps(tables))

    with patch("survivorpy.data._CACHE_TABLE_NAMES_PATH", str(cache_file)):
        result = data.get_table_names()
        assert result == tables

@patch("survivorpy.data.pd.read_parquet")
@patch("survivorpy.config.Path.exists", return_value=True)
@patch("survivorpy.data.get_table_names", return_value=["castaways"])
def test_load_reads_local_file(mock_get_names, mock_exists, mock_read):
    df_mock = pd.DataFrame({"name": ["Richard", "Kelly"]})
    mock_read.return_value = df_mock

    result = data.load("castaways")
    pd.testing.assert_frame_equal(result, df_mock)

@patch("survivorpy.data.get_table_names", return_value=["castaways"])
def test_load_invalid_table_raises(mock_get_names):
    with pytest.raises(ValueError):
        data.load("not_a_table")

@patch("survivorpy.data._CACHE_LAST_SYNCED_PATH", new_callable=lambda: "/tmp/mock_last_synced.json")
def test_get_last_synced(mock_path, tmp_path):
    synced_time = "2023-12-25T12:34:56"
    file_path = tmp_path / "mock_last_synced.json"
    file_path.write_text(json.dumps({"timestamp": synced_time}))

    with patch("survivorpy.data._CACHE_LAST_SYNCED_PATH", str(file_path)):
        assert data.get_last_synced() == synced_time
