import json
import pandas as pd
import requests
import base64
from .sync import _cache_table_names, _cache_data, _update_last_synced
from .config import _CACHE_DATA_DIR, _CACHE_TABLE_NAMES_PATH, _CACHE_LAST_SYNCED_PATH

def refresh_data():
    """
    Refresh the local data cache by downloading the latest available datasets from the source.

    This function updates all Survivor datasets and the list of available table names.
    It should be used when you want to ensure you have the most current version of the data.

    After calling this function, you can access updated datasets using `load("table_name")` 
    or module-level attributes like `survivorpy.castaways`.

    Example:
        from survivorpy import refresh_data
        refresh_data()
    """
    if get_last_synced() < _get_last_data_updated():
        _cache_table_names()
        table_names = get_table_names()
        _cache_data(table_names)
        _update_last_synced()
    else:
        print("Data is already up to date. No refresh needed.")

def load(table: str) -> pd.DataFrame:
    """
    Load a Survivor dataset from the local cache.

    This function reads a previously cached dataset into a pandas DataFrame. 
    It does not attempt to download or refresh the data. Use `refresh_data()` 
    first if you need to ensure the local data is up to date.

    Parameters:
        table (str): The name of the dataset to load (e.g., "castaways").

    Returns:
        pd.DataFrame: The requested dataset.

    Raises:
        ValueError: If the provided table name is not recognized.
        OSError, ValueError, etc.: If the local file is missing or unreadable.

    Example:
        import survivorpy as sv
        df = sv.load("castaways")
    """
    table_names_list = get_table_names()

    if table not in table_names_list:
        raise ValueError(f"Unknown table: '{table}'. Choose from: {table_names_list}")

    local_path = _CACHE_DATA_DIR / f"{table}.parquet"
    return pd.read_parquet(local_path)

def get_table_names():
    """
    Load the list of available Survivor datasets from the local cache.

    This function reads the names of previously cached datasets. It does not attempt 
    to download or refresh the data. Use `refresh_data()` to update the cache 
    if you need to ensure the list of datasets is current.

    Returns:
        list[str]: A list of dataset names (e.g., [..., "castaways",...]).

    Raises:
        OSError: If the table names cache file is missing or unreadable.

    Example:
        import survivorpy as sv
        tables = sv.get_table_names()

    Notes:
        You can also access the available table names via the `TABLE_NAMES` attribute.
    """
    with open(_CACHE_TABLE_NAMES_PATH, "r") as f:
        return json.load(f)

def get_last_synced():
    """
    Return the timestamp of the most recent successful data sync.

    Returns:
        str: An ISO 8601 timestamp string (e.g., "2025-04-25T19:12:05.123Z").

    Raises:
        FileNotFoundError: If the sync timestamp file does not exist.
        ValueError: If the file contents are invalid.

    Example:
        import survivorpy as sv
        tables = sv.get_last_synced()

    Notes:
        You can also access the available table names via the `LAST_SYNCED` attribute.

    """
    with open(_CACHE_LAST_SYNCED_PATH, "r") as f:
        return json.load(f)["timestamp"]

def _get_last_data_updated():
    """
    Return the timestamp of the last data update recorded in the GitHub repository.

    Returns:
        str: An ISO 8601 timestamp string (e.g., "2025-04-25T19:12:05.123Z").

    Raises:
        Exception: If the request to GitHub fails or the data is invalid.

    Notes:
        This function checks the 'data_pipeline/data_last_updated.json' file in the repository.
    """
    url = "https://api.github.com/repos/jonnycomes/survivorpy/contents/data_pipeline/data_last_updated.json?ref=update-refresh-logic"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"GitHub API request failed (status code {response.status_code}).")

    try:
        content = response.json()["content"]
        decoded = base64.b64decode(content).decode("utf-8")
        timestamp = eval(decoded)["timestamp"]
        return timestamp
    except Exception as e:
        raise Exception(f"Failed to parse GitHub API content: {e}")

