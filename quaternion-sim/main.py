import sys

import numpy as np
from canvasQT import MainWindow
from matplotlib.backends import qt_compat
from matplotlib_shapes.parallelepiped import Parallelepiped
from matplotlib_shapes.sphere import Sphere
from quaternion import quat_from_2_vectors

use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui
else:
    from PyQt4 import QtGui


class Plate(Parallelepiped):
    rot_x = 0
    rot_y = 0

    def update_func(self, axes, pressed_keys):


        # first, we extract the pressed keys
        for pk in pressed_keys:
            if pk == 0:
                self.rot_x += 1/20
            elif pk == 1:
                self.rot_x -= 1/20
            elif pk == 2:
                self.rot_y += 1/20
            elif pk == 3:
                self.rot_y -= 1/20

        pressed_keys.clear()

        vz = np.array([0,0,1])
        vdelta = np.array([np.cos(self.rot_x)*np.sin(self.rot_y),
                           np.cos(self.rot_y)*np.sin(self.rot_x),
                           np.cos(self.rot_x)*np.cos(self.rot_x)])

        self.orientation = quat_from_2_vectors(vz, vdelta)

        axes.collections = []
        self.draw(axes)


class Ball(Sphere):
    rot_x = 0
    rot_y = 0

    def update_func(self, axes, pressed_keys):


        # first, we extract the pressed keys
        for pk in pressed_keys:
            if pk == 0:
                self.rot_x += 1/20
            elif pk == 1:
                self.rot_x -= 1/20
            elif pk == 2:
                self.rot_y += 1/20
            elif pk == 3:
                self.rot_y -= 1/20

        pressed_keys.clear()

        vz = np.array([0,0,1])
        vdelta = np.array([np.cos(self.rot_x)*np.sin(self.rot_y),
                           np.cos(self.rot_y)*np.sin(self.rot_x),
                           np.cos(self.rot_x)*np.cos(self.rot_x)])

        self.orientation = quat_from_2_vectors(vz, vdelta)

        axes.clear()
        return self.draw(axes)





def main():
    plate = Ball()
    q_app = QtGui.QApplication(sys.argv)

    window = MainWindow()
    window.add_graph(plate.update_func)

    window.show()
    sys.exit(q_app.exec_())

if __name__ == "__main__":
    main()