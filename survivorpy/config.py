from pathlib import Path
from appdirs import user_cache_dir

_CACHE_DIR = Path(user_cache_dir("survivorpy", "jonnycomes"))
_CACHE_DATA_DIR = _CACHE_DIR / "tables"
_CACHE_TABLE_NAME_PATH = _CACHE_DIR / "table_names.json"

_S3_BUCKET = "survivorpy-data"
_S3_TABLE_NAMES_KEY = "metadata/table_names.json"