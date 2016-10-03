import numpy as np
from numpy import cos, sin, matrix, ndarray

from quaternion.matrix_vector_utils import tensor_product, cross_product_matrix


def RxMatrix(theta: float) -> float:
    """
    Return the rotation matrix about the x-axis with an angle of theta(rad)
    :param theta:
    :return: np.matrix
    """
    return np.matrix([[1.0, 0, 0],
                      [0, cos(theta), -sin(theta)],
                      [0, sin(theta), cos(theta)]])


def RyMatrix(theta: float) -> float:
    """
    Return the rotation matrix about the z-axis with an angle of theta(rad)
    """
    return np.matrix([[cos(theta), 0, sin(theta)],
                      [0, 1.0, 0],
                      [-sin(theta), 0, cos(theta)]])


def RzMatrix(theta: float) -> matrix:
    """
    Return the rotation matrix about the y-axis with an angle of theta(rad)
    """
    return np.matrix([[cos(theta), sin(theta), 0],
                      [sin(theta), cos(theta), 0],
                      [0, 0, 1]])


def RMatrix(axis: ndarray, theta: float, quat) -> matrix:
    """
    Return the rotation matrix about the axis with an angle of theta(rad)
    """
    if np.linalg.norm(axis) == 0:
        return matrix(np.identity(3))
    else:
        axis = axis / np.linalg.norm(axis)
        return cos(theta) * np.identity(3) + \
               sin(theta) * cross_product_matrix(axis) + \
               (1.0 - cos(theta)) * tensor_product(axis, axis)


def RMatrix_fast(quat: 'Quaternion') -> matrix:
    """
    Return the rotation matrix corresponding to the quaternion
    without verifying that the axis norm is not zero
    """
    q0q0 = quat[0] * quat[0]
    q1q0 = quat[1] * quat[0]
    q2q0 = quat[2] * quat[0]
    q3q0 = quat[3] * quat[0]
    q1q1 = quat[1] * quat[1]
    q2q1 = quat[2] * quat[1]
    q3q1 = quat[3] * quat[1]
    q2q2 = quat[2] * quat[2]
    q3q2 = quat[3] * quat[2]
    q3q3 = quat[3] * quat[3]

    # TODO Finish implementation of RMatrix_fast (look at the formula on wiki)

    # return matrix([[, , ],
    #              [, , ]
    #              [, , ]])
