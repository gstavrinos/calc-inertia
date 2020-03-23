# calc_inertia.py
With an object's STL file and mass, calculate its inertia, based on its bounding box, in mass \* dimension \* scale. The output is URDF-ready.

## Dependencies (Compatible with both Python2 and Python3)
* numpy-stl (sudo pip install numpy-stl)

## Command line params
* 1: STL file
* 2: Mass (in kg)
* 3: Scale (in acese you are scaling your model before use)(= 0.000001 if stl is in mm)

## Example
`python calc_inertia.py "/home/gstavrinos/meshes/model.stl" 0.025 1`

# calc_inertia_for_urdf.py
Based on the provided URDF (or xacro, by just disregarding xacro tags), it reads all **meshes** (no primitive shapes) that have a `mass` inertial tag, and prints a URDF-ready inertia matrix.

## Dependencies
* numpy-stl (sudo pip install numpy-stl)
* urdf_paser_py (sudo pip install urdf-parser-py)

## Command line params
* 1: URDF file

## Example
`python calc_inertia_for_urdf.py /home/gstavrinos/urdfs/model.urdf`
