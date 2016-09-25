import unittest

from frames import Frame, FrameManager
from quaternion.quaternion import Quaternion
from quaternion.pose import Pose
from numpy import array, allclose

class TestFrame(unittest.TestCase):
    def test_translate_frame(self):
        frame = Frame("", Pose(), "")
        frame.translate(array([1,2,3]))

        self.assertTrue(allclose(frame.pose.position, array([1, 2, 3]).reshape(3,1)))

        frame.translate(array([1, 2, 3]))

        self.assertTrue(allclose(frame.pose.position, array([2, 4, 6]).reshape(3,1)))

    def test_frame_rotate(self):
        frame = Frame("", Pose(), "")
        

    """
    def test_solid_pose_in_frame(self):

        fixed_frame = Frame("fixed", Pose(), "")
        self.assertTrue(False)
    """

if __name__ == '__main__':
    unittest.main()