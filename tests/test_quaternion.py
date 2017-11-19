import unittest
from math import sqrt
from quaternion_sim.geometry.quaternion import Quaternion, slerp

class TestQuaternion(unittest.TestCase):
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
            //Your code goes here
            float val = 1.0f / (float)Math.Sqrt(2);
            Quaternion quat = Quaternion.Slerp(new Quaternion(val, 0, val, 0), new Quaternion(0, val, 0, val), 0.5f);
            Console.WriteLine(quat);
        }
    }
    """
    def test_slerp(self):
        val = 1.0 / sqrt(2)
        self.assertTrue(slerp(Quaternion([val, 0, val, 0]), Quaternion([0, val, 0, val]), 0.5)
                        == Quaternion([0.5, 0.5, 0.5, 0.5]))

if __name__ == '__main__':
    unittest.main()