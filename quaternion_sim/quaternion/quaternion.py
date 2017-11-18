import numpy as np
from typing import Union, List
from . import rotation_matrix as rotm

RAD_TO_DEG = 180.0 / np.pi


class Quaternion(object):
    """
    This quaternion uses the convention cos(theta/2) = q0, sin(theta/2)*axis = [q1, q2, q3]]
    """

    def __init__(self, array: Union[np.ndarray, List[float]] = None):
        if array is None:
            self._array = np.array([1, 0, 0, 0], dtype=float)

        elif type(array) == np.ndarray:
            assert array.size == 4, 'Quaternion should have a size of 4'
            self._array = array.astype(dtype=float)

        elif type(array) == list:
            assert len(array) == 4, 'Quaternion should have a size of 4'
            self._array = np.array(array, dtype=float)

        else:
            raise ValueError("Cannot make a quaternion from the given type")

    @property
    def q0(self):
        return self._array[0]

    @property
    def q1(self):
        return self._array[1]

    @property
    def q2(self):
        return self._array[2]

    @property
    def q3(self):
        return self._array[3]

    def normalize(self) -> None:
        if(np.allclose(self._array, np.array([0, 0, 0, 0], dtype=float))):
            self._array = np.array([1, 0, 0, 0], dtype=float)
        else:
            self._array = self._array / np.linalg.norm(self._array)

    def inverse(self) -> None:
        self._array[1:4] = -self._array[1:4]

    def get_norm(self) -> float:
        return np.linalg.norm(self._array)

    def get_inverse(self) -> 'Quaternion':
        q0 = np.array(self._array[0])
        qv = -self._array[1:4]
        return Quaternion(np.insert(qv, 0, q0))

    def get_log(self) -> 'Quaternion':
        return quaternion_log(self)

    def get_axis(self) -> np.ndarray:
        return self._array[1:4] / np.linalg.norm(self._array[1:4])

    def get_theta(self, rad: bool = True) -> float:
        if rad:
            return 2.0 * np.arctan2(np.linalg.norm(self._array[1:4]), self._array[0])
        else:
            return 2.0 * np.arctan2(np.linalg.norm(self._array[1:4]), self._array[0]) * RAD_TO_DEG

    def get_normalized(self) -> "Quaternion":
        if(np.allclose(self._array, np.array([0, 0, 0, 0], dtype=float))):
            return Quaternion.identity()
        else:
            return Quaternion(self._array / np.linalg.norm(self._array))

    def to_rot_matrix(self) -> np.matrix:
        if np.linalg.norm(self._array[1:4]) == 0:
            return np.matrix(np.identity(3))
        else:
            res = rotm.RMatrix_fast(self)
            return res

    def __repr__(self):
        return str(self._array)

    def __getitem__(self, item):
        return self._array[item]

    def __setitem__(self, key, value):
        self._array[key] = value

    def __add__(self, other: "Quaternion"):
        return Quaternion(self._array + other._array)

    def __sub__(self, other: "Quaternion"):
        return Quaternion(self._array - other._array)

    def __mul__(self, other: Union["Quaternion", float]):
        if type(other) == type(self):
            q0 = np.array(self._array[0] * other._array[0] - np.dot(self._array[1:4], other._array[1:4]))
            qv = self._array[0] * other._array[1:4] + other._array[0] * self._array[1:4] + \
                 np.cross(self._array[1:4], other._array[1:4])
            return Quaternion(np.insert(qv, 0, q0))
        elif (type(other) == float) or (type(other) == int):
            return Quaternion(self._array * other)

    def __rmul__(self, other: Union["Quaternion", float]):
        if type(other) == type(self):
            q0 = np.array(self._array[0] * other._array[0] - np.dot(self._array[1:4], other._array[1:4]))
            qv = self._array[0] * other._array[1:4] + other._array[0] * self._array[1:4] + \
                 np.cross(self._array[1:4], other._array[1:4])
            return Quaternion(np.insert(qv, 0, q0))
        elif (type(other) == float) or (type(other) == int):
            return Quaternion(self._array * other)

    def dot(self, other: "Quaternion",
            unit_quat: bool = False):
        """
        If the param unit_quat is true then the calculation ensures that the result is a unit quaternion.
        """
        if unit_quat:
            q0 = np.array(self._array[0] * other._array[0] - np.dot(self._array[1:4], other._array[1:4]))
            qv = self._array[0] * other._array[1:4] + other._array[0] * self._array[1:4] + \
                 np.cross(self._array[1:4], other._array[1:4])

            result = Quaternion(np.insert(qv, 0, q0))
            result.normalize()
            return result
        else:
            q0 = np.array(self._array[0] * other._array[0] - np.dot(self._array[1:4], other._array[1:4]))
            qv = self._array[0] * other._array[1:4] + other._array[0] * self._array[1:4] + \
                 np.cross(self._array[1:4], other._array[1:4])
            return Quaternion(np.insert(qv, 0, q0))

    @staticmethod
    def identity() -> "Quaternion":
        return Quaternion(np.array([1, 0, 0, 0], dtype=float))


