# calc-inertia
With an object's STL file and mass, calculate its inertia, based on its bounding box. The output is URDF-ready.

## Dependencies (Compatible with both Python2 and Python3)
* numpy-stl (sudo pip install numpy-stl)

## Command line params
* 1: STL file
* 2: Mass
* 3: Scale (in acese you are scaling your model before use)

## Example
`python calc_inertia.py "/home/gstavrinos/meshes/model.stl" 0.025 1`
