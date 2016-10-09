# TODO add a function (add_axis)
from PyQt4 import QtCore
from PyQt4 import QtGui
from canvas_opengl_qt import glWidget
from quaternion.pose import Pose
from solids import Solid


class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)

        # Create the graph and button(s) widgets
        self.graph_widget = glWidget(self)
        self.button = QtGui.QPushButton('Reset', self)

        # Set the layout(s)
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.graph_widget)
        mainLayout.addWidget(self.button)

        # Put the main layout in a widget to set it as the main widget
        self.main_widget = QtGui.QWidget(self)
        self.main_widget.setLayout(mainLayout)

        self.setCentralWidget(self.main_widget)

        self.pressed_keys = {}
        self.key_overflow = 128

        self.user_cyclic_call = None

    def set_camera_pose(self, pose: Pose):
        self.graph_widget.set_camera_pos(pose)

    def add_solid(self, solid: Solid):
        self.graph_widget.add_solid(solid)

    def keyPressEvent(self, event):
        # Memorize all key pressed

        if self.pressed_keys.get(event.key()) is None:
            self.pressed_keys[event.key()] = 1
        else:
            if self.pressed_keys[event.key()] < 128:
                self.pressed_keys[event.key()] += 1

    def start(self, refreshing_period: int = 100):

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.cyclic_call)
        timer.start(refreshing_period)

        self.show()

    def cyclic_call(self):
        if callable(self.user_cyclic_call):
            self.user_cyclic_call()
        self.graph_widget.updateGL()

    def set_cyclic_call(self, func):
        self.user_cyclic_call = func

    def get_pressed_keys(self, delete: bool = False):
        if delete:
            temp = self.pressed_keys
            self.pressed_keys = {}
            return temp

        else:
            return self.pressed_keys
