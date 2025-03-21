from setuptools import  setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="rasvec",
    version="0.1.0",
    description="A Geospatial data handling library.",
    author="Nischal Singh",
    author_email="nischal.singh38@gmail.com",
    url="https://github.com/davnish/rasvec.git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "geopandas",
        "rasterio",
        "patchify",
        "pillow",
        "matplotlib",
        "xyzservices",
        "ensure"
        ],
    # setup_reqires=['wheel'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)