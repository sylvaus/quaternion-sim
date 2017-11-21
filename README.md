# quaternion-sim
## Quick Description
A little project to show one use of quaternion, different ways to model 
a ball on a plate and teach a bit of control theory.

## Quaternions
### General Informations
The notation used in this project is 
**q** = [q0, q1, q2, q3] = [q0, **qv**]
where 
q0 = cos(\theta/2)
**qv** = sin(\theta/2)**e**
with **e** the axis of rotation (with a unit norm)

### Quaternion Math
Will soon be described on the draft of my [website](http://pywhy.pythonanywhere.com/).


## Getting Started
Clone this repository
Make sure you have all the required python and Ubuntu packages then run:   
`python3 main.py`

## Implementation Status 
- Quaternion class (easy): Done
- Pose class (easy): Done
- Solid class (easy): Done
- Frame class (medium): Done
- Frame Manager (medium): Done
- the graphic side (medium): On going (90%)
    - Solids (ball and plate): Done
    - Axes: Done
    - Improving Classes
- Ball plate dynamics equation: Not started 

- Adding C\Cpp externals for faster computation: Not started

- Tests: On going
    - frames (100%)
    - quaternion (0%)
    - pose (0%)
    - solids (0%)
    

## Requirements
- Python 3.5
- Numpy (developed with V1.10.4)
- PyQt4 (developed with V4.11.4) 
    - Installed using Homebrew on Mac
- matplolib (developed with V1.5.1)
    - Not required anymore (switched to OpenGl for 
      visual representation) 
- PyOpenGL (developed with V3.1.0)

### Pip Packages
The first four are contained in the Anaconda Python 3.5 distribution.
The last one can be obtained by using pip:   
`pip install numpy PyOpenGL PyOpenGL_accelerate`

### Ubnutu Packages
#### OpenGl
`sudo apt-get install build-essential libgl1-mesa-dev libglew-dev libsdl2-dev libsdl2-image-dev libglm-dev libfreetype6-dev`
#### PyQt4
`sudo apt-get install python3-pyqt4`
