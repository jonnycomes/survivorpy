import os
import json
import pytest
from unittest.mock import patch, mock_open
from survivorpy import table_names

def test_load_table_names_from_cache(tmp_path):
    cache_path = tmp_path / "table_names.json"
    data = ["castaways", "seasons"]
    cache_path.write_text(json.dumps(data))

    with patch("survivorpy.table_names._CACHE_PATH", str(cache_path)):
        result = table_names._load_table_names()
        assert result == data

def test_load_table_names_refresh_downloads_from_s3(tmp_path):
    mock_data = ["tribes", "votes"]
    mocked_json = json.dumps(mock_data)

    with patch("survivorpy.table_names._CACHE_PATH", str(tmp_path / "table_names.json")), \
         patch("survivorpy.table_names._fetch_table_names_from_s3") as mock_fetch, \
         patch("builtins.open", mock_open(read_data=mocked_json)):

        result = table_names._load_table_names(refresh=True)
        mock_fetch.assert_called_once()
        assert result == mock_data
