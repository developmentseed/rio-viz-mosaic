"""rio_viz app."""

from starlette.responses import Response, HTMLResponse

from rio_viz.app import viz as BaseVizClass
from rio_viz_mosaic.templates.viewer import mosaic_template, mosaic_footprint_template


class vizMosaic(BaseVizClass):
    """Creates a very minimal slippy map tile server using fastAPI + Uvicorn."""

    def __init__(self, *args, **kwargs):
        """Overwrite base class."""
        super(vizMosaic, self).__init__(*args, **kwargs)

        @self.app.get(
            "/mosaic.html",
            responses={200: {"description": "Simple Mosaic viewer."}},
            response_class=HTMLResponse,
        )
        def mosaicviewer():
            """Handle /mosaic.html."""
            return mosaic_template(
                f"http://{self.host}:{self.port}",
                mapbox_access_token=self.token,
                mapbox_style=self.style,
            )

        @self.app.get(
            "/geojson.html",
            responses={200: {"description": "Simple Mosaic viewer."}},
            response_class=HTMLResponse,
        )
        def geojsonviewer():
            """Handle /mosaic.html."""
            return mosaic_footprint_template(
                f"http://{self.host}:{self.port}",
                mapbox_access_token=self.token,
                mapbox_style=self.style,
            )

        @self.app.get(
            "/mosaic/metadata",
            responses={200: {"description": "Return the metadata of the mosaic."}},
        )
        def metadata(response: Response):
            """Handle /mosaic/metadata requests."""
            return self.raster.metadata()

        @self.app.get(
            "/mosaic/geojson",
            responses={200: {"description": "Return the geojson of the mosaic."}},
        )
        def geojson(response: Response):
            """Handle /geojson requests."""
            return self.raster.geojson()

    def get_mosaic_template_url(self) -> str:
        """Get simple app template url."""
        return f"http://{self.host}:{self.port}/mosaic.html."

    def get_geojson_template_url(self) -> str:
        """Get simple app template url."""
        return f"http://{self.host}:{self.port}/geojson.html"
