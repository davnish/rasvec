# This file contains the code to create grids accross India occording to our given x and y.
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import shapely
import os


def create_grid(input_path, output_path, grid_size):

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


if __name__ == '__main__':
    # fig, ax = plt.subplots()
    # # boundary.plot(ax = ax)
    # boundary.plot(ax = ax, color = 'red')
    # grid_cells.plot(ax = ax, edgecolor='blue', facecolor = 'none')
    # print(len(grid_cells))
    # # grid_cells.plot(ax = ax, edgecolor='black', facecolor = 'none')
    # plt.show()

    create_grid("/Users/nischal/projects/rasvec/Nagla_Dhanua/mathura_village_boundary.shp",
                "/Users/nischal/projects/rasvec/grid_india/grid_mathura.shp", 500)
    pass