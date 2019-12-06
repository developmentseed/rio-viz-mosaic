"""rio_viz.cli."""

import os

import click
from rio_viz_mosaic import app, raster


class MbxTokenType(click.ParamType):
    """Mapbox token type."""

    name = "token"

    def convert(self, value, param, ctx):
        """Validate token."""
        try:
            if not value:
                return ""

            assert value.startswith("pk")
            return value

        except (AttributeError, AssertionError):
            raise click.ClickException(
                "Mapbox access token must be public (pk). "
                "Please sign up at https://www.mapbox.com/signup/ to get a public token. "
                "If you already have an account, you can retreive your "
                "token at https://www.mapbox.com/account/."
            )


@click.command()
@click.argument("mosaic_path", type=str, required=True)
@click.option(
    "--style",
    type=click.Choice(["satellite", "basic"]),
    default="basic",
    help="Mapbox basemap",
)
@click.option("--port", type=int, default=8080, help="Webserver port (default: 8080)")
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Webserver host url (default: 127.0.0.1)",
)
@click.option(
    "--mapbox-token",
    type=MbxTokenType(),
    metavar="TOKEN",
    default=lambda: os.environ.get("MAPBOX_ACCESS_TOKEN", ""),
    help="Mapbox token",
)
@click.option(
    "--footprint", is_flag=True, default=False, help="Visualize Mosaic Footprint"
)
def viz_mosaic(mosaic_path, style, port, host, mapbox_token, footprint):
    """Rasterio Viz cli."""
    # Check if cog
    src_dst = raster.MosaicRasterTiles(mosaic_path)
    application = app.vizMosaic(
        src_dst, token=mapbox_token, port=port, host=host, style=style
    )
    if footprint:
        url = application.get_geojson_template_url()
    else:
        url = application.get_mosaic_template_url()

    click.echo(f"Viewer started at {url}", err=True)
    click.launch(url)
    application.start()
