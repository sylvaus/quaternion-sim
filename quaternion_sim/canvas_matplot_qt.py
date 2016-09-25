from __future__ import unicode_literals
import sys
import matplotlib.pyplot as plt

from matplotlib.backends import qt_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.animation import FuncAnimation
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore


class DynamicCanvas(FigureCanvas):
    def __init__(self,
                 update_func,
                 parent=None,
                 timer_period=50,
                 pressed_keys=None):
        """
        :param update_func: callable taking 2 parameters (Axes3D and an Array containing keystrokes data)
        :param parent:
        :param timer_period:
        :param axes_limits:
        :param pressed_keys:
        :return: None
        """

        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111, projection='3d')
        # We want the axes cleared every time plot() is called
        self.axes.hold(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)

        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(timer_period)

        self.update_func = update_func
        self.pressed_keys = pressed_keys
        self.fig.canvas.draw()

        self.animation = FuncAnimation(self.fig, self.update_figure, interval=timer_period, blit=True)

    def update_figure(self, i):
        return self.update_func(self.axes, self.pressed_keys)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtGui.QWidget(self)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.pressed_keys = []

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Z:
            self.pressed_keys.append(0)
        elif e.key() == QtCore.Qt.Key_S:
            self.pressed_keys.append(1)
        elif e.key() == QtCore.Qt.Key_Q:
            self.pressed_keys.append(2)
        elif e.key() == QtCore.Qt.Key_D:
            self.pressed_keys.append(3)

    def add_graph(self,
                  update_func,
                  timer_period=100,
                  axes_limits=[[-2.0, 2.0], [-2.0, 2.0], [-2.0, 2.0]]):

        l = QtGui.QVBoxLayout(self.main_widget)
        dc = DynamicCanvas(update_func, self.main_widget, timer_period, self.pressed_keys)

        # Setting the axes properties
        dc.axes.set_xlim3d(axes_limits[0])
        dc.axes.set_xlabel('X')

        dc.axes.set_ylim3d(axes_limits[1])
        dc.axes.set_ylabel('Y')

        dc.axes.set_zlim3d(axes_limits[2])
        dc.axes.set_zlabel('Z')

        dc.axes.plot([1], [1], [1])

        l.addWidget(dc)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About", """""")


class CanvasQT(object):
    def __init__(self,
                 update_func,
                 timer_period=100,
                 axes_limits=[[-2.0, 2.0], [-2.0, 2.0], [-2.0, 2.0]]):
        self.q_app = QtGui.QApplication(sys.argv)
        self.window = MainWindow()
        self.window.add_graph(update_func, timer_period, axes_limits)

    def set_window_title(self, name):
        self.window.setWindowTitle("%s" % name)

    def run(self):
        self.window.show()
        sys.exit(self.q_app.exec_())


def test(w):
    pass


if __name__ == "__main__":
    uw = CanvasQT(test)
    uw.run()
