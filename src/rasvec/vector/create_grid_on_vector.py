from typing import Union
import numpy as np
import geopandas as gpd
from shapely import box
from ensure import ensure_annotations
from pathlib import Path


@ensure_annotations
def create_grid_on_vector(input_path : str, grid_size : Union[float,int], output_path: Union[str, None] = None) -> gpd.GeoDataFrame:
    """Creates a grid over the entire vector file.

    Args:
        input_path (str): Path to the vector file.
        grid_size (Union[float, int]): Grid cell size in meters.
        output_path (Union[str, None], optional): Path for the output grid file. If given will save the grid to the output path. Defaults to None.
    
    Returns:
        gpd.GeoDataFrame: GeoDataFrame of the grid cells.
    """

    input_path = Path(input_path)
    output_path = Path(output_path)

    boundary = gpd.read_file(input_path)
    boundary_crs = boundary.crs

    if boundary.crs is not None and boundary.crs.to_epsg() != 3857:
        boundary = boundary.to_crs(epsg=3857)

    boundary_union = boundary.union_all()
    xmin, ymin, xmax, ymax = boundary_union.bounds

    grid_cells = []
    for x0 in np.arange(xmin, xmax, grid_size):
        for y0 in np.arange(ymin, ymax, grid_size):
            x1, y1 = x0 + grid_size, y0 + grid_size
            new_cell = box(x0, y0, x1, y1)

            if new_cell.intersects(boundary_union):
                grid_cells.append(new_cell)

    grid_cells = gpd.GeoDataFrame(geometry=grid_cells, crs=boundary.crs).to_crs(boundary_crs)
    grid_cells["grid_no"] = range(len(grid_cells))

    if output_path:
        grid_cells.to_file(output_path, driver="ESRI Shapefile")
    
    return grid_cells
