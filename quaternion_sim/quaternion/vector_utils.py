from numpy import ndarray, array, matrix, dot


def vectorize(vec: ndarray) -> ndarray:
    """
    Return an np.ndarray of shape (3,1)
    :param array:
    :type array: ndarray
    :return: ndarray
    """
    return vec.reshape(3,1)


def matrix_vector_mul(mat: matrix, vec: array):
    return dot(mat, vec.reshape(3,1)).reshape(3, 1)

