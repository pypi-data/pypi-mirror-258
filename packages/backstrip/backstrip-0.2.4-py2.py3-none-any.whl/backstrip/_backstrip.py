import itertools as it
import typing

from matplotlib import patches as mpl_patches
from matplotlib import pyplot as plt
import numpy as np

from ._get_bbox_generic import get_bbox_generic


def backstrip(
    ax: typing.Optional[plt.Axes] = None,
    alpha: float = 0.5,
    hue: typing.Optional[typing.Iterable[str]] = None,
    hatch: typing.Optional[typing.Iterable[str]] = None,
    hatch_color: typing.Union[str, typing.Iterable[str]] = "white",
    orient: typing.Literal["v", "h"] = "v",
    **kwargs,
) -> None:
    """Draws background strips behind boxplot patches on a matplotlib Axes
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
    if ax is None:
        ax = plt.gca()

    box_patches = [
        child
        for child in ax.get_children()
        if isinstance(child, mpl_patches.PathPatch)
    ]
    box_patches.sort(
        key=lambda patch: get_bbox_generic(patch).bounds[
            {"v": 0, "h": 1}[orient]
        ],
    )
    ax_width, ax_height = np.ptp(ax.get_xlim()), np.ptp(ax.get_ylim())
    ax_x0, ax_y0 = ax.get_xlim()[0], ax.get_ylim()[0]

    if hue is None:
        hue = [patch.get_facecolor() for patch in box_patches]
    elif isinstance(hue, str):
        hue = [hue]

    if hatch is None:
        hatch = [None for __ in box_patches]
    elif isinstance(hatch, str):
        hatch = [hatch]

    if isinstance(hatch_color, str):
        hatch_color = [hatch_color]

    for patch, facecolor, hatchpattern, hatchcolor in zip(
        box_patches, it.cycle(hue), it.cycle(hatch), it.cycle(hatch_color)
    ):
        bbox = get_bbox_generic(patch)
        bbox_x0, bbox_y0, bbox_width, bbox_height = bbox.bounds
        rect = mpl_patches.Rectangle(
            xy={"v": (bbox_x0, ax_y0), "h": (ax_x0, bbox_y0)}[orient],
            width={"v": bbox_width, "h": ax_width}[orient],
            height={"v": ax_height, "h": bbox_height}[orient],
            alpha=alpha,
            edgecolor=hatchcolor,
            facecolor=facecolor,
            hatch=hatchpattern,
            linewidth=0,
            zorder=-1,
            **kwargs,
        )
        ax.add_patch(rect)