def quaternion_log(quat: Quaternion) -> Quaternion:
    return Quaternion(np.insert(quat.get_theta() * quat.get_axis(), 0, [0]))


def quaternion_x(theta: float, rad: bool = True) -> Quaternion:
    if rad:
        return Quaternion(np.array([np.cos(theta / 2), np.sin(theta / 2), 0, 0]))
    else:
        theta = theta / RAD_TO_DEG
        return Quaternion(np.array([np.cos(theta / 2), np.sin(theta / 2), 0, 0]))


def quaternion_y(theta: float, rad: bool = True) -> Quaternion:
    if rad:
        return Quaternion(np.array([np.cos(theta / 2), 0, np.sin(theta / 2), 0]))
    else:
        theta = theta / RAD_TO_DEG
        return Quaternion(np.array([np.cos(theta / 2), 0, np.sin(theta / 2), 0]))


def quaternion_z(theta: float, rad: bool = True) -> Quaternion:
    if rad:
        return Quaternion(np.array([np.cos(theta / 2), 0, 0, np.sin(theta / 2)]))
    else:
        theta = theta / RAD_TO_DEG
        return Quaternion(np.array([np.cos(theta / 2), 0, 0, np.sin(theta / 2)]))


def quaternion_axis_theta(axis: np.ndarray, theta: float, rad: bool = True) -> Quaternion:
    axis_norm = np.linalg.norm(axis)

    if axis_norm == 0:
        theta = 0
    else:
        axis = axis / axis_norm

    if not rad:
        theta = theta / RAD_TO_DEG

    return Quaternion(np.insert(axis * np.sin(theta / 2.0), 0, np.cos(theta / 2.0)))


def quaternion_2_vectors(v1: np.ndarray, v2: np.ndarray) -> Quaternion:
    assert not (np.allclose(v1, np.array([0, 0, 0]))) or \
           not (np.allclose(v2, np.array([0, 0, 0]))) \
        , "One of the vector is a zero vector"

    axis = np.cross(v1, v2)
    v1v2_norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    theta = np.arctan2(np.linalg.norm(axis) / v1v2_norm, np.dot(v1, v2) / v1v2_norm)
    return quaternion_axis_theta(axis, theta)


def lerp(quat_start: Quaternion, quat_end: Quaternion, coeff: float) -> Quaternion:
    return (quat_start * (1 - coeff)) + (quat_end * coeff)


def nlerp(quat_start: Quaternion, quat_end: Quaternion, coeff: float) -> Quaternion:
    result = (quat_start * (1 - coeff)) + (quat_end * coeff)
    result.normalize()
    return result


def slerp(quat_start: Quaternion, quat_end: Quaternion, coeff: float) -> Quaternion:

    pass  # TODO


def log_interpolation(quat_start: Quaternion, quat_end: Quaternion, coeff: float) -> Quaternion:
    pass  # TODO
