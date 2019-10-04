#!/usr/bin/env python

import os
import sys
import stl
import rospkg
import xml.etree.ElementTree
from urdf_parser_py.urdf import URDF

#(sudo pip install numpy-stl)
#(sudo pip install urdf-parser-py)

# Command line params:
# 1: URDF file


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
    xx = 1./12 * m * (y**2 + z**2) * s[0]
    yy = 1./12 * m * (x**2 + z**2) * s[1]
    zz = 1./12 * m * (x**2 + y**2) * s[2]
    return xx, yy, zz

if __name__ == '__main__':
    rospack = rospkg.RosPack()
    for (ev, el) in xml.etree.ElementTree.iterparse(sys.argv[1]):
        link_name = mass = mesh = None
        x = y = z = 0.0
        scale = [1.0, 1.0, 1.0]
        if el.tag == "link":
            link_name = el.get("name")
            
            for i in el:
                if i.tag == "inertial":
                    for j in i:
                        if j.tag == "mass":
                            mass = float(j.get("value"))
                if i.tag == "visual":
                    for j in i:
                        if j.tag == "geometry":
                            for k in j:
                                if k.tag == "mesh":
                                    mesh = k.get("filename")
                                    package, mesh = mesh.split("package://")[1].split("/", 1)
                                    mesh = rospack.get_path(package)+os.sep+mesh

                                    scale = k.get("scale", default=[1.0, 1.0, 1.0]).split()
                                    scale = [float(n) for n in scale]

            if mass != None and mesh != None:
                print("\033[97m Link name: \033[0m" + link_name)
                print("\033[93m Mass: \033[0m" + str(mass))
                print("\033[94m Mesh: \033[0m" + mesh)
                print("\033[95m Scale: \033[0m" + str(scale))
                print("---\nCalculating inertia...\n---")
                model = stl.mesh.Mesh.from_file(mesh)
                x, y, z = getDimensions(model)
                print("\033[92m")
                print("<inertia  ixx=\"%s\" ixy=\"0\" ixz=\"0\" iyy=\"%s\" iyz=\"0\" izz=\"%s\" />" % (getInertia(x, y, z, mass, scale)))
                print("\033[0m")
