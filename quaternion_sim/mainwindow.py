from typing import Callable, Dict
from PyQt4 import QtCore
from PyQt4 import QtGui
from .canvas_opengl_qt import glWidget
from .quaternion.pose import Pose
from .solids import Solid
from .axes import Axis


class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtGui.QMainWindow.__init__(self, *args, **kwargs)

        # Create the graph and button(s) widgets
        self.graph_widget = glWidget(self)

        # Set the layout(s)
        mainLayout = QtGui.QHBoxLayout()
        self.buttonsLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.graph_widget)
        mainLayout.addLayout(self.buttonsLayout)

        # Put the main layout in a widget to set it as the main widget
        self.main_widget = QtGui.QWidget(self)
        self.main_widget.setLayout(mainLayout)

        self.setCentralWidget(self.main_widget)

        self.pressed_keys = {}
        self.key_overflow = 128

        self.user_cyclic_call = None

    def set_camera_pose(self, pose: Pose) -> None:
        self.graph_widget.set_camera_pos(pose)

    def add_solid(self, solid: Solid) -> None:
        self.graph_widget.add_solid(solid)

    def add_axis(self, axis: Axis) -> None:
        self.graph_widget.add_axis(axis)

    def add_button(self, text: str, action: Callable) -> None:
        button = QtGui.QPushButton(text, self)
        button.clicked.connect(action)
        self.buttonsLayout.addWidget(button)

    def keyPressEvent(self, event) -> None:
        # Memorize all key pressed

        if self.pressed_keys.get(event.key()) is None:
            self.pressed_keys[event.key()] = 1
        else:
            if self.pressed_keys[event.key()] < 128:
                self.pressed_keys[event.key()] += 1

    def start(self, refreshing_period: int = 100) -> None:

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.cyclic_call)
        timer.start(refreshing_period)

        self.show()

    def cyclic_call(self) -> None:
        if callable(self.user_cyclic_call):
            self.user_cyclic_call()
        self.graph_widget.updateGL()

    def set_cyclic_call(self, func) -> None:
        self.user_cyclic_call = func

    def set_frame_mgr(self, frame_mgr) -> None:
        self.graph_widget.set_frame_mgr(frame_mgr)

    def get_pressed_keys(self, delete: bool = False) -> Dict:
        if delete:
            temp = self.pressed_keys
            self.pressed_keys = {}
            return temp

        else:
            return self.pressed_keys
