import sys
import quaternion.quaternion as quat
from quaternion.pose import Pose
from solids import Sphere, Parallepiped
from mainwindow import MainWindow
from PyQt4 import QtGui, QtCore
from numpy import array


class Simulation(object):
    def __init__(self):
        self.ball = Sphere()
        self.plate = Parallepiped(10, 10, 1)

        self.qt_app = QtGui.QApplication(sys.argv)

        self.window = MainWindow()

        self.window.set_camera_pose(Pose(quat.quaternion_x(-45, False),
                                         array([0, 0, -30.0])))
        self.window.add_solid(self.ball)
        self.window.add_solid(self.plate)
        self.window.set_cyclic_call(self.update_object_poses)

    def start_simulation(self):

        self.window.start(50)

        sys.exit(self.qt_app.exec_())

    def update_object_poses(self):
        keys = self.window.get_pressed_keys(True)
        if len(keys) > 0:
            if QtCore.Qt.Key_A in keys:
                self.plate.rotate(quat.quaternion_x(3, False))


def main():
    sim = Simulation()
    sim.start_simulation()


if __name__ == "__main__":
    main()
