import numpy as np

def vectorize(array) -> np.ndarray:
    """
    Return an np.ndarray of shape (3,)
    :param array:
    :type array: list or np.ndarray
    :return: np.ndarray
    """

    array = np.array(array)

    if array.shape == (3,1):
        return array.reshape((3,))

    if array.shape == (1,3):
        array = array.transpose()
        return array.reshape((3,))

    return array
