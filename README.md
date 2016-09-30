# quaternion-sim
### Quick Description
A little project to show one use of quaternion ,different ways to model 
a ball on a plate and teach a bit of control theory

### Getting Started
Clone this repository
Make sure you have all the required python packages
Run quaternion-sim.py

### Implementation Status 
- Quaternion class (easy): Done
- Pose class (easy): Done
- Solid class (easy): Done
- Frame class (medium): On going
- Frame Manager (medium): On going
- the graphic side (medium): Expected soon
    - Solids (ball and plate): Done
    - Axes: On going (require Frame class)
- Ball plate dynamics equation: Not started 
- Tests: Just started


### Requirements
- Python 3.5
- Numpy (developed with V1.10.4)
- PyQt4 (developed with V4.11.4) 
    - Installed using Homebrew on Mac
- matplolib (developed with V1.5.1)
    - Not required anymore (switched to OpenGl for 
      visual representation) 
- PyOpenGL (developed with V3.1.0)

The first four are contained in the Anaconda Python 3.5 distribution.
The last one can be obtained by using pip: 
$ pip install PyOpenGL PyOpenGL_accelerate