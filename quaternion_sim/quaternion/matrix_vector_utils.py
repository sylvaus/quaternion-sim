from numpy import matrix, ndarray, dot


def tensor_product(vec_left: ndarray, vec_right: ndarray) -> matrix:
    """
    Return the tensor product of two vectors
    """
    assert vec_left.size == vec_right.size, "the two vectors must have the same size"

    return matrix([[vl * vr for vr in vec_right] for vl in vec_left])


def cross_product_matrix(vec: ndarray) -> matrix:
    """
    Return the cross product matrix of vector vec
    """
    assert vec.size == 3, "the vector must have a size of 3"

    return matrix([[0, -vec[2], vec[1]],
                   [vec[2], 0, -vec[0]],
                   [-vec[1], vec[0], 0]])


def vectorize(vec: ndarray) -> ndarray:
    """
    Return a ndarray of shape (3,1)
    """
    return vec.reshape(3, 1)


def matrix_vector_mul(mat: matrix, vec: ndarray):
    return dot(mat, vec.reshape(3, 1)).reshape(3, 1)
