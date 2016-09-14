from PyQt4 import QtCore
from PyQt4 import QtGui

from canvas_opengl_qt import glWidget


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.widget = glWidget(self)
        self.button = QtGui.QPushButton('Reset', self)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.widget)
        mainLayout.addWidget(self.button)

        self.setCentralWidget(self.widget)

        self.pressed_keys = {}
        self.key_overflow = 128

    def add_object(self, object):
        self.widget.add_object(object)

    def keyPressEvent(self, event):
        # Memorize all key pressed

        if self.pressed_keys.has_keys(event.key()):
            self.pressed_keys[event.key()] = 1
        else:
            if self.pressed_keys[event.key()] < 128:
                self.pressed_keys[event.key()] += 1


    def start(self, refreshing_period=100):


        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.widget.updateGL)
        timer.start(refreshing_period)

        self.show()
