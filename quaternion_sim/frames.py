from quaternion.pose import Pose
from quaternion.pose import Quaternion
from numpy import array
from typing import List, Dict

class Frame(object):
    def __init__(self, name: str, pose: Pose, ref_frame: str="") -> None:
        self.name = name
        self.pose = pose
        self.ref_frame = ref_frame

    def translate(self, vector) -> None:
        self.pose.translate(vector)

    def rotate(self, quat: Quaternion) -> None:
        self.pose.rotate(quat)


class FrameManager(object):
    def __init__(self, fixed_frame: Frame) -> None:
        """
        The FrameManager is managing all the frames and allows to
        quickly express a pose in any frame.
        It has to be initialized by the inertial fixed frame
        """

        self.frames = {fixed_frame.name: fixed_frame}
        self.depth_frame_dict = {0: [fixed_frame.name]}
        self.frame_depth_dict = {fixed_frame.name: 0}
        self.fixed_frame = fixed_frame
        self.max_depth = 1

    def add_frame(self, frame: Frame) -> None:
        """
        add_frame adds the frame to the frames list and check if the frame is already present
        or if its reference frame is not present
        """

        if frame.ref_frame in self.frames:
            if frame.name in self.frames:
                raise Exception("The frame \"{0}\" already exists".format(frame.ref_frame))
            else:
                self.frames[frame.name] = frame

                depth = 1 + self.frame_depth_dict[frame.ref_frame]

                self.frame_depth_dict[frame.name] = depth

                if depth in self.depth_frame_dict:
                    self.depth_frame_dict[depth].append(frame.name)
                else:
                    self.depth_frame_dict[depth] = [frame.name]
                    self.max_depth += 1
        else:
            raise Exception("The reference frame \"{0}\" does not exist".format(frame.ref_frame))

    def solid_pose_in_frame(self, solid, frame: Frame) -> Pose:
        """
        solid_pose_in_frame takes a Solid solid and a Frame frame as parameters and return the
        pose of solid expressed in frame
        """

        frame_seqs = self.get_frame_seq(frame,
                                        self.frames[solid.ref_frame])

        pose = solid.get_pose(True)

        for frame_name in frame_seqs[0]:
            frame = self.frames[frame_name]

            pose.rotate(frame.pose.orientation)
            pose.position = frame.pose.position + \
                            frame.pose.orientation.to_rot_matrix() * pose.position

        if len(frame_seqs[1]) == 1:
            return pose

        pose_fixed = Pose(Quaternion(), array([0, 0, 0]))

        for frame_name in frame_seqs[1]:
            frame = self.frames[frame_name]

            pose_fixed.rotate(frame.pose.orientation)
            pose_fixed.position = frame.pose.position + \
                                  frame.pose.orientation.to_rot_matrix() * pose_fixed.position

        pose_fixed = pose_fixed.inverse()

        pose.rotate(pose_fixed.orientation)
        pose.position = pose_fixed.orientation.to_rot_matrix() * \
                        (pose.position + pose_fixed.position)

        return pose

    def get_frame_seq(self, from_frame: Frame, to_frame: Frame) -> List[Pose]:
        """
        get_frame_seq returns a two lists containing:
            - the forward frame sequence which goes from:

                case 1: the to_frame to the from_frame if the sequence does not include the fixed frame
                case 2: the to_frame to the fixed_frame otherwise

                [to_frame, frame_1, ..., from_frame or fixed_frame]

            - the backward frame sequence which goes from the from_frame to the fixed_frame if we are in
                case 2 for the forward sequence and only from_frame otherwise

                [from_frame, frame_1, ..., fixed_frame]

        """
        fwd_frame_seq = [to_frame.name]
        bwd_frame_seq = [from_frame.name]

        while fwd_frame_seq[-1] != self.fixed_frame.name and \
                        fwd_frame_seq[-1] != from_frame.name:
            fwd_frame_seq.append(self.frames[fwd_frame_seq[-1]].ref_frame)

        # The to_frame is not part of the frame_seq
        if self.fixed_frame != from_frame.name and \
                        fwd_frame_seq[-1] == self.fixed_frame.name:

            while bwd_frame_seq[-1] != self.fixed_frame.name:
                bwd_frame_seq.append(self.frames[bwd_frame_seq[-1]].ref_frame)

        return [fwd_frame_seq, bwd_frame_seq]

    def get_all_frame_poses(self) -> Dict[str, Pose]:
        poses = {self.fixed_frame.name: self.fixed_frame.pose}

        for depth in range(1, self.max_depth):
            for frame_name in self.depth_frame_dict[depth]:
                pose = Pose()
                frame = self.frames[frame_name]
                pose_ref_frame = poses[frame.ref_frame]

                pose.orientation = pose_ref_frame.orientation * \
                                    frame.pose.orientation
                pose.position = pose_ref_frame.position + \
                                 pose_ref_frame.orientation.to_rot_matrix() * \
                                 frame.pose.position

                poses[frame_name] = pose

        return poses