from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from numpy import matrix
from numpy.core.numeric import identity
from quaternion import *


class Solids(object):
    def __init__(self,
                 position: np.ndarray = np.array([0, 0, 0]),
                 orientation: Quaternion = Quaternion(),
                 original_orientation: Quaternion = Quaternion(),
                 mass: float = 1.0,
                 inertia: matrix = identity(3),
                 ambient_color: list = (1, 1, 1, 0),
                 diffuse_color: list = (1, 1, 1, 0)):

        self.position = position
        self.orientation = orientation
        self.orig_orient = original_orientation
        self.mass = mass
        self.inertia = inertia
        self.ambient_color = ambient_color
        self.diffuse_color = diffuse_color

    def set_position(self, pos: np.ndarray):
        self.position = pos

    def set_orient(self, quat: Quaternion):
        self.orientation = quat

    def set_origin_orientation(self, quat: Quaternion):
        self.orig_orient = quat

    def set_mass(self, mass: float):
        self.mass = mass

    def set_inertia(self, inertia: matrix):
        self.inertia = inertia

    def rotate(self, quat: Quaternion):
        self.orientation = quat * self.orientation

    def translate(self, delta_pos: np.ndarray):
        self.position = delta_pos + self.position

    def get_position(self):
        return self.position

    def get_orient(self):
        return self.orientation

    def get_origin_orientation(self):
        return self.orig_orient

    def get_mass(self):
        return self.mass

    def get_inertia(self):
        return self.inertia

    def move_to_pose(self):
        # Reset init view
        glLoadIdentity()

        # Translate to the right position
        glTranslatef(self.position[0],
                     self.position[1],
                     self.position[2])

        # Rotate to the right orientation
        angle = self.orientation.get_theta() * 360.0
        axis = self.orientation.get_axis()

        glRotatef(angle,
                  axis[0],
                  axis[1],
                  axis[2])

    def apply_material(self):
        # Set material
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [i for i in self.ambient_color])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [i for i in self.diffuse_color])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 0.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 20)


class Sphere(Solids):
    def __init__(self, radius: int = 1, *args):
        Solids.__init__(*args)
        self.radius = radius

    def draw(self):
        self.move_to_pose()
        self.apply_material()

        # draw sphere
        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad, GLU_FILL)
        gluQuadricTexture(quad, True)
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, self.radius, 20, 20)


class Parallepiped(Solids):
    def __init__(self,
                 length: int = 1,
                 width: int = 1,
                 height: int = 1,
                 *args):
        Solids.__init__(*args)
        self.length = length
        self.width = width
        self.height = height

    def draw(self):
        self.move_to_pose()
        self.apply_material()

        # draw parallelepiped
        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad, GLU_FILL)
        gluQuadricTexture(quad, True)
        gluQuadricNormals(quad, GLU_SMOOTH)
        glScalef(self.length, self.width, self.height)
        glutSolidCube(1)


if __name__ == "__main__":
    print(identity(3))
