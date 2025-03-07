# This file contains the code to create grids accross India occording to our given x and y.
import geopandas as gpd
# import matplotlib.pyplot as plt
import numpy as np
import shapely
# import os


def create_grid_on_vector(input_path, output_path, grid_size):
    """Creates grid of the given vector.

    Args:
        input_path (str): vector file path.
        output_path (str): output file path.
        grid_size (str): grid size to be created in meters.
    """

    boundary = gpd.read_file(input_path)
    if boundary.crs.to_epsg() != 3857:
        boundary = boundary.to_crs(epsg = 3857)

    xmin, ymin, xmax, ymax = boundary.total_bounds

    grid_cells = []
    for x0 in np.arange(xmin, xmax, grid_size):
        for y0 in np.arange(ymin, ymax, grid_size):
            x1, y1 = x0+grid_size, y0+grid_size
            new_cell = shapely.geometry.box(x0, y0, x1, y1)

            if new_cell.intersects(boundary['geometry'].any()):
                grid_cells.append(new_cell)

    grid_cells = gpd.GeoDataFrame(geometry=grid_cells, crs = boundary.crs)
    grid_cells['grid_no'] = range(len(grid_cells))

    grid_cells.to_file(output_path, driver='ESRI Shapefile')