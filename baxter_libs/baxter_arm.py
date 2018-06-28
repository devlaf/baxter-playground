import os
import sys
import time
import rospy
import baxter_interface
import robot_utils
from baxter_interface import CHECK_VERSION
from robot_utils import Side
from baxter_gripper import BaxterGripper
#from async_node_publisher import AsyncNodePublisher
from ros_tools.async_node_publisher import AsyncNodePublisher

class BaxterArm(object):

    def __init__(self, side):
        robot_utils.ensure_robot_enabled()

        if side == Side.LEFT:
            self._arm = baxter_interface.Limb(Side.LEFT)
        else:
            self._arm = baxter_interface.Limb(Side.RIGHT)

        self._joint_names = self._arm.joint_names()
        self._publisher = AsyncNodePublisher()
        self._node_id = "baxter_arm" + side
        
        self.Gripper = BaxterGripper(side)

    def get_joint_names(self):
        return self._joint_names
    
    def get_current_position(self, joint_name):
        return self._arm.joint_angle(joint_name)

    def get_current_pose(self):
        return dict(map(lambda x: (x, self.get_current_position(x)), self.get_joint_names()))

    def set_pose(self, pose):
        self._publisher.publish_async(self._node_id, 100, self._arm.set_joint_positions(pose, True),
        self.are_all_joints_within_tolerance(pose, self.get_current_pose(), baxter_interface.JOINT_ANGLE_TOLERANCE))

    def are_all_joints_within_tolerance(self, joints_expected, joints_actual, tolerance):
        pairs = zip(joints_expected.values(), joints_actual.values())
        compliance = map(lambda x: self.is_within_tolerance(x[0], x[1], tolerance), pairs)
        return reduce(lambda y, z: y and z, compliance)
   
    def is_within_tolerance(self, expected, actual, tolerance):
        return (abs(expected - actual) <= tolerance)

    def set_joint_speed(self, speed):
        if speed > 1 or speed < 0:
            rospy.logerr("BaxterArm.set_joint_speed(...) -- Invalid args; speed must be between 0.0 and 1.0")
            return

        self._arm.set_joint_position_speed(speed)

    def get_current_cartesian_position(self):
        return self._arm.endpoint_pose()

