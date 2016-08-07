from quaternion import *
from vector_utils import *
from cell_phone_connect import *

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Parallelepiped(object):
    def __init__(self,
                 length: float = 1,
                 width: float = 1,
                 height: float = 1,
                 center: np.ndarray = np.array([0, 0, 0]),
                 orientation: Quaternion = Quaternion()):

        # Set the characteristics of the cube
        self.orientation = orientation
        self.center = center
        self.length = length

        # Define the vertices
        theta = np.linspace(np.pi / 4, 2 * np.pi + np.pi / 4, 5)[:4]
        x = length * np.cos(theta)
        y = width * np.sin(theta)
        z = height * np.ones(x.size)

        self.vertices = [vectorize(v) for v in list(zip(x, y, z)) + list(zip(x, y, -z))]

        # Define vertices groups to generate the 6 planes
        self.planes = [[0, 1, 2, 3], [4, 5, 6, 7],
                       [0, 4, 5, 1], [0, 4, 7, 3],
                       [2, 6, 5, 1], [2, 6, 7, 3]]

        # Define the original orientation
        self.orientation_origin = Quaternion()

    def draw(self, axes: Axes3D):
        R = (self.orientation * (self.orientation_origin.inverse())).to_rot_matrix()
        verts = [vectorize(np.dot(R, v)) for v in self.vertices]

        for plane in self.planes:
            collection = Poly3DCollection(
                [[self.center + verts[index] for index in plane]])
            axes.add_collection3d(collection)

    def set_orientation(self, quat: Quaternion):
        self.orientation = quat

    def get_orientation(self) -> Quaternion:
        return self.orientation

    def set_orientation_origin(self, quat: Quaternion):
        self.orientation_origin = quat

    def get_orientation_origin(self) -> Quaternion:
        return self.orientation_origin


class Cube(Parallelepiped):
    def __init__(self,
                 length: float = 1,
                 center: np.ndarray = np.array([0, 0, 0]),
                 orientation: Quaternion = Quaternion()):

        super().__init__(length, length, length, center, orientation)