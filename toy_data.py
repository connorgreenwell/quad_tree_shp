import shapely
import shapely.geometry as geom
import numpy as np
import fiona

print("generating...")
res = 10.
latlon = np.mgrid[
    -90:90:res,
    -180:180:res]
squares = np.stack([latlon, latlon+res])
squares = squares.reshape([4, -1]).T

boxes = list(map(lambda sq: geom.box(*sq), squares))

print("saving...")

schema = {
    "geometry": "Polygon",
    "properties": {"id": "int"},
}
with fiona.open("toy.shp", "w", "ESRI Shapefile", schema) as f:
    for idx, box in enumerate(boxes):
        f.write({
            "geometry": geom.mapping(box),
            "properties": {"id": idx}
        })

print("done")
