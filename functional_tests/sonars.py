import os
import time
import rospy
from baxter_libs.robot_utils import *
from baxter_libs.baxter import Baxter
from baxter_libs.baxter_sonar_array import SonarArray

def test_sonars():
    baxter = Baxter()
    
    sonars = baxter.Head.SonarArray

    sonars.enable_sonar_array(False)
    sleep(3)
    sonars.enable_sonar_array(True)
    
    #sonars.listen_for_sonar_info()

    while True:
        i = input("Enter to end")
        if not i:
            break

