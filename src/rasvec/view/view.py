import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.plot import show
import rasterio as rio

def view_rasters(plot_list : list | str, grid : tuple | None = None) -> None:
    """Plots the given list of plots."""

    if isinstance(plot_list, str):
        plot_list = [plot_list]

    if grid:
        row = grid[0]
        col = grid[1]
    else:
        col = len(plot_list)
        row = 1

    fig, ax = plt.subplots(row, col, figsize=(10,10))

    idx = 0
    if row == 1 and col == 1:
        show(rio.open(plot_list[idx]), ax=ax)
        ax.axis('off')
    elif row == 1:
        for x in range(col):
            show(rio.open(plot_list[idx]), ax=ax[x])
            ax[x].axis('off')
            idx += 1
    else:
        for x in range(row):
            for y in range(col):
                show(rio.open(plot_list[idx]), ax=ax[x][y])
                ax[x][y].axis('off')
                idx += 1
    plt.tight_layout()
    plt.show()
    return
