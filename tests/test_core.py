import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from survivorpy import core

@patch("survivorpy.core._load_table_names", return_value=["castaways"])
@patch("os.path.exists", return_value=True)
@patch("pandas.read_parquet")
def test_load_uses_local_file(mock_read, mock_exists, mock_table_names):
    df_mock = pd.DataFrame({"name": ["Richard", "Kelly"]})
    mock_read.return_value = df_mock

    result = core.load("castaways")
    assert result.equals(df_mock)

@patch("survivorpy.core._load_table_names", return_value=["votes"])
@patch("os.path.exists", return_value=False)
@patch("boto3.client")
@patch("pandas.read_parquet")
def test_load_from_s3(mock_read, mock_boto, mock_exists, mock_table_names):
    df_mock = pd.DataFrame({"vote": ["yes", "no"]})
    mock_read.return_value = df_mock

    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = {"Body": MagicMock(read=lambda: b"parquet-bytes")}
    mock_boto.return_value = mock_s3

    result = core.load("votes", refresh=True)
    assert result.equals(df_mock)
    mock_s3.get_object.assert_called_once()

def test_load_invalid_table_raises():
    with patch("survivorpy.core._load_table_names", return_value=["castaways"]):
        with pytest.raises(ValueError):
            core.load("aliens")
