from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt4.QtOpenGL import *
from quaternion.pose import Pose
from solids import Solid


class glWidget(QGLWidget):
    def __init__(self,
                 parent,
                 camera_pose: Pose = Pose(),
                 back_color: list = [0.3, 0.5, 1.0, 0.0],
                 ambient_light_color: list = [1.0, 1.0, 1.0, 0],
                 diffuse_light_color: list = [1.0, 1.0, 1.0, 0],
                 diffuse_light_position: list = [10.0, 10.0, 10.0, 0.0],
                 objects: list = []
                 ):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        self.objects = objects

        # Camera pose
        self.camera_pose = camera_pose

        # Color parameters
        self.back_color = back_color

        # Lighting parameters
        self.ambient_light_color = ambient_light_color
        self.diffuse_light_color = diffuse_light_color
        self.diffuse_light_position = diffuse_light_position

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for object in self.objects:
            object.draw()

        glutSwapBuffers()

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
        glTranslatef(self.camera_pose.position[0],
                     self.camera_pose.position[1],
                     self.camera_pose.position[2])

        glRotatef(self.camera_pose.orientation.get_theta(rad=False),
                  self.camera_pose.orientation[1],
                  self.camera_pose.orientation[2],
                  self.camera_pose.orientation[3])

        glMatrixMode(GL_MODELVIEW)

        self.init_lights()

    def set_camera_pos(self, pose: Pose):
        self.camera_pose = pose

    def set_ambient_light(self, color: list):
        self.ambient_light_color = color

    def set_diffuse_light(self, color: list, position: list):
        self.diffuse_light_color = color
        self.diffuse_light_position = position

    def init_lights(self):
        glEnable(GL_LIGHTING)

        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse_light_color)
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_light_position)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT1, GL_AMBIENT, self.ambient_light_color)
        glEnable(GL_LIGHT1)

    def add_solid(self, solid: Solid):
        self.objects.append(solid)
