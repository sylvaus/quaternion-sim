from PyQt4 import QtCore
from PyQt4 import QtGui
from canvas_opengl_qt import glWidget
from quaternion.pose import Pose


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

    def set_camera_pose(self, pose: Pose):
        self.graph_widget.set_camera_pos(pose)

    def add_object(self, object):
        self.graph_widget.add_object(object)

    def keyPressEvent(self, event):
        # Memorize all key pressed

        if self.pressed_keys.has_keys(event.key()):
            self.pressed_keys[event.key()] = 1
        else:
            if self.pressed_keys[event.key()] < 128:
                self.pressed_keys[event.key()] += 1


    def start(self, refreshing_period=100):


        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.graph_widget.updateGL)
        timer.start(refreshing_period)

        self.show()
