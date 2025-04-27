from pathlib import Path
from appdirs import user_cache_dir

_CACHE_DIR = Path(user_cache_dir("survivorpy", "jonnycomes"))
_CACHE_DATA_DIR = _CACHE_DIR / "tables"
_CACHE_TABLE_NAMES_PATH = _CACHE_DIR / "table_names.json"
_CACHE_LAST_SYNCED_PATH = _CACHE_DIR / "last_synced.json"

_S3_BUCKET = "survivorpy-data"
_S3_TABLE_NAMES_KEY = "metadata/table_names.json"

def has_cache():
    """
    Checks if the cache is properly set up by ensuring that the cache
    directory and its necessary files and subdirectories exist and are non-empty.

    Specifically, it checks:
    - The existence of the main cache directory.
    - The existence of the 'tables' subdirectory.
    - The existence of the 'table_names.json' and 'last_synced.json' files.

    Returns:
        bool: True if the cache is fully set up (all directories and files exist and are non-empty),
              False otherwise.
    """
    if not _CACHE_DIR.exists() or not _CACHE_DIR.is_dir():
        return False

    if not _CACHE_DATA_DIR.exists() or not _CACHE_DATA_DIR.is_dir() or not any(_CACHE_DATA_DIR.iterdir()):
        return False

    if not _CACHE_TABLE_NAMES_PATH.exists() or not _CACHE_TABLE_NAMES_PATH.is_file():
        return False

    if not _CACHE_LAST_SYNCED_PATH.exists() or not _CACHE_LAST_SYNCED_PATH.is_file():
        return False

    return True
