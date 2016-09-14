"""
Dynamic model
ma = f
I w_dot + w^Iw = m
"""
from numpy import matrix, ndarray
from numpy.core.numeric import identity
from quaternion import Quaternion


class Runge_Kutta_45(object):
    def __init__(self,
                 mass: float = 1.0,
                 inertia: matrix = identity(3)):

        self.mass = mass
        self.inertia = inertia

    def compute_next_step(self,
                          t: float,
                          p: ndarray,
                          v: ndarray,
                          quat: Quaternion,
                          w: ndarray,
                          f: ndarray,
                          m: ndarray,
                          F_fp: ndarray):

        # translational part
        for i in range(0,4):
            v = v + f*t/4

        return