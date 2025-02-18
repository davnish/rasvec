import os
import glob
import shutil
# import platform
# from tqdm import tqdm
import numpy as np
from shapely.geometry import box, Polygon
# import rasterio as rio
# import fiona
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from PIL import Image



# path = os.path.join(r'vectors', '*.shp')

# vectors = sorted([int(os.path.basename(i).split('.')[0].split('_')[0]) for i in glob.glob(path)])

# desktops = {'AH-Nichal-Singh': [vectors[0], vectors[-1]]}

# grid_range = desktops[platform.node()]



def copy_from_nas(district_name):
    """
    This function will copy all the files from nas(Z:) to local
    - This function will also make the folder for the district if its not there
    - This function will only copy the files to the local which are in the range given in `grid_range` list.
    - If the folder already exists it will only copy the files which needs to be copied.
    """
    print(f'Starting range from: {grid_range}')
    print('Starting CP files from NAS to local')
    local_path = os.path.join(district_name)
    if os.path.exists(local_path) == 0:
        os.mkdir(district_name)
        os.mkdir(os.path.join(local_path, 'images'))
        os.mkdir(os.path.join(local_path, 'masks'))
        os.mkdir(os.path.join(local_path, 'vectors'))

    # Calculating the grids which needs to be copied
    local_list = np.asarray(get_list(district_name, of = 'images', drive = 'D'))
    local_list = local_list[(grid_range[0] <= local_list) & (local_list <= grid_range[1])]

    nas_list = np.asarray(get_list(district_name, of = 'images', drive = 'Z'))
    nas_list = nas_list[(grid_range[0] <= nas_list) & (nas_list <= grid_range[1])]
    diff = calculate_diff(nas_list, local_list)

    nas_cp_path = os.path.join('Z:', f'{district_name}', 'images')
    local_images_path = os.path.join(local_path, 'images')
    
    for i in diff:
        img_nas_cp_path = os.path.join(nas_cp_path, f'{i}.tif')
        img_to_cp_path = os.path.join(local_images_path, f'{i}.tif')
        if os.path.exists(img_nas_cp_path):
            print(f'Transferring img: {i}')
            shutil.copy(img_nas_cp_path, img_to_cp_path)
    print('Done Copying')

def find_mx_grid_idx(path):
    mx_grid_idx = 0
    for i in glob.glob(os.path.join(path, '*')):
        grid_idx = int(i.split('\\')[-1].split('.')[-2]) # Here taking '/' can be a problem for windows as windows uses '\\' 
        if grid_idx > mx_grid_idx:
            mx_grid_idx = grid_idx
    
    return mx_grid_idx

def get_list(district_name, of = 'images', drive = 'D'):
    path = os.path.join(f'{drive}:', district_name, f'{of}')
    district_list = [int(p.split('.')[0]) for p in os.listdir(path) if os.path.splitext(p)[1] in ['.tif']]
    return sorted(district_list)

def marked_list(district_name):
    vec_list = get_list(district_name, of = 'vectors')
    return vec_list
# net use z: \\Azure_Noida\Deepak_Kushwaha
def get_ranges(arr):
    '''
    This Function find the continous ranges in an array and return it in a vector
    '''
    # arr = get_list(district_name, of = 'images')
    rge = []

    i = 0
    for j in range(1, len(arr)):
        if arr[j] !=  arr[j-1] + 1:
            rge.append([arr[i], arr[j-1]])
            i = j
        
        if j == len(arr)-1:
            rge.append([arr[i], arr[j]])
    return rge

def calculate_diff(images_arr, vectors_arr):
    j = 0
    diff_arr = []
    if(len(vectors_arr) == 0): return images_arr # If the second array is empty

    for i in range(len(images_arr)):
        if images_arr[i] == vectors_arr[j]:
            j += 1
        else:
            diff_arr.append(images_arr[i])
        if j>=len(vectors_arr) : 
            diff_arr.extend(images_arr[i+1:])
            break

    return diff_arr

def get_leftover(district_name):
    images_arr = get_list(district_name, of = 'images')
    vectors_arr = get_list(district_name, of = 'vectors')
    # return get_ranges(calculate_diff(images_arr, vectors_arr))
    return calculate_diff(images_arr, vectors_arr)

def cp_nas_leftover(district_name):
    left = get_leftover(district_name)
    nas_cp_path = os.path.join('Z:', f'{district_name}', 'vectors')
    local_path = os.path.join(district_name, 'vectors')
    for vec in left:
        print(f'Copying {vec}')
        shutil.copy(os.path.join(local_path, f'{vec}.tif'), os.path.join(nas_cp_path, f'{vec}.tif'))

def clip_vector_by_raster(raster_path, vector_path, output_path):
    with rasterio.open(raster_path) as src:
        bounds = src.bounds
        raster_extent = box(*bounds)

    vector = gpd.read_file(vector_path).to_crs('EPSG:3857')
    clipped_features = []

    for feature in vector['geometry']:
        try:
            if feature is not None:
                # geom = shape(feature)
                if feature.intersects(raster_extent):
                    clipped_geom = feature.intersection(raster_extent)
                    if isinstance(clipped_geom, Polygon):
                        clipped_features.append(clipped_geom)
        except Exception as e: 
            print(e)
            continue
    
    try:
        clipped_gdf = gpd.GeoDataFrame(geometry=clipped_features, crs='EPSG:3857')
        clipped_gdf.to_file(output_path, driver='ESRI Shapefile')
    except Exception as e:
        print(clipped_gdf)
        print(e)



if __name__ == "__main__":

    raster_path = r"data_raw\Koilwar_1.tif"
    vector_path = r"data_raw\vector\Koilwar_Build.shp"
    output_path = r"data_raw\vector\clipped\Koilwar_Build.shp"

    # clip_vector_by_raster(raster_path, vector_path, output_path)
    data_raw\patched