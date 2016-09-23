from quaternion.pose import Pose
from solids import Solid

class Frame(object):
    def __init__(self, name: str, pose: Pose, ref_frame):
        self.name = name
        self.pose = pose
        self.ref_frame = ref_frame


    def translate(self, vector):
        self.pose.translate(vector)

    def rotate(self, quat):
        self.rotate(quat)


class FrameManager(object):
    def __init__(self, fixed_frame: Frame):
        self.frames = {fixed_frame.name:fixed_frame}
        self.fixed_frame = fixed_frame

    def add_frame(self, frame: Frame):
        if frame.ref_frame.name in self.frames:
            self.frames[frame.name] = frame

    def solid_pose_in_frame(self, solid: Solid, frame: Frame):
        cur_frame = solid.frame



