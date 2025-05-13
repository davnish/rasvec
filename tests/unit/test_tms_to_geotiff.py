from rasvec import tms_to_geotiff
from pathlib import Path
import tempfile


def test_tms_to_geotiff():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_name = Path(temp_dir, 'output.tiff')
        bbox = [74.347916, 24.287027, 74.355469, 24.293128999999997]
        tms_to_geotiff(output=temp_name, bbox=bbox, zoom=19, source='satellite', overwrite=True, quiet=True)
        assert temp_name.exists()