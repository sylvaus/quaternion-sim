import sys
from quaternion.quaternion import Quaternion, quat_from_axis_and_theta
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
        quat = quat_from_axis_and_theta([1,1,0],0.78)
        self.window.set_camera_pose(Pose(quat,[0,0,-30.0]))
        self.window.add_object(self.ball)
        self.window.add_object(self.plate)

    def start_simulation(self):

        self.window.start(50)

        sys.exit(self.qt_app.exec_())




def main():
    sim = Simulation()
    sim.start_simulation()


if __name__ == "__main__":
    main()