import pytest
import json
import pandas as pd
from pathlib import Path
from io import BytesIO
from unittest.mock import patch, MagicMock, mock_open
from survivorpy import sync

@patch("survivorpy.sync._CACHE_DIR")
@patch("survivorpy.sync._CACHE_DATA_DIR")
@patch("survivorpy.sync._CACHE_TABLE_NAMES_PATH")
@patch("survivorpy.sync._CACHE_LAST_SYNCED_PATH")
def test_has_cache(mock_last_synced_path, mock_table_names_path, mock_cache_data_dir, mock_cache_dir):
    # Case 1: Cache is set up properly
    mock_cache_dir.exists.return_value = True
    mock_cache_dir.is_dir.return_value = True
    mock_cache_data_dir.exists.return_value = True
    mock_cache_data_dir.is_dir.return_value = True
    mock_cache_data_dir.iterdir.return_value = [Path("fake_file")]  # Simulate non-empty directory
    mock_table_names_path.exists.return_value = True
    mock_table_names_path.is_file.return_value = True
    mock_last_synced_path.exists.return_value = True
    mock_last_synced_path.is_file.return_value = True

    assert sync.has_cache() is True  # Should return True when everything exists

    # Case 2: Cache directory does not exist
    mock_cache_dir.exists.return_value = False
    assert sync.has_cache() is False  # Should return False when _CACHE_DIR does not exist
    mock_cache_dir.exists.return_value = True

    # Case 3: Cache directory exists but is not a directory
    mock_cache_dir.is_dir.return_value = False
    assert sync.has_cache() is False  # Should return False when _CACHE_DIR is not a directory
    mock_cache_dir.is_dir.return_value = True

    # Case 4: _CACHE_DATA_DIR exists but is empty
    mock_cache_data_dir.iterdir.return_value = []  # Empty directory
    assert sync.has_cache() is False  # Should return False when _CACHE_DATA_DIR is empty
    mock_cache_data_dir.iterdir.return_value = [Path("fake_file")]

    # Case 5: _CACHE_TABLE_NAMES_PATH does not exist
    mock_table_names_path.exists.return_value = False
    assert sync.has_cache() is False  # Should return False when _CACHE_TABLE_NAMES_PATH does not exist
    mock_table_names_path.exists.return_value = True

    # Case 6: _CACHE_LAST_SYNCED_PATH does not exist
    mock_last_synced_path.exists.return_value = False
    assert sync.has_cache() is False  # Should return False when _CACHE_LAST_SYNCED_PATH does not exist
    mock_last_synced_path.exists.return_value = True

@patch("survivorpy.sync.boto3.client")
@patch("survivorpy.sync.pd.read_parquet")
def test_cache_data_saves_parquet(mock_read, mock_boto):
    s3_mock = MagicMock()
    s3_mock.get_object.return_value = {"Body": BytesIO(b"fake data")}
    mock_boto.return_value = s3_mock

    df_mock = pd.DataFrame({"x": [1]})
    mock_read.return_value = df_mock

    with patch("survivorpy.sync._CACHE_DATA_DIR", Path("/tmp")):
        sync._cache_data(["castaways"])
        s3_mock.get_object.assert_called_once()
        mock_read.assert_called_once()

@patch("survivorpy.sync.boto3.client")
def test_cache_table_names_downloads_file(mock_boto):
    s3_mock = MagicMock()
    mock_boto.return_value = s3_mock

    with patch("survivorpy.sync._CACHE_TABLE_NAMES_PATH", Path("/tmp/table_names.json")):
        sync._cache_table_names()
        s3_mock.download_file.assert_called_once()

@patch("builtins.open", new_callable=mock_open)
@patch("survivorpy.sync.datetime")
def test_update_last_synced_writes_json(mock_datetime, mock_open_file):
    mock_datetime.utcnow.return_value.isoformat.return_value = "2024-01-01T00:00:00"

    with patch("survivorpy.sync._CACHE_LAST_SYNCED_PATH", Path("/tmp/last_synced.json")):
        sync._update_last_synced()

    handle = mock_open_file()
    written = "".join(call.args[0] for call in handle.write.call_args_list)
    assert written == '{"timestamp": "2024-01-01T00:00:00"}'

