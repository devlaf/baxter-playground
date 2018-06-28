import os
import rospy
from baxter_libs.robot_utils import *
from baxter_libs.baxter import Baxter
from baxter_libs.baxter_gripper import BaxterGripper

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
    baxter = Baxter()
    baxter.RightArm.Gripper.DashButton.register_on_pressed_handler(test_gripper_buttons_dash_pressed)
    baxter.RightArm.Gripper.DashButton.register_on_released_handler(test_gripper_buttons_dash_released)
    while True:
        i = input("Enter to end")
        if not i:
            break

def test_gripper_buttons_dash_pressed():
    print "Dash pressed"

def test_gripper_buttons_dash_released():
    print "Dash released"
