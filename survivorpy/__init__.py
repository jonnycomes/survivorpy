from .data import load, refresh_data, get_table_names, get_last_synced
from .config import _CACHE_DIR

# Initialize cache if it's missing or empty
if not _CACHE_DIR.exists() or not any(_CACHE_DIR.iterdir()):
    refresh_data()

TABLE_NAMES = get_table_names()
LAST_SYNCED = get_last_synced()

def __getattr__(name):
    if name in get_table_names():
        return load(name)
    raise AttributeError(
        f"module 'survivorpy' has no attribute '{name}'. "
        f"Available tables: {', '.join(get_table_names())}"
    )

__all__ = ["load", "refresh_data", "TABLE_NAMES", "get_table_names", "LAST_SYNCED", "get_last_synced"] + TABLE_NAMES
