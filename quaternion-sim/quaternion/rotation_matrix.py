import numpy as np
from numpy import cos, sin

from quaternion.matrix_utils import tensor_product, cross_product_matrix


def RxMatrix(theta):
    """
    Return the rotation matrix about the x-axis with an angle of theta(rad)
    :param theta:
    :return: np.matrix
    """
    return np.matrix([[1.0, 0, 0],
                      [0, cos(theta), -sin(theta)],
                      [0, sin(theta), cos(theta)]])


def RyMatrix(theta):
    """
    Return the rotation matrix about the z-axis with an angle of theta(rad)
    :param theta:
    :return: np.matrix
    """
    return np.matrix([[cos(theta), 0, sin(theta)],
                      [0, 1.0, 0],
                      [-sin(theta), 0, cos(theta)]])


def RzMatrix(theta):
    """
    Return the rotation matrix about the y-axis with an angle of theta(rad)
    :param theta:
    :return: np.matrix
    """
    return np.matrix([[cos(theta), sin(theta), 0],
                      [sin(theta), cos(theta), 0],
                      [0, 0, 1]])


def RMatrix(axis, theta):
    """
    Return the rotation matrix about the axis with an angle of theta(rad)
    :param axis:
    :param theta:
    :return: np.matrix
    """
    if np.linalg.norm(axis) == 0:
        return np.identity(3)
    else:
        axis /= np.linalg.norm(axis)
        return cos(theta) * np.identity(3) + \
               sin(theta) * cross_product_matrix(axis) + \
               (1.0 - cos(theta)) * tensor_product(axis, axis)
