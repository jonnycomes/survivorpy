from .core import load
from .table_names import TABLE_NAMES

def __getattr__(name):
    if name == "castaways":
        return load("castaways")
    if name == "episodes":
        return load("episodes")
    raise AttributeError(f"module 'survivorpy' has no attribute '{name}'")

