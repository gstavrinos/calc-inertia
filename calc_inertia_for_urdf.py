#!/usr/bin/env python

import os
import sys
import xacro
import collada
from stl import mesh
from urdf_parser_py.urdf import URDF, Mesh, Box, Sphere, Cylinder

# For dependencies:
# pip install -r requirements.txt

# Command line params:
# 1: URDF file

def getSTLDimensions(model):
    return model.x.max() - model.x.min(), model.y.max() - model.y.min(), model.z.max() - model.z.min()

def getColladaDimensions(model):
    minx = miny = minz = float("inf")
    maxx = maxy = maxz = float("-inf")
    for tr_vertex in model.geometries[0].primitives[0].vertex[model.geometries[0].primitives[0].vertex_index]:
        for v in tr_vertex:
            maxx = maxx if v[0] <= maxx else v[0]
            maxy = maxy if v[1] <= maxy else v[1]
            maxz = maxz if v[2] <= maxz else v[2]
            minx = minx if v[0] >= minx else v[0]
            miny = miny if v[1] >= miny else v[1]
            minz = minz if v[2] >= minz else v[2]
    return maxx - minx, maxy - miny, maxz - minz

# Based on https://en.wikipedia.org/wiki/List_of_moments_of_inertia#List_of_3D_inertia_tensors
def getInertia(geometry, m, s):
    print("\033[97m Link name: \033[0m" + link_name)
    print("\033[93m Mass: \033[0m" + str(m))
    print("\033[95m Scale: \033[0m" + str(s))
    xx = yy = zz = 0.0
    if type(geometry) == Mesh:
        print("\033[94m Mesh: \033[0m" + geometry.filename)
        print("---\nCalculating inertia...\n---")
        ROS_VERSION = os.getenv("ROS_VERSION")
        get_pkg_fn = None
        if not ROS_VERSION:
            print("Could not find the ROS_VERSION environment variable, thus, can't determine your ros version. Assuming ROS2!")
            ROS_VERSION = "2"
        if ROS_VERSION == "1":
            import rospkg
            get_pkg_fn = rospkg.RosPack().get_path
        else:
            import ament_index_python
            get_pkg_fn = ament_index_python.get_package_share_path
        pkg_tag = "package://"
        file_tag = "file://"
        mesh_file = ""
        if geometry.filename.startswith(pkg_tag):
            package, mesh_file = geometry.filename.split(pkg_tag)[1].split(os.sep, 1)
            print(get_pkg_fn(package))
            mesh_file = str(get_pkg_fn(package))+os.sep+mesh_file
        elif geometry.filename.startswith(file_tag):
            mesh_file = geometry.filename.replace(file_tag, "")
        x = y = z = 0
        if mesh_file.endswith(".stl"):
            model = mesh.Mesh.from_file(mesh_file)
            x,y,z = getSTLDimensions(model)
        # Assuming .dae
        else:
            model = collada.Collada(mesh_file)
            x,y,z = getColladaDimensions(model)
        xx,yy,zz = getBoxInertia(x, y, z, m, s)
    elif type(geometry) == Box:
        print("\033[94m Box: \033[0m" + str(geometry.size))
        print("---\nCalculating inertia...\n---")
        x,y,z = geometry.size
        xx,yy,zz = getBoxInertia(x, y, z, m, s)
    elif type(geometry) == Sphere:
        print("\033[94m Sphere Radius: \033[0m" + str(geometry.radius))
        print("---\nCalculating inertia...\n---")
        xx,yy,zz = getSphereInertia(geometry.radius, m)
    elif type(geometry) == Cylinder:
        print("\033[94m Cylinder Radius and Length: \033[0m" + str(geometry.radius) + "," + str(geometry.length))
        print("---\nCalculating inertia...\n---")
        xx,yy,zz = getCylinderInertia(geometry.radius, geometry.length, m)

    print("\033[92m")
    print("<inertia  ixx=\"%s\" ixy=\"0\" ixz=\"0\" iyy=\"%s\" iyz=\"0\" izz=\"%s\" />" % (xx,yy,zz))
    print("\033[0m")

def getBoxInertia(x, y, z, m, s):
    x *= s[0]
    y *= s[1]
    z *= s[2]
    xx = 1./12 * m * (y**2 + z**2)
    yy = 1./12 * m * (x**2 + z**2)
    zz = 1./12 * m * (x**2 + y**2)
    return xx, yy, zz

def getSphereInertia(r, m):
    i = 2./5 * m * r**2
    return i, i, i

def getCylinderInertia(r, h, m):
    xx = yy = 1./12 * m * (3 * r**2 + h**2)
    zz = 1./2 * m * r**2
    return xx, yy, zz

if __name__ == '__main__':
    robot = URDF.from_xml_string(xacro.process_file(sys.argv[1]).toprettyxml())
    for link in robot.links:
        link_name = mass = geometry = None
        x = y = z = 0.0
        scale = [1.0, 1.0, 1.0]
        link_name = link.name
        inertial = link.inertial
        if inertial:
            mass = inertial.mass
            if mass:
                visual = link.visual
                if visual:
                    geometry = visual.geometry
                # If we don't find a visual geometry, look for a collision one
                else:
                    collision = link.collision
                    if collision:
                        geometry = collision.geometry

        if mass != None and geometry != None:
            try:
                if geometry.scale:
                    scale = geometry.scale
            except:
                scale = [1.0,1.0,1.0]
            getInertia(geometry, mass, scale)
