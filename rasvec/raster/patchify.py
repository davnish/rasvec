import rasterio as rio
from patchify import patchify
import os
import numpy as np

def patchify_raster(raster_path, output_path, patch_size = 1024, padding=True):   
    """
    This function will patchify the images and keep them geotagged.

    Args:
        raster_path (str):          Raster's Path.
        output_path (_type_):     Directory's Path, where to save all the patched images.
        patch_size (int, optional): size of every path, 
                                    every patch will be of size (patch_size x patch_size). Defaults to 1024.
        padding (bool, optional):   If padding is set to true, a padding of 0 will be done at the corner patches,
                                    which are not multiples of (patch_sizexpatch_size).
    """
    with rio.open(raster_path) as src:
        data = src.read().transpose(1,2,0).squeeze()
        # profile = src.profile
        transform = src.transform
        crs = src.crs
    
    filename = os.path.basename(raster_path)

    if padding:
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
            patch_path = os.path.join(output_path, f"{os.path.splitext(filename)[0]}.{idx}.tif")

            with rio.open(patch_path, 'w', **patch_meta) as dst:
                dst.write(patch.transpose(2, 0, 1) if data.ndim == 3 else patch)
            idx += 1

    print(f"Saved the patched files in output dir: {output_path}")
            