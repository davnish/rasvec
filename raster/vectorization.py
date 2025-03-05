import geopandas as gpd
from rasterio import features
import rasterio as rio
import shapely


def vectorization(source, output, simplify_tolerance=None, dst_crs=None, **kwargs):
    """Vectorize a raster dataset.
    Args:
        source (str): The path to the tiff file.
        output (str): The path to the vector file.
        simplify_tolerance (float, optional): The maximum allowed geometry displacement.
        The higher this value, the smaller the number of vertices in the resulting geometry.
    """

    with rio.open(source) as src:
        band = src.read()

        mask = band != 0
        shapes = features.shapes(band, mask=mask, transform=src.transform)

    fc = [
        {"geometry": shapely.geometry.shape(shape), "properties": {"value": value}}
        for shape, value in shapes
    ]
    if simplify_tolerance is not None:
        for i in fc:
            i["geometry"] = i["geometry"].simplify(tolerance=simplify_tolerance)

    gdf = gpd.GeoDataFrame.from_features(fc)
    if src.crs is not None:
        gdf.set_crs(crs=src.crs, inplace=True)

    if dst_crs is not None:
        gdf = gdf.to_crs(dst_crs)

    gdf.to_file(output, **kwargs)