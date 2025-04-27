from .data import load, refresh_data, get_table_names, get_last_synced
from .config import has_cache

# Refresh the data if cache is not set up
if not has_cache():
    refresh_data()

# Fetch key attributes for module access
TABLE_NAMES = get_table_names()
LAST_SYNCED = get_last_synced()

# Define the public API
__all__ = ["load", 
           "refresh_data", 
           "TABLE_NAMES", "get_table_names", 
           "LAST_SYNCED", "get_last_synced", 
           "has_cache"
           ] + TABLE_NAMES

def __getattr__(name):
    """
    Dynamically load tables when accessed as attributes.
    Raises AttributeError if the table name is not found.
    """
    if name in get_table_names():
        return load(name)
    raise AttributeError(
        f"module 'survivorpy' has no attribute '{name}'. "
        f"Available tables: {', '.join(get_table_names())}"
    )
