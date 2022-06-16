# calc_inertia_for_urdf.py
Based on a provided URDF (or xacro), it reads all geometries that have a `mass` inertial tag, and prints a URDF-ready inertia matrix.

## Dependencies
* xacro (pip install xacro)
* numpy-stl (pip install numpy-stl)
* pycollada (pip install pycollada)
* urdf_paser_py (pip install urdf-parser-py)

Install with `pip install -r requirements.txt`

## Command line params
* 1: URDF file

### Features added in release 2.1
* Support for Collada (.dae) mesh files (in addition to STL)

### Features added in release 2.0
* Support for ROS1 **AND** ROS2. This functionality basically involves looking for mesh files in `package://` tags. (If your urdf/xacro only includes `file://` tags, there is nothing ROS-related to worry about)
* Support for **ALL** kind of geometries (mesh, box, sphere, cylinder)
* Xacro integration for files that use arguments or parameters in fields of interest
* Support for links that have inertia but not a visual tag (collisions only)

### Example
`python calc_inertia_for_urdf.py /home/gstavrinos/urdfs/model.urdf`
### Output

```
 Link name: chassis_link_00
 Mass: 48.0
 Scale: [0.015, 0.015, 0.015]
 Mesh: file:///home/gstavrinos/ros2_ws/install/kart_description/share/kart_description/meshes/kart_chassis.stl
---
Calculating inertia...
---

<inertia  ixx="107.96846534714074" ixy="0" ixz="0" iyy="279.5263367708269" iyz="0" izz="346.94143021711494" />

 Link name: steering_wheel_link_00
 Mass: 7.0
 Scale: [0.015, 0.015, 0.015]
 Mesh: file:///home/gstavrinos/ros2_ws/install/kart_description/share/kart_description/meshes/kart_steering_wheel.stl
---
Calculating inertia...
---

<inertia  ixx="1.7008840358588881" ixy="0" ixz="0" iyy="2.939219711456205" iyz="0" izz="3.1101995734940084" />
.
.
.

```

---


# calc_inertia.py
:warning:**Currently deprecated**:warning:

With an object's STL file and mass, calculate its inertia, based on its bounding box, in mass \* dimension \* scale. The output is URDF-ready.

## Dependencies (Compatible with both Python2 and Python3)
* numpy-stl (sudo pip install numpy-stl)

## Command line params
* 1: STL file
* 2: Mass (in kg)
* 3: Scale (in case you are scaling your model before use)(= 0.000001 if stl is in mm)

## Example
`python calc_inertia.py "/home/gstavrinos/meshes/model.stl" 0.025 1`

