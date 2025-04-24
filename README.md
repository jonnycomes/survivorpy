# SurvivorPy

SurvivorPy is a Python wrapper of the data from the R package [survivoR](https://github.com/doehm/survivoR). It enables Python coders easy access to clean, structured data on contestants, seasons, episodes, votes, and more from the reality show *Survivor*—directly from Python, using familiar `pandas` dataframes.

SurvivorPy syncs its data with survivoR on a weekly basis, ensuring the data reflects recent updates to the survivoR package.

## Installation

Coming soon — the package will be pip installable.

```bash
pip install survivorpy
```

## Usage

There are a few different ways to access Survivor data with `survivorpy`, depending on your preferences and needs. In all cases, the tables are provided as `pandas` DataFrames.

### Import a table directly

If you know the name of the table you want, you can import it directly:

```python
from survivorpy import castaways

castaways.head()
```

### See all available tables
To see what's available, use the `TABLE_NAMES` constant:

```python
from survivorpy import TABLE_NAMES

print(TABLE_NAMES)
# [..., 'castaways', ...]
```

### Using the `load()` function
`survivorpy` provides a `load()` function which gives an alternative way to access the tables:

```python
import survivorpy as sv

df = sv.load('castaways')
df.head()
```

By default, survivorpy caches tables locally after the first download. To fetch the latest version from the source (kept in sync weekly with the survivoR package), use the `refresh` tag:

```python
df = sv.load('castaways', refresh=True)
```

No matter which method you choose, you’ll get rich Survivor data, neatly packaged and ready to explore with your favorite `pandas` tools.

## Data Source and Attribution

This package provides Python access to data from the [survivoR](https://github.com/doehm/survivoR) package by Daniel Oehm and contributors. We’re grateful to the folks at survivoR for maintaining such a rich and well-structured dataset.

The original data is licensed under the MIT License, and we preserve that license and attribution in accordance with its terms.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Got ideas or spot a bug? Feel free to open an issue or pull request — contributions of all kinds are welcome!


