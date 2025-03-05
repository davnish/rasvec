from setuptools import  setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="rasvec",
    version="0.0.1",
    description="",
    author="Nischal Singh",
    author_email="nischal.singh38@gmail.com",
    url="https://github.com/davnish/rasvec.git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"", "rasvec"},
    packages=find_packages(where="rasvec"),
    install_requires=[
        "rasterio >= 1.3.10",
        "geopandas >= 1.0.1",
        "patchify >= 0.2.3"
        ],
    python_requires = ">=3.11",
    license="MIT",
)