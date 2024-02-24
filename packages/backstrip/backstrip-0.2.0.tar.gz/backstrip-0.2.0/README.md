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
ax = sns.boxplot(data=titanic, x="age", y="class", hue="alive", orient="h")
backstrip(ax, hatch=["oo", "xx"], orient="h")

plt.show()
```

![example](docs/assets/test_backstrip_hatching.png)

---

```python3
from backstrip import backplot
from matplotlib import pyplot as plt
import seaborn as sns

g = backplot(
    data=sns.load_dataset("titanic"),
    x="class",
    y="age",
    hue="alive",
    col="who",
    style="alone",  # hatches by this column
)

plt.show()
```

![example](docs/assets/test_backplot_v_facet.png)

## API

### `backstrip`: direct, axes-level interface

```python3
def backstrip(
    ax: plt.Axes,
    alpha: float = 0.5,
    hue: typing.Optional[typing.Iterable[str]] = None,
    hatch: typing.Optional[typing.Iterable[str]] = None,
    hatch_color: typing.Union[str, typing.Iterable[str]] = "white",
    orient: typing.Literal["v", "h"] = "v",
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
  orient : Literal['v', 'h'], default 'v'
    The orientation of the backstrips.

    Should match orientation of boxplot. Can be 'v' for vertical or 'h' for
    horizontal.
  kwargs : dict
    Additional keyword arguments to pass to the `Rectangle` patches.

Returns
-------
None
"""
```

### `backplot`: tidy-data, figure-level interface

```python3
def backplot(
    data: pd.DataFrame,
    x: typing.Optional[str] = None,
    y: typing.Optional[str] = None,
    hue: typing.Optional[str] = None,
    style: typing.Optional[str] = None,
    col: typing.Optional[str] = None,
    row: typing.Optional[str] = None,
    order: typing.Optional[typing.Sequence[str]] = None,
    hue_order: typing.Optional[typing.Sequence[str]] = None,
    style_order: typing.Optional[typing.Sequence[str]] = None,
    hatches: typing.Optional[typing.Sequence[str]] = None,
    orient: typing.Literal["v", "h"] = "v",
    palette: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
    backstrip_kws: dict = frozendict(),
    legend_width_inches: float = 1.5,
    legend_kws: dict = frozendict(),
    **kwargs: dict,
) -> sns.FacetGrid:
    """Create a composite plot that combines boxplots with backstrips,
    optionally hatched according to a categorical style variable.

    Provides a tidy-data, seaborn-like interface for backstrip elements. Unlike
    backstrip, this function uses the seaborn.catplot interface to create
    boxplots (and then applies backstrips to the resulting axes).

    Parameters
    ----------
    data : pd.DataFrame
        The input dataset, where each row is an observation and each column is a feature.
    x : Optional[str], optional
        The name of the column in `data` to be plotted on the x-axis.
    y : Optional[str], optional
        The name of the column in `data` to be plotted on the y-axis.
    hue : Optional[str], optional
        The name of the column in `data` to assign boxplot colors.

        Backstrip colors are matched to the boxplot colors.
    style : Optional[str], optional
        The name of the column in `data` to assign backstrip hatch patterns.
    col : Optional[str], optional
        Variable in `data` for facet wrapping the columns.
    row : Optional[str], optional
        Variable in `data` for facet wrapping the rows.
    order : Optional[Sequence[str]], optional
        The order to plot the x or y categorical levels in.

        If None, order is assigned arbitrarily.
    hue_order : Optional[Sequence[str]], optional
        The order to assign hue levels with palette colors.

        If None, order is assigned arbitrarily.
    style_order : Optional[Sequence[str]], optional
        The order to assign style levels with hatch patterns.

        If None, order is assigned arbitrarily.
    hatches : Optional[Sequence[str]], optional
        A sequence of hatch patterns to use for the styles.

        If None, an arbitrary sequence of hatch patterns is used.
    orient : {'v', 'h'}, default 'v'
        Orientation of the plot (vertical or horizontal).
    palette : Optional[Union[str, Sequence[str]]], optional
        Colors to use for the different levels of the `hue` variable.

        If None, the default seaborn color palette is used.
    backstrip_kws : dict, default dict()
        Additional keyword arguments for the backstrip function.
    legend_width_inches : float, default 1.5
        The width of the legend in inches.

        Overridden by any passed `legend_kws` options.
    legend_kws : dict, default dict()
        Additional keyword arguments for the legend.
    **kwargs : dict
        Additional keyword arguments passed to `sns.catplot`.

    Returns
    -------
    sns.FacetGrid
        A FacetGrid object which is the figure-level container for the plots.

    Notes
    -----
    If boxplot strips contain more than one style column value, they will be
    hatched with both (or all) corresponding hatch patterns.
    """
```
