import os
import sys
import time
import rospy
import robot_utils
from robot_utils import Side
from baxter import Baxter
from baxter_gripper import BaxterGripper

def test_head_utils():
    baxter = Baxter()
    baxter.Head.set_face_image('/home/ruser/devin_crap/img/nick_cage.jpg')
    baxter.Head.set_head_orientation(1.5, 1.0)
    baxter.Head.nod_head()
    baxter.Head.set_head_orientation(-1.5, 1.0)
    baxter.Head.nod_head()
    baxter.Head.set_head_orientation_neutral()

def test_grippers():
    baxter = Baxter()

    right_gripper = baxter.RightArm.Gripper
    right_gripper.close()
    print right_gripper.get_current_position()
    right_gripper.open()
    print right_gripper.get_current_position()
    right_gripper.close()
    print right_gripper.get_current_position()
    
    left_gripper = baxter.LeftArm.Gripper
    left_gripper.close()
    print left_gripper.get_current_position()
    left_gripper.open()
    print left_gripper.get_current_position()
    left_gripper.close()
    print left_gripper.get_current_position()

def test_gripper_buttons():
    while True:
        baxter = Baxter()
        baxter.RightArm.Gripper.DashButton.register_on_pressed_handler(test_gripper_buttons_dash_pressed)
        baxter.RightArm.Gripper.DashButton.register_on_released_handler(test_gripper_buttons_dash_released)

def test_gripper_buttons_dash_pressed():
    print "Dash pressed"

def test_gripper_buttons_dash_released():
    print "Dash released"

def test_arm():
    baxter = Baxter()
    
    #blah = baxter.LeftArm.get_current_position("left_w0")
    #print "Test get left_w0 position: " + str(blah)

    #carte = baxter.LeftArm.get_current_cartesian_position()
    #print "Test cartesian: " + str(carte)

    #test_arm_return(baxter)
    #test_arm_mirror(baxter)
    test_arm_speed(baxter)

def test_arm_speed(baxter):
    baxter.LeftArm.set_joint_speed(1)
    baxter.RightArm.set_joint_speed(1)
    time.sleep(2)
    print "pick first"
    pose1 = baxter.LeftArm.get_current_pose()
    time.sleep(2)
    print "pick second"
    pose2 = baxter.LeftArm.get_current_pose()
    time.sleep(2)
    print "go"
    baxter.LeftArm.set_pose(pose1)
    baxter.LeftArm.set_pose(pose2)

def test_arm_return(baxter):
    pose = baxter.LeftArm.get_current_pose()
    time.sleep(2)
    baxter.LeftArm.set_pose(pose)

def test_arm_mirror(baxter):
    while True:
        pose = baxter.LeftArm.get_current_pose()
        for key in pose.keys():
            pose[key.replace("left", "right")] = pose.pop(key)
            
        baxter.RightArm.set_pose(pose)
        time.sleep(0.1)

def main():
    robot_utils.startup()
    
    #test_head_utils()
    #test_grippers()
    test_arm()
    #test_gripper_buttons()
    
    robot_utils.shutdown()
    return 0

if __name__ == '__main__':
    sys.exit(main())

