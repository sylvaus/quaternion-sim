import sys
import quaternion.quaternion
from quaternion.pose import Pose
from solids import Sphere, Parallepiped
from mainwindow import MainWindow
from PyQt4 import QtGui


class Simulation(object):
    def __init__(self):
        self.ball = Sphere()
        self.plate = Parallepiped(10, 10, 1)

        self.qt_app = QtGui.QApplication(sys.argv)

        self.window = MainWindow()
        quat = quaternion.quaternion.quat_x(-45, False)
        self.window.set_camera_pose(Pose(quat, [0, 0, -30.0]))
        self.window.add_object(self.ball)
        self.window.add_object(self.plate)
        self.window.set_cyclic_call(self.update_object_poses)

    def start_simulation(self):

        self.window.start(50)

        sys.exit(self.qt_app.exec_())

    def update_object_poses(self):
        keys = self.window.get_pressed_keys(True)
        if len(keys) > 0:
            print(keys)


def main():
    sim = Simulation()
    sim.start_simulation()


if __name__ == "__main__":
    main()
