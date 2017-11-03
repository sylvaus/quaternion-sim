from quaternion.pose import Pose
from frames import Frame, FrameManager
from solids import Sphere, Parallepiped
from numpy import array
from time import time

VEC_X = array([1, 0, 0]).astype(dtype=float).reshape(3, 1)
VEC_Y = array([0, 1, 0]).astype(dtype=float).reshape(3, 1)
VEC_Z = array([0, 0, 1]).astype(dtype=float).reshape(3, 1)

class DynamicsBallAndPlate(object):
    def __init__(self):

        self.time = time()

    def compute_next_ball_pose(self,
                               ball: Sphere,
                               plate: Parallepiped,
                               frame_mgr: FrameManager,
                               gravity: float = -9.81) -> None:

        if time is None:
            self.time = time()

        d_time = time() - self.time

        vec_normal = plate.pose.orientation.to_rot_matrix() * VEC_Z

        accel = gravity * array([vec_normal[0],
                                 vec_normal[1],
                                 0]).astype(dtype=float).reshape(3, 1)

        ball.vel = ball.vel + d_time * accel

        ball.translate(d_time * ball.vel)
