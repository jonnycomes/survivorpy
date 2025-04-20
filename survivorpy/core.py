import pandas as pd
from pathlib import Path
import requests


_DATA_URL = "https://raw.githubusercontent.com/yourname/survivordata/main/data/" ## Modify later
_LOCAL_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
_VALID_TABLES = {
    "castaways": "castaways.parquet",
    "episodes": "episodes.parquet",
    # Add more later...
}


def load(table: str, refresh: bool = False) -> pd.DataFrame:
    """
    Load a Survivor dataset as a pandas DataFrame.

    Parameters:
        table (str): Name of the table to load (e.g., "castaways")

    Returns:
        pd.DataFrame: The requested dataset.
    """
    if table not in _VALID_TABLES:
        raise ValueError(f"Unknown table: '{table}'. Choose from: {list(_VALID_TABLES)}")

    fname = f"{table}.parquet"
    local_path = _LOCAL_DATA_DIR / fname

    if refresh or not local_path.exists():
        _LOCAL_DATA_DIR.mkdir(exist_ok=True)
        url = _DATA_URL + fname
        r = requests.get(url)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(r.content)

    return pd.read_parquet(local_path)