from numpy import ndarray, array, matrix, dot

def vectorize(array: ndarray) -> ndarray:
    """
    Return an np.ndarray of shape (3,)
    :param array:
    :type array: ndarray
    :return: ndarray
    """

    if array.shape == (3,1):
        return array.reshape((3,))

    if array.shape == (1,3):
        array = array.transpose()
        return array.reshape((3,))

    return array

def matrix_vector_mul(mat: matrix, vect: array):
    return vectorize(dot(mat,vect))
