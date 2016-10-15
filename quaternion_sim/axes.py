from OpenGL.GL import glLoadIdentity, glTranslatef, glRotatef, glMaterialfv, \
                        glMaterialf, GL_FRONT_AND_BACK, GL_AMBIENT, GL_DIFFUSE, \
                        GL_SPECULAR, GL_SHININESS
from OpenGL.GLU import gluNewQuadric, gluQuadricDrawStyle, gluQuadricTexture, \
                        gluQuadricNormals, gluCylinder, GLU_FILL, GLU_SMOOTH

from frames import Frame
from quaternion.quaternion import quaternion_x, quaternion_y, Quaternion


class Axis(object):
    def __init__(self, frame: Frame, size: float=1):

        self.frame = frame
        self.size = size
        self.colors = [[1.0, 0.0, 0.0, 0],
                       [0.0, 1.0, 0.0, 0],
                       [0.0, 0.0, 1.0, 0]]

        self.rots = [quaternion_x(-90, False),
                     quaternion_y(90, False),
                     Quaternion()]

    def draw(self, from_fixed_frame: bool = True):
        if from_fixed_frame:
            # Reset init view
            glLoadIdentity()

        # Translate to the right position
        glTranslatef(self.frame.pose.position[0],
                     self.frame.pose.position[1],
                     self.frame.pose.position[2])

        # Rotate to the right orientation
        self.glRotateQ(self.frame.pose.orientation)

        for i in range(0, 3):
            self.draw_arrow(self.colors[i])
            self.glRotateQ(self.rots[i])


    def draw_arrow(self, color):

        # Set material
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, color)
        #glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)
        #glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 0.0])
        #glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 20)

        # Draw cylinder
        quad = gluNewQuadric()
        gluQuadricDrawStyle(quad, GLU_FILL)
        gluQuadricTexture(quad, True)
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluCylinder(quad, self.size / 30, self.size / 30,
                    self.size * 0.8, 20, 20)

        # Move to the arrowhead position
        glTranslatef(0, 0, self.size * 0.8)

        # Draw arrowhead
        gluQuadricDrawStyle(quad, GLU_FILL)
        gluQuadricTexture(quad, True)
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluCylinder(quad, self.size / 15, 0,
                    self.size * 0.2, 20, 20)

        # Revert to the original position
        glTranslatef(0, 0, -self.size * 0.8)

    @staticmethod
    def glRotateQ(quat: Quaternion):
        glRotatef(quat.get_theta(rad=False),
                  quat[1],
                  quat[2],
                  quat[3])
