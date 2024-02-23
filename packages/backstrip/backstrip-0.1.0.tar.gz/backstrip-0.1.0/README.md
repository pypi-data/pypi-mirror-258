[
![PyPi](https://img.shields.io/pypi/v/backstrip.svg?)
](https://pypi.python.org/pypi/backstrip)
[
![CI](https://github.com/mmore500/backstrip/actions/workflows/ci.yaml/badge.svg)
](https://github.com/mmore500/backstrip/actions)
[
![GitHub stars](https://img.shields.io/github/stars/mmore500/backstrip.svg?style=round-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/backstrip)

*backstrip* adds color-coordinated fill behind matplotlib boxplots

- Free software: MIT license
- Repository: <https://github.com/mmore500/backstrip>

## Install

`python3 -m pip install backstrip`

## Example Usage

```python3
from backstrip import backstrip
from matplotlib import pyplot as plt
import seaborn as sns

titanic = sns.load_dataset("titanic")
ax = sns.boxplot(data=titanic, x="class", y="age", hue="alive")
backstrip(ax)

plt.show()
```

![example](docs/assets/test_backstrip_hatching.png)


## API

```python3
def backstrip(
    ax: plt.Axes,
    alpha: float = 0.5,
    hue: typing.Optional[typing.Iterable[str]] = None,
    hatch: typing.Optional[typing.Iterable[str]] = None,
    hatch_color: typing.Union[str, typing.Iterable[str]] = "white",
    orient: str = "v",
    **kwargs,
) -> None:
"""
Draws background strips behind boxplot patches on a matplotlib Axes
object to enhance the visual identifiability of hue-keyed groups.

This function iterates over PathPatch objects (representing boxes) within a
matplotlib Axes, and draws semi-transparent rectangles (strips) in the
background.

These strips can be customized in color (`hue`), pattern (`hatch`), and
orientation (`orient`).

Parameters
----------
ax : plt.Axes
    The matplotlib Axes object on which to draw the backstrips.
  alpha : float, default 0.5
    The opacity level of the backstrips.
  hue : Union[None, str, Iterable[str]], optional
    The color(s) for the backstrips.

    Can be a single color or a sequence of colors. If `None`, the colors of
    the box objects in the Axes are matched.
  hatch : Union[None, str, Iterable[str]], default None
    The hatch pattern(s) for the backstrips.

    Can be a single pattern or a sequence of patterns. If `None`, no
    hatch patterns are applied.
  hatch_color : Union[str, Iterable[str]], default 'white'
    The color of hatch patterns, if applied.
  orient : str, default 'v'
    The orientation of the backstrips. Can be 'v' for vertical or 'h' for
    horizontal.
  kwargs : dict
    Additional keyword arguments to pass to the `Rectangle` patches.

Returns
-------
None
"""
```
