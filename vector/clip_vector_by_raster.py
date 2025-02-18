import geopandas as gpd
import rasterio as rio
import os
from shapely.geometry import box, Polygon


def clip_vector_by_raster(raster_path, vector_path, output_path):
    filename = os.path.basename(raster_path).split('.')[0]
    with rio.open(raster_path) as src:
        bounds = src.bounds
        raster_extent = box(*bounds)

    vector = gpd.read_file(vector_path).to_crs('EPSG:3857')

    clipped_vec = vector.clip(mask = raster_extent)
    clipped_vec.to_file(os.path.join(clipped_vec, f'{filename}.shp'), driver = "ESRI Shapefile")