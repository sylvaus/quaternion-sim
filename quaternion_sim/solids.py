from OpenGL.GL import glLoadIdentity, glTranslatef, glRotatef, glMaterialfv, \
                        glMaterialf, GL_FRONT_AND_BACK, GL_AMBIENT, GL_DIFFUSE, \
                        GL_SPECULAR, GL_SHININESS, glScalef
from OpenGL.GLU import gluNewQuadric, gluQuadricDrawStyle, gluQuadricTexture, \
                        gluQuadricNormals, gluSphere, GLU_FILL, GLU_SMOOTH
from OpenGL.GLUT import glutSolidCube

from numpy import matrix, ndarray, pi
from numpy.core.numeric import identity

from quaternion.quaternion import Quaternion
from quaternion.pose import Pose

from frames import Frame

import copy as cp

rad_to_deg = 180 / pi


class Solid(object):
    def __init__(self,
                 name: str,
                 pose: Pose = Pose(),
                 init_pose: Pose = Pose(),
                 ref_frame: str = None,
                 mass: float = 1.0,
                 inertia: matrix = identity(3),
                 ambient_color: list = [0.0, 0.0, 0.0, 0],
                 diffuse_color: list = [0.0, 0.0, 0.0, 0]):

        self.name = name
        self.pose = pose
        self.init_pose = cp.deepcopy(init_pose)

        if ref_frame is None:
            self.ref_frame = None
            self.frame = None

        else:
            self.ref_frame = ref_frame
            self.frame = Frame("frame_{0}".format(self.name),
                               self.pose,
                               self.ref_frame)

        self.mass = mass
        self.inertia = inertia
        self.ambient_color = ambient_color
        self.diffuse_color = diffuse_color

    def set_pose(self, pose: Pose):
        self.pose = pose
        self.frame.pose = pose

    def set_position(self, pos: ndarray):
        self.pose.position = pos

    def set_orientation(self, quat: Quaternion):
        self.pose.orientation = quat

    def set_init_pose(self, pose: Pose):
        self.init_pose = pose

    def set_init_position(self, pos: ndarray):
        self.init_pose.position = pos

    def set_init_orientation(self, quat: Quaternion):
        self.init_pose.orientation = quat

    def set_mass(self, mass: float):
        self.mass = mass

    def set_inertia(self, inertia: matrix):
        self.inertia = inertia

    def rotate(self, quat: Quaternion):
        self.pose.rotate(quat)

    def translate(self, delta_pos: ndarray):
        self.pose.translate(delta_pos)

    def get_pose(self, dcopy=False) -> Pose:
        if dcopy:
            return cp.deepcopy(self.pose)
        else:
            return self.pose

    def get_position(self) -> ndarray:
        return self.pose.position

    def get_orientation(self) -> Quaternion:
        return self.pose.orientation

    def get_init_pose(self, dcopy=False) -> Pose:
        if dcopy:
            return cp.deepcopy(self.init_pose)
        else:
            return self.init_pose

    def get_init_position(self) -> ndarray:
        return self.init_pose.position

    def get_init_orientation(self) -> Quaternion:
        return self.init_pose.orientation

    def get_mass(self) -> float:
        return self.mass

    def get_inertia(self) -> matrix:
        return self.inertia

    def opgl_move_to_pose(self, from_fixed_frame: bool = True):
        if from_fixed_frame:
            # Reset init view
            glLoadIdentity()

        # Translate to the right position
        glTranslatef(self.pose.position[0],
                     self.pose.position[1],
                     self.pose.position[2])

        # Rotate to the right orientation
        glRotatef(self.pose.orientation.get_theta(rad=False),
                  self.pose.orientation[1],
                  self.pose.orientation[2],
                  self.pose.orientation[3])

    def apply_material(self):
        # Set material
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, self.ambient_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.diffuse_color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 0.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 20)

    def draw(self, from_fixed_frame: bool = True):
        self.opgl_move_to_pose(from_fixed_frame)
        self.apply_material()


class Sphere(Solid):
    def __init__(self, radius: int = 1, *args, **kwargs):
        Solid.__init__(self, *args, **kwargs)
        self.radius = radius

    def draw(self, from_fixed_frame: bool = True):
        self.opgl_move_to_pose(from_fixed_frame)
        self.apply_material()

        # draw sphere
        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad, GLU_FILL)
        gluQuadricTexture(quad, True)
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, self.radius, 20, 20)


class Parallepiped(Solid):
    def __init__(self,
                 length: int = 1,
                 width: int = 1,
                 height: int = 1,
                 *args,
                 **kwargs):
        Solid.__init__(self, *args, **kwargs)
        self.length = length
        self.width = width
        self.height = height

    def draw(self, from_fixed_frame: bool = True):
        self.opgl_move_to_pose(from_fixed_frame)
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
