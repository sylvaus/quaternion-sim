from quaternion.pose import Pose
from quaternion.pose import Quaternion

class Frame(object):
    def __init__(self, name: str, pose: Pose, ref_frame: str):
        self.name = name
        self.pose = pose
        self.ref_frame = ref_frame

    def translate(self, vector):
        self.pose.translate(vector)

    def rotate(self, quat: Quaternion):
        self.rotate(quat)


class FrameManager(object):
    def __init__(self, fixed_frame: Frame):
        """
        The FrameManager is managing all the frames and allows to
        quickly express a pose in any frame.
        """
        self.frames = {fixed_frame.name: fixed_frame}
        self.fixed_frame = fixed_frame

    def add_frame(self, frame: Frame):
        if frame.ref_frame in self.frames:
            self.frames[frame.name] = frame
        else:
            raise "The reference frame {0} does not exist".format(frame.ref_frame)

    def solid_pose_in_frame(self, solid, frame: Frame) -> Pose:
        frame_seqs = self.get_frame_seq(frame, solid.frame)

    def get_frame_seq(self, from_frame: Frame, to_frame: Frame) -> list:
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

