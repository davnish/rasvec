import os
import glob
import tempfile
from pathlib import Path
from rasvec import patchify_raster

def test_patchify_raster():
    base_dir = Path(__file__).parent.parent.parent
    raster_path = os.path.join(base_dir, "docs", "examples", "sample_data", "raster", "ras.tif")
    with tempfile.TemporaryDirectory() as temp_dir:
        patchify_raster(raster_path, temp_dir, 256, padding=True)
        patches = glob.glob(os.path.join(temp_dir, '*.tif'))
        assert len(patches) == 24
