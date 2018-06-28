from robot_utils import Side
from baxter_arm import BaxterArm
from baxter_head import BaxterHead

class Baxter(object):

    def __init__(self):
        self.LeftArm = BaxterArm(Side.LEFT)
        self.RightArm = BaxterArm(Side.RIGHT)
        self.Head = BaxterHead()
