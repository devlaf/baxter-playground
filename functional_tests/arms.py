import os
import time
import rospy
from baxter_libs.robot_utils import *
from baxter_libs.baxter import Baxter
from baxter_libs.baxter_gripper import BaxterGripper

def test_arm_return(baxter):
    baxter = Baxter()
    
    pose = baxter.LeftArm.get_current_pose()
    print "Move the arm manually"
    
    time.sleep(3)
    baxter.LeftArm.set_pose(pose)
    
    while True:
        i = input("Enter to end")
        if not i:
            break


def test_arm_mirror(baxter):
    baxter = Baxter()
    while True:
        pose = baxter.LeftArm.get_current_pose()
        for key in pose.keys():
            pose[key.replace("left", "right")] = pose.pop(key)
            
        baxter.RightArm.set_pose(pose)
        time.sleep(0.1)

