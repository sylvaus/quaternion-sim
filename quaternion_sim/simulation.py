import sys
from .quaternion import quaternion as quat
from .quaternion.pose import Pose
from .solids import Sphere, Parallepiped
from .frames import Frame, FrameManager
from .axes import Axis
from .mainwindow import MainWindow
from PyQt4 import QtGui, QtCore
from numpy import array


class Simulation(object):
    def __init__(self):
        gray_color = [0.4, 0.4, 0.4, 0.0]

        self.frame_ref = Frame("ref_frame", Pose())
        self.plate = Parallepiped(10, 10, 1, name="plate", ref_frame="ref_frame")
        self.ball = Sphere(name="ball",
                           pose=Pose(position=array([0, 0, 1.5])),
                           init_pose=Pose(position=array([0, 0, 1.5])),
                           ref_frame=self.plate.frame.name,
                           ambient_color=gray_color,
                           diffuse_color=gray_color)

        self.frame_mgr = FrameManager(self.frame_ref)
        self.frame_mgr.add_frame(self.plate.frame)
        self.frame_mgr.add_frame(self.ball.frame)

        self.axis = Axis(self.frame_ref,10)

        self.qt_app = QtGui.QApplication(sys.argv)

        self.window = MainWindow()

        self.window.set_camera_pose(Pose(quat.quaternion_x(-45, False),
                                         array([0, 0, -30.0])))
        self.window.add_solid(self.ball)
        self.window.add_solid(self.plate)
        self.window.add_axis(self.axis)
        self.window.set_frame_mgr(self.frame_mgr)
        self.window.set_cyclic_call(self.update_object_poses)
        self.window.add_button("Reset", self.reset)

    def start_simulation(self):

        self.window.start(10)

        sys.exit(self.qt_app.exec_())

    def reset(self):
        self.plate.reset_pose()
        self.ball.reset_pose()
        self.ball.reset_vels()

    def update_object_poses(self):
        keys = self.window.get_pressed_keys(delete=True)
        if len(keys) > 0:
            if QtCore.Qt.Key_A in keys:
                self.plate.rotate(quat.quaternion_x(3, False))
            if QtCore.Qt.Key_Q in keys:
                self.plate.rotate(quat.quaternion_x(-3, False))
            if QtCore.Qt.Key_S in keys:
                self.plate.rotate(quat.quaternion_y(3, False))
            if QtCore.Qt.Key_W in keys:
                self.plate.rotate(quat.quaternion_y(-3, False))
            if QtCore.Qt.Key_Z in keys:
                self.plate.rotate(quat.quaternion_z(3, False))
            if QtCore.Qt.Key_X in keys:
                self.plate.rotate(quat.quaternion_z(-3, False))

            if QtCore.Qt.Key_P in keys:
                self.ball.translate(array([0.1,0,0]))

            if QtCore.Qt.Key_M in keys:
                self.ball.translate(array([0,0.1,0]))

            if QtCore.Qt.Key_Escape in keys:
                self.reset()


