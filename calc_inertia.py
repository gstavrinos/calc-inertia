#!/usr/bin/env python
import sys
import stl
#(sudo pip install numpy-stl)

# Command line params:
# 1: STL file
# 2: Mass
# 3: Scale

def getDimensions(model):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in model.points:
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return maxx - minx, maxy - miny, maxz - minz


# Based on https://en.wikipedia.org/wiki/List_of_moments_of_inertia#List_of_3D_inertia_tensors
def getInertia(x, y, z, m, s):
    xx = 1./12 * m * (y**2 + z**2) * s
    yy = 1./12 * m * (x**2 + z**2) * s
    zz = 1./12 * m * (x**2 + y**2) * s
    return xx, yy, zz

if __name__ == '__main__':
    model = stl.mesh.Mesh.from_file(sys.argv[1])
    m = float(sys.argv[2])
    scale = float(sys.argv[3])

    x, y, z = getDimensions(model)

    print("<inertia  ixx=\"%s\" ixy=\"0\" ixz=\"0\" iyy=\"%s\" iyz=\"0\" izz=\"%s\" />" % (getInertia(x, y, z, m, scale)))