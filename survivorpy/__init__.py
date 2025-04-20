from .core import load

def __getattr__(name):
    if name == "castaways":
        return load("castaways")
    if name == "episodes":
        return load("episodes")
    raise AttributeError(f"module 'survivorpy' has no attribute '{name}'")

