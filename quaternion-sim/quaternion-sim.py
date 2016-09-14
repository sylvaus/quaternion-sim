import sys
from solids import Sphere, Parallepiped
from mainwindow import MainWindow
from PyQt4 import QtGui

class Simulation(object):
    def __init__(self):
        self.ball = Sphere()
        self.plate = Parallepiped(10, 10, 1)

        self.qt_app = QtGui.QApplication(sys.argv)
        self.window = MainWindow()
        self.window.add_object(self.ball)

    def start_simulation(self):

        self.window.start(50)

        sys.exit(self.qt_app.exec_())




def main():
    sim = Simulation()
    sim.start_simulation()


if __name__ == "__main__":
    main()