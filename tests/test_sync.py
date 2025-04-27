import pytest
import json
import pandas as pd
from pathlib import Path
from io import BytesIO
from unittest.mock import patch, MagicMock, mock_open
from survivorpy import sync


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

