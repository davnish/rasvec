import geopandas as gpd
import rasterio as rio
from rasterio.features import rasterize
import numpy as np

def rasterization(raster_path, vector_path, output_path, classification_column = None):
    """
    Rasterize the vector file and save it as a tiff file.
    If there are multiple classes in the vector file, the classification_column should be provided.

    Args:
        raster_path (str): Raster path.
        vector_path (str): Vector path.
        output_path (str): Output directory path.c
        classification_column (str, optional): column name whose value will be used to burn into the raster. 
        The values in the classification column will be mapped to a continous range. 
        If None, all the geometries will be burned with value 1
    """
    shp = gpd.read_file(vector_path)

    with rio.open(raster_path) as src:
        height = src.height
        width = src.width
        profile = src.profile

    if classification_column is not None:
        map_value = {value: key for key, value in enumerate(shp[classification_column].unique(), 1)}
        shapes = ((geom, map_value(value)) for geom, value in zip(shp.geometry, shp[classification_column]) if geom.is_valid)
    else:
        shapes = ((geom, 1) for geom in shp.geometry if geom.is_valid)


    rasterized = rasterize(shapes, out_shape = (height, width), transform = profile['transform'], fill = 0, dtype = np.uint8)

    meta = {
        'driver': 'GTiff',
        'height': height,
        'width': width,
        'count': 1,
        'dtype': rasterized.dtype,
        'crs': shp.crs,
        'transform': profile['transform']
    }

    with rio.open(output_path, 'w', **meta) as dst:
        dst.write(rasterized, 1)

