from pathlib import Path
from .data import load, refresh_data, get_table_names
from .config import _CACHE_DIR

# Initialize cache if it's missing or empty
if not Path(_CACHE_DIR).exists() or not any(Path(_CACHE_DIR).iterdir()):
    refresh_data()

def __getattr__(name):
    if name == "TABLE_NAMES":
        return get_table_names()
    if name in get_table_names():
        return load(name)
    raise AttributeError(
        f"module 'survivorpy' has no attribute '{name}'. "
        f"Available tables: {', '.join(get_table_names())}"
    )
