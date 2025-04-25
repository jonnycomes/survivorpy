import pytest
import pandas as pd
from unittest.mock import patch, mock_open, MagicMock
from survivorpy import data
import os
import json


def test_load_table_names_from_cache(tmp_path):
    cache_path = tmp_path / "table_names.json"
    tables = ["castaways", "seasons"]
    cache_path.write_text(json.dumps(tables))

    with patch("survivorpy.data._CACHE_TABLE_NAME_PATH", str(cache_path)):
        result = data._load_table_names()
        assert result == tables

def test_load_table_names_refresh_downloads_from_s3(tmp_path):
    mock_data = ["tribes", "votes"]
    mocked_json = json.dumps(mock_data)

    with patch("survivorpy.data._CACHE_TABLE_NAME_PATH", str(tmp_path / "table_names.json")), \
         patch("survivorpy.data._fetch_table_names_from_s3") as mock_fetch, \
         patch("builtins.open", mock_open(read_data=mocked_json)):

        result = data._load_table_names(refresh=True)
        mock_fetch.assert_called_once()
        assert result == mock_data



@patch("survivorpy.data._load_table_names", return_value=["castaways"])
@patch("os.path.exists", return_value=True)
@patch("pandas.read_parquet")
def test_load_uses_local_file(mock_read, mock_exists, mock_table_names):
    df_mock = pd.DataFrame({"name": ["Richard", "Kelly"]})
    mock_read.return_value = df_mock

    result = data.load("castaways")
    assert result.equals(df_mock)

@patch("survivorpy.data._load_table_names", return_value=["votes"])
@patch("os.path.exists", return_value=False)
@patch("boto3.client")
@patch("pandas.read_parquet")
def test_load_from_s3(mock_read, mock_boto, mock_exists, mock_table_names):
    df_mock = pd.DataFrame({"vote": ["yes", "no"]})
    mock_read.return_value = df_mock

    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": MagicMock(read=lambda: b"parquet-bytes")}
    mock_boto.return_value = mock_s3

    result = data.load("votes", refresh=True)
    assert result.equals(df_mock)
    mock_s3.get_object.assert_called_once()

def test_load_invalid_table_raises():
    with patch("survivorpy.data._load_table_names", return_value=["castaways"]):
        with pytest.raises(ValueError):
            data.load("aliens")
