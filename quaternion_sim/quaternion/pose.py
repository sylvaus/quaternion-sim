from numpy import ndarray, array, allclose
from quaternion.quaternion import Quaternion


class Pose(object):
    def __init__(self,
                 orientation: Quaternion = Quaternion(),
                 position: ndarray = array([0, 0, 0], dtype=float)) -> None:

        self.orientation = orientation

        assert position.shape == (3,) or position.shape == (3, 1), \
            "The position should be an array of size (3,1)"
        self.position = position.astype(dtype=float).reshape(3, 1)

    def translate(self, translation: ndarray) -> None:
        self.position += translation.astype(float).reshape(3, 1)

    def rotate(self, orientation: Quaternion) -> None:
        self.orientation = orientation * self.orientation

    def inverse(self) -> 'Pose':
        return Pose(self.orientation.get_inverse(), -1 * self.position)

    def is_equal(self, pose: 'Pose') -> 'Pose':
        """
        return True if the two poses are equal
        The rotation matrices are compared for the quaternion  due to
        the fact that the 2 quaternions [1,0,0,0] and [-1,0,0,0]
        represent the same rotation (identity)
        """
        if allclose(self.position, pose.position) and \
                allclose(self.orientation.to_rot_matrix(),
                         pose.orientation.to_rot_matrix(), 10**(-10), 10**(-10)):
            return True
        else:
            return False

    def __repr__(self):
        return "position: {0} \norientation: {1}".format(str(self.position.reshape(1, 3)),
                                                         str(self.orientation))

    def __add__(self, pose):
        return Pose(self.orientation * pose.orientation,
                    self.position + pose.position)

    def __sub__(self, pose):
        return Pose(self.orientation * pose.orientation.get_inverse(),
                    self.position + pose.position)
