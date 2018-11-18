import os
import sys
import time
import rospy
from baxter_libs.robot_utils import *
from baxter_libs.baxter import Baxter
from baxter_libs.baxter_gripper import BaxterGripper

def test_head_utils():
    baxter = Baxter()
    test_head_image(baxter)
    test_head_orientation(baxter)

def test_head_image(baxter):
    baxter.Head.set_face_image('functional_tests/img/sad_robot_4.jpg')

def test_head_orientation(baxter):
    baxter.Head.set_head_orientation(1.5, 1.0)
    baxter.Head.nod_head()
    baxter.Head.set_head_orientation(-1.5, 1.0)
    baxter.Head.nod_head()
    baxter.Head.set_head_orientation_neutral()


