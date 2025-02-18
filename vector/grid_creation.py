# This file contains the code to create grids accross India occording to our given x and y.
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import shapely
import os

india_boundary = gpd.read_file(os.path.join("Administrative Boundary Database", "india_boundary.shp")).to_crs(epsg = 4326)

xmin, ymin, xmax, ymax = india_boundary.total_bounds

stepx, stepy = 10/111, 10/111 #This is create a grid approx 10x10km

grid_cells = []

grids_no = -1

for x0 in np.arange(xmin, xmax+stepx, stepx):
    for y0 in np.arange(ymin, ymax+stepy, stepy):

        x1 = x0+stepx
        y1 = y0+stepy
        new_cell = shapely.geometry.box(x0, y0, x1, y1)

        if new_cell.intersects(india_boundary['geometry'].any()):
            grids_no += 1
            grid_cells.append(new_cell)
        else:
            pass
grid_cells = gpd.GeoDataFrame(grid_cells, columns=['geometry'])
grid_cells.to_file(os.path.join('grid_india', 'grid_10km.shp'), driver='ESRI Shapefile')


if __name__ == '__main__':
    fig, ax = plt.subplots()
    india_boundary.plot(ax = ax)
    india_boundary.plot(ax = ax, color = 'red')
    grid_cells.plot(ax = ax, edgecolor='blue', facecolor = 'none')
    print(len(grid_cells))
    grid_cells.plot(ax = ax, edgecolor='black', facecolor = 'none')
    plt.show()