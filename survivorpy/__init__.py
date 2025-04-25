from .data import load, _load_table_names

TABLE_NAMES = _load_table_names()

def __getattr__(name):
    if name in TABLE_NAMES:
        return load(name)
    raise AttributeError(f"module 'survivorpy' has no attribute '{name}'")
