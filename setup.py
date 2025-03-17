from setuptools import  setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="rasvec",
    version="0.1.0",
    description="A python library to ease the of the handling geospatial data.",
    author="Nischal Singh",
    author_email="nischal.singh38@gmail.com",
    url="https://github.com/davnish/rasvec.git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "geopandas>=1.0.1",
        "rasterio>=1.4.3",
        "patchify>=0.2.3",
        "pillow>=11.1.0",
        "xyzservices>=2025.1.0",
        ],
    # setup_reqires=['wheel'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)