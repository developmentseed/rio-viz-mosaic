"""rio_viz.raster: raster tiles object."""

from typing import Tuple

import functools
from concurrent import futures

import numpy
import mercantile
import rasterio
from rio_tiler.main import tile as cogeoTiler
from rio_tiler_mosaic.mosaic import mosaic_tiler
from rio_tiler_mosaic.methods import defaults

from rio_viz import raster
from rio_viz_mosaic import utils


class MosaicRasterTiles(raster.RasterTiles):
    """Raster tiles object."""

    def __init__(self, mosaic_path: str):
        """Initialize MosaicRasterTiles object."""
        self.path = mosaic_path
        self.mosaic = utils.fetch_mosaic_definition(self.path)
        self.bounds = self.mosaic["bounds"]
        self.center = [
            (self.bounds[0] + self.bounds[2]) / 2,
            (self.bounds[1] + self.bounds[3]) / 2,
        ]
        self.minzoom = self.mosaic["minzoom"]
        self.maxzoom = self.mosaic["maxzoom"]

        # read layernames from the first file
        quadkeys = list(self.mosaic["tiles"].keys())
        src_path = self.mosaic["tiles"][quadkeys[0]][0]
        with rasterio.open(src_path) as src_dst:
            self.band_descriptions = utils.get_layer_names(src_dst)
            self.data_type = src_dst.dtypes[0]

    def read_tile(
        self,
        z: int,
        x: int,
        y: int,
        tilesize: int = 256,
        indexes: Tuple[int] = None,
        resampling_method: str = "bilinear",
    ) -> [numpy.ndarray, numpy.ndarray]:
        """Read raster tile data and mask."""
        assets = utils.get_assets(self.mosaic, x, y, z)
        return mosaic_tiler(
            assets,
            x,
            y,
            z,
            cogeoTiler,
            indexes=indexes,
            tilesize=tilesize,
            pixel_selection=defaults.FirstMethod(),
            resampling_method=resampling_method,
        )

    def _get_point(self, asset: str, coordinates: Tuple[float, float]) -> dict:
        with rasterio.open(asset) as src_dst:
            lng_srs, lat_srs = rasterio.warp.transform(
                "epsg:4326", src_dst.crs, [coordinates[0]], [coordinates[1]]
            )

            if not (
                (src_dst.bounds[0] < lng_srs[0] < src_dst.bounds[2])
                and (src_dst.bounds[1] < lat_srs[0] < src_dst.bounds[3])
            ):
                raise Exception("Outside bounds")

            return list(
                src_dst.sample([(lng_srs[0], lat_srs[0])], indexes=src_dst.indexes)
            )[0].tolist()

    def point(self, coordinates: Tuple[float, float]) -> dict:
        """Read point value."""

        min_zoom = self.mosaic["minzoom"]
        quadkey_zoom = self.mosaic.get("quadkey_zoom", min_zoom)  # 0.0.2
        tile = mercantile.tile(coordinates[0], coordinates[1], quadkey_zoom)
        assets = utils.get_assets(self.mosaic, tile.x, tile.y, tile.z)

        _points = functools.partial(self._get_point, coordinates=coordinates)
        with futures.ThreadPoolExecutor() as executor:
            future_work = [executor.submit(_points, item) for item in assets]
            results = list(utils._filter_futures(future_work))

        return {
            "coordinates": coordinates,
            "value": {b: r for b, r in zip(self.band_descriptions, results[0])},
        }

    def metadata(self) -> dict:
        """Get Raster metadata."""
        info = {
            "bounds": {"value": self.bounds, "crs": "epsg:4326"},
            "minzoom": self.minzoom,
            "maxzoom": self.maxzoom,
        }
        info["dtype"] = self.data_type
        info["band_descriptions"] = [(b, b) for b in self.band_descriptions]
        return info

    def geojson(self) -> dict:
        """Get Raster metadata."""
        return {
            "type": "FeatureCollection",
            "features": [
                mercantile.feature(
                    mercantile.quadkey_to_tile(qk), props=dict(files=files)
                )
                for qk, files in self.mosaic["tiles"].items()
            ],
        }
