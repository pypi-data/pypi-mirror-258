import itertools as it
import typing

from frozendict import frozendict
from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt
import opytional as opyt
import pandas as pd
import seaborn as sns

from ._backstrip import backstrip


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
        The input dataset, where each row is an observation and each column is
        a feature.
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
    # PART 1: initialize argument defaults
    ###########################################################################
    if order is None:
        position = {"v": x, "h": y}[orient]
        if position is not None:
            order = sorted(data[position].unique())

    if hue_order is None and hue is not None:
        hue_order = sorted(data[hue].unique())

    if style_order is None and style is not None:
        style_order = sorted(data[style].unique())

    if hatches is None and style is not None:
        hatch_cycle = it.cycle(
            ["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]
        )
        hatches = [*it.islice(hatch_cycle, len(style_order))]

    if palette is None:
        # silence seaborn warning about palette length
        palette = sns.color_palette("tab10")[: len(hue_order or [])]

    # PART 2: draw boxplots
    ###########################################################################
    g = sns.catplot(
        data=data,
        x=x,
        y=y,
        row=row,
        col=col,
        hue=hue,
        order=order,
        hue_order=hue_order,
        **{
            "kind": "box",
            "legend_out": True,
            **({"palette": palette} if hue is not None else {}),
            **kwargs,
        },
    )

    # PART 3: draw backstrips
    ###########################################################################
    g.map_dataframe(
        _apply_backstrip,
        x={"v": x, "h": None}[orient],
        y={"v": None, "h": y}[orient],
        hue=hue,
        style=style,
        order=order,
        hue_order=hue_order,
        style_order=style_order,
        hatches=hatches,
        orient=orient,
        **backstrip_kws,
    )

    # PART 4: set up legend
    ###########################################################################
    if g._legend is not None and style is not None:
        if hue == style:
            legend_patches = _make_legend_patches(
                title=hue,
                labels=hue_order,
                palette=palette,
                hatch_styles=[
                    hatches[style_order.index(s)] for s in style_order
                ],
            )
        else:
            legend_patches = [
                *_make_legend_patches(
                    title=hue, labels=hue_order, palette=palette
                ),
                *_make_legend_patches(
                    title=style, labels=style_order, hatch_styles=hatches
                ),
            ]

        figwidth = g.figure.get_figwidth()
        figfrac = max(0.33, (figwidth - legend_width_inches) / figwidth)

        # can't use move_legend to add handles/labels
        # see https://github.com/mwaskom/seaborn/pull/3454
        g._legend.set_visible(False)
        g._legend = plt.legend(
            handles=legend_patches,
            labels=[patch.get_label() for patch in legend_patches],
            frameon=False,
        )
        sns.move_legend(
            obj=g,
            title=None,
            **{
                "loc": "center left",
                "bbox_to_anchor": (figfrac, 0.5),
                "handleheight": 3,
                "handlelength": 5,
                **legend_kws,
            },
        )
        g.figure.subplots_adjust(right=figfrac)

    return g


def _apply_backstrip(
    data: pd.DataFrame,
    x: typing.Optional[str] = None,
    y: typing.Optional[str] = None,
    hue: typing.Optional[str] = None,
    style: typing.Optional[str] = None,
    order: typing.Optional[typing.Sequence[str]] = None,
    hue_order: typing.Optional[typing.Sequence[str]] = None,
    style_order: typing.Optional[typing.Sequence[str]] = None,
    hatches: typing.Optional[typing.Sequence[str]] = None,
    orient: typing.Literal["v", "h"] = "v",
    **kwargs: dict,
) -> None:
    """Internal helper function to map backstrip application over a seaborn
    FacetGrid.

    Calculates hatch styles for each group and applies backstrip to the current
    axes.

    Parameters
    ----------
    data : pd.DataFrame
        The input dataset with observations and features.
    x : Optional[str], optional
        Column name for the x-axis variable.
    y : Optional[str], optional
        Column name for the y-axis variable.
    hue : Optional[str], optional
        Variable for color encoding.
    style : Optional[str], optional
        Variable for style encoding, which will determine the hatch pattern.
    order : Optional[Sequence[str]], optional
        Order to plot the x or y variable levels.

        Ensures that backstrip hatches are applied in correct order.
    hue_order : Optional[Sequence[str]], optional
        Order to plot the hue variable levels.

        Ensures that backstrip hatches are applied in correct order.
    style_order : Optional[Sequence[str]], optional
        Order to plot the style variable levels.

        Ensures that backstrip hatches are applied in correct order.
    hatches : Optional[Sequence[str]], optional
        Sequence of hatch patterns for the styles.
    orient : {'v', 'h'}, default 'v'
        Orientation of the boxplot strips, either 'v' for vertical or 'h' for
        horizontal.
    **kwargs : dict
        Additional keyword arguments to be passed to the backstrip function.
    """
    if orient == "v":
        assert y is None
    elif orient == "h":
        assert x is None

    keys = [var for var in [x, y, hue] if var is not None]
    if len(keys) == 1:
        keys = keys[0]  # silence pandas warning about single-item tuple
    groups = data.groupby(keys) if keys else [(None, data)]
    lookup = {k if isinstance(k, tuple) else (k,): v for k, v in groups}

    if style is not None:
        hatch_styles = []
        for key in (
            it.product(
                *(var for var in [order, hue_order] if var is not None),
            )
            if keys
            else [(None,)]
        ):
            try:
                group = lookup[key]
            except KeyError:
                continue

            hatch_style = "".join(
                hatches[style_order.index(s)]
                for s in group[style].unique()
                if s is not None and s in style_order
            )
            hatch_styles.append(hatch_style)

        if not hatch_styles:
            hatch_styles = None
    else:
        hatch_styles = None

    kwargs.pop("color", None)  # color from kwargs interferes, want box colors
    backstrip(
        ax=plt.gca(),
        hatch=hatch_styles,
        orient=orient,
        **kwargs,
    )


def _make_legend_patches(
    title: typing.Optional[str],
    labels: typing.Sequence[str],
    palette: typing.Optional[typing.Sequence[str]] = None,
    hatch_styles: typing.Optional[typing.Sequence[str]] = None,
) -> typing.List[mpl_patches.Patch]:
    """Internal helper function to create legend patches.

    Called separately for hue and style (hatching) elements if they are mapped
    to different variables or once for both if mapped to the same variable.

    Parameters
    ----------
    title : Optional[str]
        Title for the legend group.

        If provided, it creates a legend title patch.
    labels : Sequence[str]
        Text labels for each non-title patch.
    palette : Optional[Sequence[str]], default=None
        Color palette for the patches.

        If not provided, defaults to 'none' (transparent).
    hatch_styles : Optional[Sequence[str]], default=None
        Hatch patterns for each patch.

        If not provided, patches will have no hatch.

    Returns
    -------
    List[mpl_patches.Patch]
        A list of matplotlib patch objects that can be used to create a custom
        legend.
    """
    handles = []

    if title is not None:
        handles.append(
            mpl_patches.Patch(facecolor="none", edgecolor="none", label=title),
        )

    handles.extend(
        mpl_patches.Patch(
            facecolor=color,
            edgecolor="black",
            label=label,
            hatch=hatch,
        )
        for label, color, hatch in zip(
            opyt.or_value(labels, tuple()),
            opyt.or_value(palette, it.repeat("none")),
            opyt.or_value(hatch_styles, it.repeat(None)),
        )
    )
    if palette is not None:
        for handle in handles:
            handle._hatch_color = (1, 1, 1, 1)

    return handles
