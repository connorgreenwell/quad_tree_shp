import shapely.geometry as geom

mass_inpoly = lambda region, polys: [
    idx
    for idx in polys.keys()
    if region.intersects(polys[idx])
]

class Node():
    def __init__(self, shapes, bounds=None):
        assert isinstance(shapes, dict)
        self.shapes = shapes

        if bounds is None:
            bounds = geom.MultiPolygon(shapes.values()).bounds
            bounds = geom.box(*bounds)
        assert isinstance(bounds, geom.Polygon)
        self.bounds = bounds

        self.nodes = None

    def split(self, recurse=0):
        bounds = self.bounds.bounds
        center = (
            (bounds[0] + bounds[2]) / 2,        
            (bounds[1] + bounds[3]) / 2,        
        )

        sub_bounds = [
            geom.box(center[0], center[1], bounds[2], bounds[3]), 
            geom.box(bounds[0], center[1], center[0], bounds[3]),
            geom.box(bounds[0], bounds[1], center[0], center[1]),
            geom.box(center[0], bounds[1], bounds[2], center[1]),
        ]

        self.nodes = []
        for sub in sub_bounds:
            inds = mass_inpoly(sub, self.shapes)            
            sub_shapes = {
                idx: self.shapes[idx]
                for idx in inds
            }

            node = Node(sub_shapes, sub)
            if recurse > 0:
                node.split(recurse=recurse-1)

            self.nodes.append(node)

    def search(self, candidate):
        # if we have sub nodes, search through those
        for node in (self.nodes or []):
            if node.bounds.intersects(candidate):
                return node.search(candidate)

        # if we dont have any nodes, or somehow they all miss, we should just check all of our
        # shapes and return that
        for idx, shape in self.shapes.items():
            if shape.intersects(candidate):
                return idx

        # if we dont find a shape, just return -1
        return -1
