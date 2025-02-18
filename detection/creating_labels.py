import glob
import geopandas as gpd
import os


for file in glob.glob(r"coconut_data\clipped_v2\patched_label\*\*.shp", recursive=True):
    # print(folder)
    gdf = gpd.read_file(file)
    filename = os.path.splitext(os.path.basename(file))[0]
    gdf.drop(columns= 'geometry', inplace = True)
    gdf['class'] = 0    
    gdf = gdf.reindex(columns= ['class', 'distx', 'disty', 'width', 'height'])

    print(file)
    gdf.to_csv(rf'coconut_data\clipped_v2\patched_label_txt\{filename}.txt', index = False, sep=" ", header=None)