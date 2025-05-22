import os
import tempfile
from pathlib import Path
from rasvec import grid_vector

def test_grid_vector():
    base_dir = Path(__file__).parent.parent.parent
    vector_file_path = os.path.join(base_dir, "docs", "examples", "sample_data", "vector", "vec", "vec.shp")
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file_path = os.path.join(temp_dir, "grid.shp")
        grid_cells = grid_vector(vector_file_path, 1000, output_file_path)
        assert len(grid_cells) == 81 and os.path.exists(output_file_path)
    