# depth=8 seems ideal for the countries shapefile

import quad_tree_shp as node
import shapely.geometry as geom
import shapefile as shp
import numpy as np
import time

f = shp.Reader("/homes/connor/workspace/face2gps/src/binning/tree/data/ne_50m_admin_0_countries.shp")
#f = shp.Reader("data/toy.shp")
shapes = {
    str(sr.record[-20]): geom.shape(sr.shape)
    for sr in f.iterShapeRecords()
}

depth = 6

root = node.Node(shapes, geom.box(-180, -90, 180, 90))
root.split(recurse=depth)

for _ in range(100):
    point = np.random.uniform([-180, -90], [180, 90])    
    code = root.search(geom.Point(point))
    print(code)
