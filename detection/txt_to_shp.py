import glob
import os

import geopandas as gpd
import numpy as np
import rasterio as rio
# import tifffile as tiff

from shapely.geometry import box, Point
import pandas as pd

def txt_to_shp(txt_dir, img_dir, shp_dir):
    for i in glob.glob(os.path.join(txt_dir, "*.txt")):
        file_name = os.path.splitext(os.path.basename(i))[0]
        
        with rio.open(os.path.join(img_dir, f"{file_name}.tif")) as src:
            # profile = src.profile
            bounds = src.bounds
            crs = src.crs
            # raster_extent = box(*bounds)
            top_left_corner = (bounds.left, bounds.top)
            bottom_right_corner = (bounds.right, bounds.bottom)
        
        df = pd.read_csv(i, delimiter = " ", names = ['class', 'x', 'y', 'width', 'height'])  

        df['x'] = df['x'] * (bottom_right_corner[0] - top_left_corner[0]) + top_left_corner[0]
        df['y'] = top_left_corner[1] - df['y'] * (top_left_corner[1] - bottom_right_corner[1])

        df['centroid'] = [Point(x, y) for x, y in zip(df.x, df.y)]

        gdf = gpd.GeoDataFrame(geometry = df['centroid'], crs = crs)
        
        # gdf['geometry'] = gdf.geometry.apply(lambda geom: point_to_bbox(geom, buffer_x, buffer_y))
        gdf.to_file(os.path.join(shp_dir, f"{file_name}.shp"), driver="ESRI Shapefile")
    
def concat(shp_dir, output_dir):
    df = None
    for i in glob.glob(os.path.join(shp_dir, "*.shp")):
        df_curr = gpd.read_file(i)
        if df is None:
            df = df_curr
        else:
            df = pd.concat([df, df_curr], ignore_index = True)
            
    gdf = gpd.GeoDataFrame(df)
    gdf.to_file(os.path.join(output_dir, "prediction.shp"), driver="ESRI Shapefile")

if __name__ == "__main__":
    txt_to_shp(rf"results_s/txt/*.txt", rf"coconut_data\image_patched", rf"results_s/shp")
    concat(shp_dir = rf"results_s/shp", output_dir = rf"results_s")