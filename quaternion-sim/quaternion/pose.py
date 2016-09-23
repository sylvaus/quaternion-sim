from numpy import ndarray, array
from quaternion.quaternion import Quaternion

class Pose(object):
    def __init__(self,
                 orientation: Quaternion = Quaternion(),
                 position: ndarray = array([0,0,0])):

        self.orientation = orientation

        assert position.shape == (3,) or position.shape == (3,1), \
            "The position should be an array of size (3,1)"

        self.position = position.reshape(3,1)

    def translate(self, translation: ndarray):
        self.position += translation.reshape(3,1)

    def rotate(self, orientation: Quaternion):
        self.orientation *= orientation

    def get_opengl_rot(self):
        return self.orientation.to_opengl_rot()

    def get_opengl_trans(self):
        return self.position[0], self.position[1], self.position[2]


    def __add__(self, pose):
        return Pose(self.orientation * pose.orientation,
                    self.position + pose.position)

    def __sub__(self, pose):
        return Pose(self.orientation * pose.orientation.inverse(),
                    self.position + pose.position)