import unittest
from math import sqrt
import numpy as np
from quaternion_sim.geometry.quaternion import Quaternion, slerp


class TestQuaternion(unittest.TestCase):
    def test_constructors(self):
        quat = Quaternion()
        self.assertEqual(quat.q0, 1)
        self.assertEqual(quat.q1, 0)
        self.assertEqual(quat.q2, 0)
        self.assertEqual(quat.q3, 0)

        quat = Quaternion([1, 2, 3, 4])
        self.assertEqual(quat.q0, 1)
        self.assertEqual(quat.q1, 2)
        self.assertEqual(quat.q2, 3)
        self.assertEqual(quat.q3, 4)

        quat = Quaternion(np.array([1, 2, 3, 4]))
        self.assertEqual(quat.q0, 1)
        self.assertEqual(quat.q1, 2)
        self.assertEqual(quat.q2, 3)
        self.assertEqual(quat.q3, 4)

    def test_neg(self):
        quat = -Quaternion([1, 2, 3, 4])
        self.assertEqual(quat.q0, -1)
        self.assertEqual(quat.q1, -2)
        self.assertEqual(quat.q2, -3)
        self.assertEqual(quat.q3, -4)

    def test_inverse(self):
        quat = Quaternion([1, 2, 3, 4])
        quat.inverse()
        self.assertEqual(quat.q0, 1)
        self.assertEqual(quat.q1, -2)
        self.assertEqual(quat.q2, -3)
        self.assertEqual(quat.q3, -4)

    def test_scalar_mult(self):
        quat = Quaternion([1, 2, 3, 4])
        quat = 2.0 *  quat
        self.assertEqual(quat.q0, 2)
        self.assertEqual(quat.q1, 4)
        self.assertEqual(quat.q2, 6)
        self.assertEqual(quat.q3, 8)

        quat = Quaternion([1, 2, 3, 4])
        quat = quat * (-2.0)
        self.assertEqual(quat.q0, -2)
        self.assertEqual(quat.q1, -4)
        self.assertEqual(quat.q2, -6)
        self.assertEqual(quat.q3, -8)

    def test_quat_mult(self):
        quat_left = Quaternion([1, 2, 3, 4])
        quat_right = Quaternion([5, -6, 7, -8])
        quat = quat_left * quat_right
        self.assertEqual(quat.q0, 28)
        self.assertEqual(quat.q1, -48)
        self.assertEqual(quat.q2, 14)
        self.assertEqual(quat.q3, 44)


    def test_slerp(self):
        """
        Got expected results value using the following C# code:
        using System;
        using System.Collections.Generic;
        using System.Linq;
        using System.Text.RegularExpressions;
        using System.Numerics;

        public class Program
        {
            public static void Main(string[] args)
            {
                // Careful the C# takes X, Y, Z, W and the python constructor takes W, X, Y, Z
                float val = 1.0f / (float)Math.Sqrt(2);
                Quaternion quat = Quaternion.Slerp(new Quaternion(val, 0, val, 0), new Quaternion(0, val, 0, val), 0.5f);
                Console.WriteLine(quat);
            }
        }
        """
        val = 1.0 / sqrt(2)
        self.assertEqual(slerp(Quaternion([0, val, 0, val]), Quaternion([val, 0, val, 0]), 0.5),
                         Quaternion([0.5, 0.5, 0.5, 0.5]))
        self.assertEqual(slerp(Quaternion([0, val, 0, val]), Quaternion([val, 0, val, 0]), 0.1),
                         Quaternion([0.1106159, 0.6984012, 0.1106159, 0.6984012]))
        self.assertEqual(slerp(Quaternion([0, -val, 0, -val]), Quaternion([val, 0, val, 0]), 0.1),
                         Quaternion([0.1106159, -0.6984012, 0.1106159, -0.6984012]))
        self.assertEqual(slerp(Quaternion([0, -val, 0, -val]), Quaternion([val, 0, val, 0]), 0.7),
                         Quaternion([0.6300368, -0.3210198, 0.6300368, -0.3210198]))

        self.assertEqual(slerp(Quaternion([0, -val, -val, 0]), Quaternion([val, 0, val, 0]), 0.7, True),
                         Quaternion([-0.5463428, -0.2523113, -0.7986541, 0]))


if __name__ == '__main__':
    unittest.main()
