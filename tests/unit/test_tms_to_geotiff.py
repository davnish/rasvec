import os

from rasvec import tms_to_geotiff


def test_tms_to_geotiff():
    bbox = [-95.3704, 29.6762, -95.368, 29.6775]
    image = "satellite.tif"
    tms_to_geotiff(
        output=image, bbox=bbox, zoom=20, source="Satellite", overwrite=True
    )
    assert os.path.exists(image)