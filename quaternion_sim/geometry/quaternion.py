from math import acos, cos, sin, atan2, asin
from typing import Union, List
import numpy as np

RAD_TO_DEG = 180.0 / np.pi
DOT_THRESHOLD = 0.9995


def sign(val):
    return 1 if val >= 0.0 else -1


class Quaternion(object):
    """
    This geometry uses the convention cos(theta/2) = q0, sin(theta/2)*axis = [q1, q2, q3]]
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
            raise ValueError("Cannot make a geometry from the given type")

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

    w = q0
    x = q1
    y = q2
    z = q3

    def normalize(self) -> None:
        """
        Normalize Quaternion
        :return: None
        """
        if np.allclose(self._array, np.array([0, 0, 0, 0], dtype=float)):
            self._array = np.array([1, 0, 0, 0], dtype=float)
        else:
            self._array = self._array / np.linalg.norm(self._array)

    def inverse(self) -> None:
        """
        Inverse Quaternion
        :return: None
        """
        self._array[1:4] = -self._array[1:4]

    def get_norm(self) -> float:
        """
        Returns Quaternion norm
        :return: float
        """
        return np.linalg.norm(self._array)

    def get_inverse(self) -> 'Quaternion':
        """
        Returns Quaternion's inverse
        :return: Quaternion
        """
        q0 = np.array(self._array[0])
        qv = -self._array[1:4]
        return Quaternion(np.insert(qv, 0, q0))

    def get_log(self) -> 'Quaternion':
        """
        Returns Quaternion's log
        :return: Quaternion
        """
        return quaternion_log(self)

    def get_axis(self) -> np.ndarray:
        """
        Returns Quaternion's axis
        :return: numpy.ndarray
        """
        if np.allclose(self._array, np.array([0, 0, 0], dtype=float)):
            return np.array([1, 0, 0], dtype=float)
        else:
            return self._array[1:4] / np.linalg.norm(self._array[1:4])

    def get_theta(self, rad: bool = True) -> float:
        """
        Returns Quaternion theta's angle (range [-PI .. PI])
        :param rad: if true returns radians otherwise degrees
        :return: float
        """
        if rad:
            return 2.0 * acos(self._array[0])
        else:
            return 2.0 * acos(self._array[0]) * RAD_TO_DEG

    def get_normalized(self) -> "Quaternion":
        """
        Returns normalized geometry
        :return: Quaternion
        """
        if np.allclose(self._array, np.array([0, 0, 0, 0], dtype=float)):
            return Quaternion.identity()
        else:
            return Quaternion(self._array / np.linalg.norm(self._array))

    def to_rot_matrix(self) -> np.matrix:
        """
        Returns rotation matrix corresponding to the Quaternion
        :return: numpy.matrix
        """
        if np.linalg.norm(self._array[1:4]) == 0:
            return np.matrix(np.identity(3))
        else:
            q1q0 = self._array[1] * self._array[0]
            q2q0 = self._array[2] * self._array[0]
            q3q0 = self._array[3] * self._array[0]
            q1q1 = self._array[1] * self._array[1]
            q2q1 = self._array[2] * self._array[1]
            q3q1 = self._array[3] * self._array[1]
            q2q2 = self._array[2] * self._array[2]
            q3q2 = self._array[3] * self._array[2]
            q3q3 = self._array[3] * self._array[3]

            return np.matrix([[1 - 2 * (q2q2 + q3q3), 2 * (q2q1 - q3q0), 2 * (q3q1 + q2q0)],
                              [2 * (q2q1 + q3q0), 1 - 2 * (q1q1 + q3q3), 2 * (q3q2 - q1q0)],
                              [2 * (q3q1 - q2q0), 2 * (q3q2 + q1q0), 1 - 2 * (q1q1 + q2q2)]])

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
            qv = self._array[0] * other._array[1:4] + other._array[0] * self._array[1:4]\
                 + np.cross(self._array[1:4], other._array[1:4])
            return Quaternion(np.insert(qv, 0, q0))
        else:
            return Quaternion(self._array * other)

    def __rmul__(self, other: Union["Quaternion", float]):
        if type(other) == type(self):
            q0 = np.array(self._array[0] * other._array[0] - np.dot(self._array[1:4], other._array[1:4]))
            qv = self._array[0] * other._array[1:4] + other._array[0] * self._array[1:4]\
                 + np.cross(self._array[1:4], other._array[1:4])
            return Quaternion(np.insert(qv, 0, q0))
        else:
            return Quaternion(self._array * other)

    def __neg__(self):
        return Quaternion(-self._array)

    def __eq__(self, other: "Quaternion") -> bool:
        return np.allclose(self._array, other._array)

    def dot(self, other: "Quaternion") -> float:
        """
        Return geometry dot product
        :param other: Quaternion
        :return: float
        """
        return np.asscalar(np.dot(self._array, other._array))

    @staticmethod
    def identity() -> "Quaternion":
        """
        Returns Quaternion corresponding to Identity rotation
        :return: Quaternion
        """
        return Quaternion(np.array([1, 0, 0, 0], dtype=float))

    def to_euler_angles(self):
        """
        Quaternion to Euler Angles [roll, pitch, yaw] based on 
        https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles#Quaternion_to_Euler_Angles_Conversion
        :return: [roll, pitch, yaw]
        """
        y2 = self._array[2] ** 2

        sin_roll = +2.0 * (self._array[0] * self._array[1] + self._array[2] * self._array[3])
        cos_roll = +1.0 - 2.0 * ((self._array[1] ** 2) + y2)
        roll = atan2(sin_roll, cos_roll)

        sin_pitch = +2.0 * (self._array[0] * self._array[2] - self._array[3] * self._array[1])
        sin_pitch = sign(sin_pitch) if abs(sin_pitch) > 1 else sin_pitch
        pitch = asin(sin_pitch)

        sin_yaw = +2.0 * (self._array[0] * self._array[3] + self._array[1] * self._array[2])
        cos_yaw = +1.0 - 2.0 * (y2 + self._array[3] * self._array[3])
        yaw = atan2(sin_yaw, cos_yaw)

        return [roll, pitch, yaw]

    @staticmethod
    def from_euler_angles(roll: float, pitch: float, yaw: float) -> "Quaternion":
        """
        Euler angles to quaternion based on
        https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles#Euler_Angles_to_Quaternion_Conversion
        :param roll:
        :param pitch:
        :param yaw:
        :return: Quaternion
        """
        cy = cos(yaw * 0.5)
        sy = sin(yaw * 0.5)
        cr = cos(roll * 0.5)
        sr = sin(roll * 0.5)
        cp = cos(pitch * 0.5)
        sp = sin(pitch * 0.5)

        return Quaternion([cy * cr * cp + sy * sr * sp,
                           cy * sr * cp - sy * cr * sp,
                           cy * cr * sp + sy * sr * cp,
                           sy * cr * cp - cy * sr * sp])


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
           not (np.allclose(v2, np.array([0, 0, 0]))), \
           "One of the vector is a zero vector"

    axis = np.cross(v1, v2)
    v1v2_norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    theta = np.arctan2(np.linalg.norm(axis) / v1v2_norm, np.dot(v1, v2) / v1v2_norm)
    return quaternion_axis_theta(axis, theta)


def dot_product(quat_left: Quaternion, quat_right: Quaternion) -> float:
    return quat_left.dot(quat_right)


def lerp(quat_start: Quaternion, quat_end: Quaternion, coeff: float) -> Quaternion:
    """
    Linear interpolation
    :param quat_start: Start geometry
    :param quat_end: End Quaternion
    :param coeff: Interpolation coefficient
    :return: Quaternion
    """
    return (quat_start * (1 - coeff)) + (quat_end * coeff)


def nlerp(quat_start: Quaternion, quat_end: Quaternion, coeff: float) -> Quaternion:
    """
    Normalized linear interpolation
    :param quat_start: Start geometry
    :param quat_end: End Quaternion
    :param coeff: Interpolation coefficient
    :return: Quaternion
    """
    result = (quat_start * (1 - coeff)) + (quat_end * coeff)
    result.normalize()
    return result


def slerp(quat_start: Quaternion, quat_end: Quaternion, coeff: float, shortest_path: bool = False) -> Quaternion:
    """
    Spherical Linear Interpolation inspired by C++ code presented there: https://en.wikipedia.org/wiki/Slerp
    :param quat_start: Start geometry
    :param quat_end: End Quaternion
    :param coeff: Interpolation coefficient
    :param shortest_path: Takes the shortest path between the two orientations
    :return: Quaternion
    """
    quat_start = quat_start.get_normalized()
    quat_end = quat_end.get_normalized()
    dot = dot_product(quat_start, quat_end)

    if abs(dot) > DOT_THRESHOLD:
        return nlerp(quat_start, quat_end, coeff)

    if shortest_path and (dot < 0.0):
        dot = -dot
        quat_end = -quat_end

    dot = dot if abs(dot) <= 1 else sign(dot)  # constrain dot to 1 .. -1 for acos
    delta_angle = acos(dot) * coeff

    quat_end_normal = quat_end - quat_start * dot  # geometry normal to quat_start in quat_start quat_end plan
    quat_end_normal.normalize()

    return quat_end_normal * sin(delta_angle) + quat_start * cos(delta_angle)


def log_interpolation(quat_start: Quaternion, quat_end: Quaternion, coeff: float) -> Quaternion:
    """
    Logarithmic Quaternion Interpolation
    :param quat_start: Start geometry
    :param quat_end: End Quaternion
    :param coeff: Interpolation coefficient
    :return: Quaternion
    """
    delta_quat = quat_end * (quat_start.get_inverse())
    angle = delta_quat.get_theta()

    return quaternion_axis_theta(delta_quat.get_axis(), angle * coeff) * quat_start
