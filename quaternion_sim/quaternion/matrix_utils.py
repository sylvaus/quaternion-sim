import numpy as np


def tensor_product(vec_left, vec_right):
    """
    Return the tensor product of two vectors
    :param vec_left:
    :type vec_left: np.ndarray
    :param vec_right:
    :type vec_right: np.ndarray
    :return:
    """
    assert vec_left.size == vec_right.size, "the two vectors must have the same size"

    return np.matrix([[vl * vr for vr in vec_right] for vl in vec_left])


def cross_product_matrix(vec):
    """
    Return the cross product matrix of vector vec
    :param vec:
    :type vec: np.ndarray
    :return:
    """
    assert vec.size == 3, "the vector must have a size of 3"

    return np.matrix([[0, -vec[2], vec[1]],
                      [vec[2], 0, -vec[0]],
                      [-vec[1], vec[0], 0]])
