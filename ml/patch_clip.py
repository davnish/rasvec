import geopandas as gpd
import rasterio as rio
# import tifffile as tiff
from patchify import patchify
from shapely.geometry import box, Polygon, Point
import glob
import os
import numpy as np
import math

def patch_save(img_path, save_path_dir, patch_size = 1024):   
    """
    - This function will patchify the images and keep them geotagged
    - This is internally using patchify that's why it will leave the corner pixels
      or part of the image.

    """
    with rio.open(img_path) as src:
        data = src.read().transpose(1,2,0).squeeze()
        # profile = src.profile
        transform = src.transform
        crs = src.crs
    
    filename = os.path.basename(img_path)
    print(img_path)
    # print(data.ndim)

    pad_height = (patch_size - data.shape[0] % patch_size) % patch_size
    pad_width = (patch_size - data.shape[1] % patch_size) % patch_size

    if data.ndim == 3:
        data = np.pad(data, ((0, pad_height), (0, pad_width), (0, 0)), mode='constant')
        patches = patchify(data, (patch_size,patch_size,3), step = patch_size).squeeze()
    else:
        data = np.pad(data, ((0, pad_height), (0, pad_width)), mode='constant')
        patches = patchify(data, (patch_size,patch_size), step = patch_size).squeeze()
        
    
    idx = 0
    for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            patch = patches[i, j]
            
            patch_transform = transform * rio.Affine.translation(j * patch_size, i * patch_size)
            patch_meta = {
                'driver': 'GTiff',
                'height': patch_size,
                'width': patch_size,
                'count': patch.shape[2] if data.ndim == 3 else 1,
                'dtype': patch.dtype,
                'crs': crs,
                'transform': patch_transform
            }
            patch_path = os.path.join(save_path_dir, f"{os.path.splitext(filename)[0]}.{idx}.tif")

            with rio.open(patch_path, 'w', **patch_meta) as dst:
                dst.write(patch.transpose(2, 0, 1) if data.ndim == 3 else patch)
            idx += 1

def clip_vector_by_raster(raster_path, vector_path, output_path):
    with rio.open(raster_path) as src:
        bounds = src.bounds
        raster_extent = box(*bounds)
        top_left_corner = (bounds.left, bounds.top)
        botton_right_corner = (bounds.right, bounds.bottom)

    vector = gpd.read_file(vector_path).to_crs('EPSG:3857')
    clipped_features = []
    distx = []
    disty = []
    width = []
    height = []
    for feature in vector['geometry']:
        try:
            if feature is not None:
                # geom = shape(feature)
                if feature.intersects(raster_extent):
                    clipped_geom = feature.intersection(raster_extent)
                    if isinstance(clipped_geom, Point):
                        clipped_features.append(clipped_geom)
                        # distance = math.sqrt((clipped_geom.x - top_left_corner[0])**2 + (clipped_geom.y - top_left_corner[1])**2)
                        # distances.append(distance)
                        distx.append(abs(clipped_geom.x-top_left_corner[0])/abs(top_left_corner[0] - botton_right_corner[0]))
                        disty.append(abs(clipped_geom.y-top_left_corner[1])/abs(top_left_corner[1] - botton_right_corner[1]))
                        width.append(5/abs(botton_right_corner[0] - top_left_corner[0]))
                        height.append(5/abs(botton_right_corner[1] - top_left_corner[1]))
        except Exception as e: 
            print(e)
            continue
    
    if len(clipped_features) > 0:
        try:
            clipped_gdf = gpd.GeoDataFrame({"distx": distx, "disty": disty, "width": width, "height": height}, geometry=clipped_features, crs='EPSG:3857')
            file_path = os.path.join(output_path, os.path.basename(raster_path))
            clipped_gdf.to_file(file_path, driver='ESRI Shapefile')
        except Exception as e:
            print(clipped_gdf)
            print(e)


def clip_vector(idx):
    shp = gpd.read_file(rf"D:\projects\unet_parcel\data_new\label_raw\{idx}_manualClean.shp").to_crs(3857)
    
    with rio.open(rf"D:\projects\unet_parcel\data_new\images\{idx}.tif") as src:
        bound = src.bounds
        mask = box(bound[0], bound[1], bound[2], bound[3])
        
    shp_new = shp.clip(mask = mask)
    shp_new.to_file(rf"D:\projects\unet_parcel\data_new\label_shp\{idx}.shp", driver = "ESRI Shapefile")

if __name__ == "__main__":
    patch_save(r"Vanathavilluwa_North.tif", r"coconut_data\image_patched", patch_size = 640)
    # for i in glob.glob(r"coconut_data\clipped_v2\patched_data\*.tif"):
        
    #     clip_vector_by_raster(i, r"coconut_data\clipped_v2\label\2.shp", r"coconut_data\clipped_v2\patched_label")