import os
import rasterio as rio
import geopandas as gpd
from shapely import box

def clip_vector_by_raster(raster_path, vector_path, output_path):
    """
    This function clips the vector file given the raster's extent.

    Note:
    The given raster's crs should be "3857".

    Args:
        raster_path (str): Raster's path
        vector_path (str): Vector's path
        output_path (str): Output_path directory filepath, the filename is carried from the given vector's name
    """
    shp = gpd.read_file(vector_path).to_crs(3857)
    filename = os.path.basename(vector_path)
    
    with rio.open(raster_path) as src:
        bound = src.bounds
        mask = box(bound[0], bound[1], bound[2], bound[3])
        
    shp_new = shp.clip(mask = mask)
    output_path_filename = os.path.join(output_path, filename)
    shp_new.to_file(output_path_filename, driver = "ESRI Shapefile")

# def clip_vector_by_raster(raster_path, vector_path, output_path):
#     with rio.open(raster_path) as src:
#         bounds = src.bounds
#         raster_extent = box(*bounds)
#         top_left_corner = (bounds.left, bounds.top)
#         botton_right_corner = (bounds.right, bounds.bottom)

#     vector = gpd.read_file(vector_path).to_crs('EPSG:3857')
#     clipped_features = []
#     distx = []
#     disty = []
#     width = []
#     height = []
#     for feature in vector['geometry']:
#         try:
#             if feature is not None:
#                 # geom = shape(feature)
#                 if feature.intersects(raster_extent):
#                     clipped_geom = feature.intersection(raster_extent)
#                     if isinstance(clipped_geom, Point):
#                         clipped_features.append(clipped_geom)
#                         # distance = math.sqrt((clipped_geom.x - top_left_corner[0])**2 + (clipped_geom.y - top_left_corner[1])**2)
#                         # distances.append(distance)
#                         distx.append(abs(clipped_geom.x-top_left_corner[0])/abs(top_left_corner[0] - botton_right_corner[0]))
#                         disty.append(abs(clipped_geom.y-top_left_corner[1])/abs(top_left_corner[1] - botton_right_corner[1]))
#                         width.append(5/abs(botton_right_corner[0] - top_left_corner[0]))
#                         height.append(5/abs(botton_right_corner[1] - top_left_corner[1]))
#         except Exception as e: 
#             print(e)
#             continue
    
#     if len(clipped_features) > 0:
#         try:
#             clipped_gdf = gpd.GeoDataFrame({"distx": distx, "disty": disty, "width": width, "height": height}, geometry=clipped_features, crs='EPSG:3857')
#             file_path = os.path.join(output_path, os.path.basename(raster_path))
#             clipped_gdf.to_file(file_path, driver='ESRI Shapefile')
#         except Exception as e:
#             print(clipped_gdf)
#             print(e)