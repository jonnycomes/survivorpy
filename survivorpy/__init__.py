from .core import load
from .table_names import TABLE_NAMES

def __getattr__(name):
    if name in TABLE_NAMES:
        return load(name)
    raise AttributeError(f"module 'survivorpy' has no attribute '{name}'")

