# SurvivorPy

SurvivorPy is a Python wrapper of the data from the R package [survivoR](https://github.com/doehm/survivoR). It enables easy access to clean, structured data on contestants, seasons, episodes, votes, and more from the reality show *Survivor*—directly from Python, using familiar `pandas` dataframes.

SurvivorPy syncs its data with survivoR on a weekly basis, ensuring the data reflects recent updates to the survivoR package.

## Installation

Coming soon — the package will be pip installable.

```bash
pip install survivorpy
```

## Usage


```python
from survivorpy import castaways

print(castaways.head())
```

```python
import survivorpy as svr

df_castaways = svr.load("castaways")
df_episodes = svr.load("episodes")
# etc.
```

More usage examples and documentation will be added as the project develops.

## Data Source and Attribution

This package provides Python access to data from the [survivoR](https://github.com/doehm/survivoR) package by Daniel Oehm and contributors. We’re grateful to the folks at survivoR for maintaining such a rich and well-structured dataset.

The original data is licensed under the MIT License, and we preserve that license and attribution in accordance with its terms.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Got ideas or spot a bug? Feel free to open an issue or pull request — contributions of all kinds are welcome!


