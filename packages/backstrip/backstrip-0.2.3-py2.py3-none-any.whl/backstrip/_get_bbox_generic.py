import matplotlib as mpl


# https://stackoverflow.com/q/31148401/17332200
def get_bbox_generic(obj) -> mpl.transforms.Bbox:
    fig, ax = obj.figure, obj.axes
    disp = obj.get_window_extent(renderer=fig.canvas.get_renderer())
    return disp.transformed(ax.transData.inverted())
