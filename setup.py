"""setup: rio-viz-mosaic"""

from setuptools import setup, find_packages

# Runtime requirements.
inst_reqs = ["rio-viz", "rio-tiler-mosaic", "mercantile"]

extra_reqs = {
    "test": ["requests", "mock", "pytest", "pytest-cov"],
    "dev": ["mock", "pytest", "pytest-cov", "pre-commit"],
}

setup(
    name="rio-viz-mosaic",
    version="0.0.1",
    python_requires=">=3",
    description=u"Visualize Cloud Optimized GeoTIFF Mosaics in browser",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="COG COGEO Rasterio GIS MVT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points="""
      [rasterio.rio_plugins]
      viz_mosaic=rio_viz_mosaic.scripts.cli:viz_mosaic
      """,
)
