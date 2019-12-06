# rio-viz-mosaic

Rasterio plugin to visualize [Mosaic](https://github.com/developmentseed/mosaicjson-spec) of Cloud Optimized GeoTIFF in browser.

![](https://user-images.githubusercontent.com/10407788/70332350-62d62980-180f-11ea-9527-9eaecdbcdbc5.png)

### Install

```bash
# python-vtzero will only compile with Cython < 0.29
$ pip install cython==0.28
$ pip install git+https://github.com/developmentseed/rio-viz-mosaic.git
```

##### CLI
```bash 
$ rio viz-mosaic --help                                                                                                
Usage: rio viz-mosaic [OPTIONS] MOSAIC_PATH

  Rasterio Viz cli.

Options:
  --style [satellite|basic]  Mapbox basemap
  --port INTEGER             Webserver port (default: 8080)
  --host TEXT                Webserver host url (default: 127.0.0.1)
  --mapbox-token TOKEN       Mapbox token
  --footprint                Visualize Mosaic Footprint
  --help                     Show this message and exit.
```

Create mosaic-json file (see [cogeo-mosaic](https://github.com/developmentseed/cogeo-mosaic) cli)

