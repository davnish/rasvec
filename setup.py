from setuptools import  setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="rasvec",
    version="0.0.8",
    description="A python library to ease the of the handling geospatial data.",
    author="Nischal Singh",
    author_email="nischal.singh38@gmail.com",
    url="https://github.com/davnish/rasvec.git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "rasvec"},
    packages=find_packages(where="rasvec"),
    install_requires=[
        "geopandas>=0.8.0",
        "rasterio>=1.3.10",
        "patchify>=0.2.3"
        ],
    setup_reqires=['wheel'],
    python_requires=">=3.9",
    license="MIT",
)