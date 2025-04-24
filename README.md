# SurvivorPy

**survivorpy** is a Python wrapper of the Survivor data from the R package [survivoR](https://github.com/doehm/survivoR). It enables easy access to clean, structured data on contestants, seasons, episodes, votes, and more from the reality TV show *Survivor*—directly from Python, using familiar `pandas` dataframes.

This package is designed to stay in sync with updates to the original R package, allowing Python users to benefit from ongoing enhancements and new data.

## Installation

Coming soon — the package will be installable via `pip`.

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

The data used in this package is sourced from the [`survivoR`](https://github.com/doehm/survivoR) R package by Daniel Oehm and contributors. The original package is licensed under the MIT License.

We thank the `survivoR` team for making this rich dataset available to the public and for maintaining an up-to-date and comprehensive resource.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

This package redistributes data from the `survivoR` R package, which is also licensed under the MIT License. The original license and attribution from `survivoR` are preserved in accordance with the terms of that license. For more information, see the [survivoR GitHub repository](https://github.com/doehm/survivoR).

## Contributing

Contributions are welcome! Please open an issue or pull request if you'd like to improve the package.

## Disclaimer

This package is not affiliated with or endorsed by CBS, the producers of *Survivor*, or the creators of the original dataset. It is intended for educational, analytical, and research purposes — and definitely not just because it was fun to make.

