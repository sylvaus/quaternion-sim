from cellphone_utils.cellphone_connect import *
from mpl_toolkits.mplot3d import Axes3D


class Sphere(object):
    def __init__(self,
                 radius: float = 1,
                 center: np.ndarray = np.array([0, 0, 0]),
                 orientation: Quaternion = Quaternion()):

        self.orientation = orientation
        self.center = center
        self.radius = radius

        # Define the original orientation
        self.orientation_origin = Quaternion()

        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)

        self.x = 10 * np.outer(np.cos(u), np.sin(v))
        self.y = 10 * np.outer(np.sin(u), np.sin(v))
        self.z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

    def draw(self, axes: Axes3D):
        R = (self.orientation * (self.orientation_origin.inverse())).to_rot_matrix()

        xx = R[0,0]*self.x + R[0,1]*self.y + R[0,2]*self.z
        yy = R[1,0]*self.x + R[1,1]*self.y + R[1,2]*self.z
        zz = R[2,0]*self.x + R[2,1]*self.y + R[2,2]*self.z

        axes.plot_surface(xx, yy, zz, rstride=4, cstride=4, color='b')
        return axes,

    def set_orientation(self, quat: Quaternion):
        self.orientation = quat

    def get_orientation(self) -> Quaternion:
        return self.orientation

    def set_orientation_origin(self, quat: Quaternion):
        self.orientation_origin = quat

    def get_orientation_origin(self) -> Quaternion:
        return self.orientation_origin