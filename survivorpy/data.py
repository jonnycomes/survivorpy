import os
import json
import pandas as pd
from .data_store import *
from .config import _CACHE_DATA_DIR, _CACHE_TABLES_NAME_PATH

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
    _cache_table_names()
    tables = get_table_names()
    _cache_data(tables)

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

    local_path = os.path.join(_CACHE_DATA_DIR, f"{table}.parquet")
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

