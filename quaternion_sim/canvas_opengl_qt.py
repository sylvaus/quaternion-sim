# TODO clean imports, add a function (add_axis) and the related draw part

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt4.QtOpenGL import *
from .geometry.pose import Pose
from .solids import Solid
from .frames import FrameManager, Frame
from .axes import Axis


class glWidget(QGLWidget):
    def __init__(self,
                 parent,
                 camera_pose: Pose = Pose(),
                 back_color: list = None,
                 ambient_light_color: list = None,
                 diffuse_light_color: list = None,
                 diffuse_light_position: list = None,
                 solids: list = None,
                 axes: list = None,
                 frame_mgr: FrameManager = None
                 ):

        # ADDED FOR LINUX
        glutInit(sys.argv)

        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)

        self.solids = solids if solids else []
        self.axes = axes if axes else []

        self.frame_mgr = frame_mgr

        # Camera pose
        self.camera_pose = camera_pose

        # Color parameters
        self.back_color = back_color if back_color else [0.3, 0.5, 1.0, 0.0]

        # Lighting parameters
        self.ambient_light_color = ambient_light_color if ambient_light_color else [1.0, 1.0, 1.0, 0]
        self.diffuse_light_color = diffuse_light_color if diffuse_light_color else [1.0, 1.0, 1.0, 0]
        self.diffuse_light_position = diffuse_light_position if diffuse_light_position else [10.0, 10.0, 10.0, 0.0]

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.frame_mgr is None:
            for solid in self.solids:
                solid.draw()

            for axis in self.axes:
                axis.draw()

        else:
            frame_poses = self.frame_mgr.get_all_frame_poses()

            for solid in self.solids:
                self.move_to_pose(frame_poses[solid.ref_frame])
                solid.draw(False)

            for axis in self.axes:
                self.move_to_pose(frame_poses[axis.frame.name])
                axis.draw(False)

        # REMOVED FOR LINUX
        # glutSwapBuffers()

    def updateGL(self):
        self.glDraw()

    def initializeGL(self):
        glClearColor(self.back_color[0], self.back_color[1],
                     self.back_color[2], self.back_color[3])

        # Set the display
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        gluPerspective(45.0, 1.33, 0.1, 100.0)
        self.move_to_pose(self.camera_pose, False)

        glMatrixMode(GL_MODELVIEW)

        self.init_lights()

    def set_camera_pos(self, pose: Pose):
        self.camera_pose = pose

    def set_ambient_light(self, color: list):
        self.ambient_light_color = color

    def set_diffuse_light(self, color: list, position: list):
        self.diffuse_light_color = color
        self.diffuse_light_position = position

    def set_frame_mgr(self, frame_mgr:FrameManager):
        self.frame_mgr = frame_mgr

    def init_lights(self):
        glEnable(GL_LIGHTING)

        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse_light_color)
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_light_position)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT1, GL_AMBIENT, self.ambient_light_color)
        glEnable(GL_LIGHT1)

    def add_axis(self, axis: Axis):
        if not hasattr(axis, "draw"):
            raise "The frame {0} does not have a draw function".format(axis.__str__())

        self.axes.append(axis)

    def add_solid(self, solid: Solid):
        if not hasattr(solid, "draw"):
            raise "The solid {0} does not have a draw function".format(solid.__str__())

        self.solids.append(solid)

    def move_to_pose(self, pose: Pose, from_ref_frame:bool = True):
        if from_ref_frame:
            glLoadIdentity()

        glTranslatef(pose.position[0],
                     pose.position[1],
                     pose.position[2])

        glRotatef(pose.orientation.get_theta(rad=False),
                  pose.orientation[1],
                  pose.orientation[2],
                  pose.orientation[3])
