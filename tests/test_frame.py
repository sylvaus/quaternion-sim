import unittest

from numpy import array, allclose

from quaternion_sim.frames import Frame, FrameManager
from quaternion_sim.geometry.quaternion import Quaternion, quaternion_axis_theta, quaternion_x, \
                                     quaternion_z
from quaternion_sim.geometry.pose import Pose
from quaternion_sim.solids import Solid


class TestFrame(unittest.TestCase):
    def test_translate_frame(self):
        frame = Frame("", Pose(), "")
        frame.translate(array([1, 2, 3]))

        self.assertTrue(allclose(frame.pose.position, array([1, 2, 3]).reshape(3, 1)))

        frame.translate(array([1, 2, 3]))

        self.assertTrue(allclose(frame.pose.position, array([2, 4, 6]).reshape(3, 1)))

    def test_frame_rotate(self):
        frame = Frame("", Pose(), "")

        quat_1 = quaternion_axis_theta(array([1, 1, 0]),
                                       30,
                                       False)
        quat_2 = quaternion_axis_theta(array([1, 0, 1]),
                                       120,
                                       False)
        quat_f = quat_2 * quat_1

        frame.rotate(quat_1)
        self.assertTrue(allclose(frame.pose.orientation.array,
                                 quat_1._array))

        frame.rotate(quat_2)
        self.assertTrue(allclose(frame.pose.orientation.array,
                                 quat_f.array))

    def test_get_frame_seq(self):
        fixed_frame = Frame("fixed", Pose(), "")
        frame_1 = Frame("frame_1", Pose(), "fixed")
        frame_2 = Frame("frame_2", Pose(), "frame_1")
        frame_3 = Frame("frame_3", Pose(), "frame_2")
        frame_4 = Frame("frame_4", Pose(), "fixed")

        frame_mgr = FrameManager(fixed_frame)
        frame_mgr.add_frame(frame_1)
        frame_mgr.add_frame(frame_2)
        frame_mgr.add_frame(frame_3)
        frame_mgr.add_frame(frame_4)

        res = ["frame_3", "frame_2", "frame_1", "fixed"]
        self.assertTrue(res == frame_mgr.get_frame_seq(fixed_frame, frame_3)[0])

        res1 = ["frame_2", "frame_1", "fixed"]
        res2 = ["frame_4", "fixed"]
        self.assertTrue([res1, res2] == frame_mgr.get_frame_seq(frame_4, frame_2))

    def test_solid_pose_in_frame(self):
        vec_x = array([1, 0, 0])
        vec_y = array([0, 1, 0])
        vec_z = array([0, 0, 1])
        vec_null = array([0, 0, 0])

        quat_x = quaternion_x(90, False)
        quat_z = quaternion_z(90, False)
        quat_null = Quaternion()

        fixed_frame = Frame("fixed", Pose(), "")
        frame_1 = Frame("frame_1", Pose(quat_x, vec_z), "fixed")
        frame_2 = Frame("frame_2", Pose(quat_x, vec_z), "frame_1")
        frame_3 = Frame("frame_3", Pose(quat_x, vec_z), "frame_2")
        frame_4 = Frame("frame_4", Pose(quat_null, vec_x), "fixed")
        frame_5 = Frame("frame_5", Pose(quat_z, vec_y), "frame_4")

        frame_mgr = FrameManager(fixed_frame)
        frame_mgr.add_frame(frame_1)
        frame_mgr.add_frame(frame_2)
        frame_mgr.add_frame(frame_3)
        frame_mgr.add_frame(frame_4)
        frame_mgr.add_frame(frame_5)

        solid_1 = Solid("solid_1", pose=Pose(), ref_frame="frame_1")
        pose = frame_mgr.solid_pose_in_frame(solid_1, fixed_frame)
        res = Pose(quaternion_x(90, False), array([0, 0, 1]))
        self.assertTrue(res.is_equal(pose), [res, pose])

        solid_2 = Solid("solid_2", pose=Pose(), ref_frame="frame_1")
        pose = frame_mgr.solid_pose_in_frame(solid_2, fixed_frame)
        res = Pose(quaternion_x(-270, False), array([0, 0, 1]))
        self.assertTrue(res.is_equal(pose), [res, pose])

        solid_3 = Solid("solid_3", pose=Pose(), ref_frame="frame_2")
        pose = frame_mgr.solid_pose_in_frame(solid_3, fixed_frame)
        res = Pose(quaternion_x(180, False), array([0, -1, 1]))
        self.assertTrue(res.is_equal(pose), [res, pose])

        solid_4 = Solid("solid_4", pose=Pose(quat_x, vec_z), ref_frame="frame_3")
        pose = frame_mgr.solid_pose_in_frame(solid_4, fixed_frame)
        res = Pose()
        self.assertTrue(Pose().is_equal(pose), [res, pose])

        res = Pose(Quaternion(), array([-1, 0, 0]))
        pose = frame_mgr.solid_pose_in_frame(solid_4, frame_4)
        self.assertTrue(res.is_equal(pose), [res, pose])

        res = Pose(quaternion_z(-90, False), array([-1, 1, 0]))
        pose = frame_mgr.solid_pose_in_frame(solid_4, frame_5)
        self.assertTrue(res.is_equal(pose), [res, pose])

    def test_get_all_frame_poses(self):
        vec_x = array([1, 0, 0])
        vec_y = array([0, 1, 0])
        vec_z = array([0, 0, 1])
        vec_null = array([0, 0, 0])

        quat_x = quaternion_x(90, False)
        quat_z = quaternion_z(90, False)
        quat_null = Quaternion()

        fixed_frame = Frame("fixed", Pose(), "")
        frame_1 = Frame("frame_1", Pose(quat_x, vec_z), "fixed")
        frame_2 = Frame("frame_2", Pose(quat_x, vec_z), "frame_1")
        frame_3 = Frame("frame_3", Pose(quat_x, vec_z), "frame_2")
        frame_4 = Frame("frame_4", Pose(quat_null, vec_x), "fixed")
        frame_5 = Frame("frame_5", Pose(quat_z, vec_y), "frame_4")

        frame_mgr = FrameManager(fixed_frame)
        frame_mgr.add_frame(frame_1)
        frame_mgr.add_frame(frame_2)
        frame_mgr.add_frame(frame_3)
        frame_mgr.add_frame(frame_4)
        frame_mgr.add_frame(frame_5)

        poses = frame_mgr.get_all_frame_poses()

        pose_frame_1 = Pose(quaternion_axis_theta(vec_x, 90, rad=False),
                            vec_z)
        pose_frame_2 = Pose(quaternion_axis_theta(vec_x, 180, rad=False),
                            vec_z - vec_y)
        pose_frame_3 = Pose(quaternion_axis_theta(vec_x, 270, rad=False),
                            - vec_y)
        pose_frame_4 = Pose(quat_null,
                            vec_x)
        pose_frame_5 = Pose(quaternion_axis_theta(vec_z, 90, rad=False),
                            vec_y + vec_x)
        pose_frame_ref = Pose(quat_null, vec_null)


        self.assertTrue(poses["fixed"].is_equal(pose_frame_ref))
        self.assertTrue(poses["frame_1"].is_equal(pose_frame_1))
        self.assertTrue(poses["frame_2"].is_equal(pose_frame_2))
        self.assertTrue(poses["frame_3"].is_equal(pose_frame_3))
        self.assertTrue(poses["frame_4"].is_equal(pose_frame_4))
        self.assertTrue(poses["frame_5"].is_equal(pose_frame_5))


if __name__ == '__main__':
    unittest.main()
