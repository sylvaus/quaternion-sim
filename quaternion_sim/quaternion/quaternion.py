import numpy as np
from quaternion import rotation_matrix as rotm
from time import time

rad_to_deg = 180.0 / np.pi


class Quaternion(object):
    """
    This quaternion uses the convention cos(theta/2) = q0, sin(theta/2)*axis = [q1, q2, q3]]
    """

    def __init__(self, array: np.ndarray = None, rot_quaternion: bool = False):
        if array is None:
            self.array = np.array([1, 0, 0, 0], dtype=float)

        elif type(array) == np.ndarray:
            assert array.size == 4, 'Quaternion should have a size of 4'
            self.array = array.astype(dtype=float)

        elif type(array) == list:
            assert len(array) == 4, 'Quaternion should have a size of 4'
            self.array = np.array(array, dtype=float)

        else:
            raise ValueError("Cannot make a quaternion from the given type")

    def normalize(self) -> None:
        assert not (np.allclose(self.array, np.array([0, 0, 0, 0], dtype=float))) \
            , "Cannot normalize [0,0,0,0] quaternion"
        self.array = self.array / np.linalg.norm(self.array)

    def inverse(self) -> None:
        self.array[1:4] = -self.array[1:4]

    def get_norm(self) -> float:
        return np.linalg.norm(self.array)

    def get_inverse(self) -> 'Quaternion':
        q0 = np.array(self.array[0])
        qv = -self.array[1:4]
        return Quaternion(np.insert(qv, 0, q0))

    def get_log(self) -> 'Quaternion':
        return quaternion_log(self)

    def get_axis(self) -> np.ndarray:
        return self.array[1:4] / np.linalg.norm(self.array[1:4])

    def get_theta(self, rad: bool = True) -> float:
        if rad:
            return 2.0 * np.arctan2(np.linalg.norm(self.array[1:4]), self.array[0])
        else:
            return 2.0 * np.arctan2(np.linalg.norm(self.array[1:4]), self.array[0]) * rad_to_deg

    def to_rot_matrix(self) -> np.matrix:
        if np.linalg.norm(self.array[1:4]) == 0:
            return np.matrix(np.identity(3))
        else:
            res = rotm.RMatrix_fast(self)
            return res

    def __repr__(self):
        return str(self.array)

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, key, value):
        self.array[key] = value

    def __add__(self, other: "Quaternion"):
        return Quaternion(self.array + other.array)

    def __sub__(self, other: "Quaternion"):
        return Quaternion(self.array - other.array)

    def __mul__(self, other: "Quaternion"):
        q0 = np.array(self.array[0] * other.array[0] - np.dot(self.array[1:4], other.array[1:4]))
        qv = self.array[0] * other.array[1:4] + other.array[0] * self.array[1:4] + \
             np.cross(self.array[1:4], other.array[1:4])
        return Quaternion(np.insert(qv, 0, q0))

    def dot(self, other: "Quaternion",
            unit_quat: bool = False,
            orient_quat: bool = False):

        #TODO finish the implementation
        """
        If the param orient_quat is true then the calculation ensures that the result is a unit quaternion.
        To do so, the term q0 is computed with the formula
            q0 = sqrt(1 - q1^2 - q1^2 - q1^2 - q1^3)
        However, this result is only true if
        """
        if orient_quat:
            q0 = np.array(self.array[0] * other.array[0] - np.dot(self.array[1:4], other.array[1:4]))
            qv = self.array[0] * other.array[1:4] + other.array[0] * self.array[1:4] + \
                 np.cross(self.array[1:4], other.array[1:4])
            return Quaternion(np.insert(qv, 0, q0))
        elif unit_quat:
            q0 = np.array(self.array[0] * other.array[0] - np.dot(self.array[1:4], other.array[1:4]))
            qv = self.array[0] * other.array[1:4] + other.array[0] * self.array[1:4] + \
                 np.cross(self.array[1:4], other.array[1:4])
            return Quaternion(np.insert(qv, 0, q0))
        else:
            q0 = np.array(self.array[0] * other.array[0] - np.dot(self.array[1:4], other.array[1:4]))
            qv = self.array[0] * other.array[1:4] + other.array[0] * self.array[1:4] + \
                 np.cross(self.array[1:4], other.array[1:4])
            return Quaternion(np.insert(qv, 0, q0))


def quaternion_log(quat: Quaternion) -> Quaternion:
    return Quaternion(np.insert(quat.get_theta() * quat.get_axis(), 0, 0))


def quaternion_x(theta: float, rad: bool = True) -> Quaternion:
    if rad:
        return Quaternion([np.cos(theta / 2), np.sin(theta / 2), 0, 0])
    else:
        theta = theta / rad_to_deg
        return Quaternion([np.cos(theta / 2), np.sin(theta / 2), 0, 0])


def quaternion_y(theta: float, rad: bool = True) -> Quaternion:
    if rad:
        return Quaternion([np.cos(theta / 2), 0, np.sin(theta / 2), 0])
    else:
        theta = theta / rad_to_deg
        return Quaternion([np.cos(theta / 2), 0, np.sin(theta / 2), 0])


def quaternion_z(theta: float, rad: bool = True) -> Quaternion:
    if rad:
        return Quaternion([np.cos(theta / 2), 0, 0, np.sin(theta / 2)])
    else:
        theta = theta / rad_to_deg
        return Quaternion([np.cos(theta / 2), 0, 0, np.sin(theta / 2)])


def quaternion_axis_theta(axis: np.ndarray, theta: float, rad: bool = True) -> Quaternion:
    axis_norm = np.linalg.norm(axis)

    if axis_norm == 0:
        theta = 0
    else:
        axis = axis / axis_norm

    if not rad:
        theta = theta / rad_to_deg

    return Quaternion(np.insert(axis * np.sin(theta / 2.0), 0, np.cos(theta / 2.0)))


def quaternion_2_vectors(v1: np.ndarray, v2: np.ndarray) -> Quaternion:
    assert not (np.allclose(v1, np.array([0, 0, 0]))) or \
           not (np.allclose(v2, np.array([0, 0, 0]))) \
        , "One of the vector is a zero vector"

    axis = np.cross(v1, v2)
    v1v2_norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    theta = np.arctan2(np.linalg.norm(axis) / v1v2_norm, np.dot(v1, v2) / v1v2_norm)
    return quaternion_axis_theta(axis, theta)


def _test():
    q = Quaternion()


if __name__ == "__main__":
    _test()
