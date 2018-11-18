import os
import sys
import rospy
import cv2
import cv_bridge
import baxter_interface
import robot_utils
from baxter_sonar_array import SonarArray

from sensor_msgs.msg import (
    Image,
)

class BaxterHead(object):

    def __init__(self):
        robot_utils.ensure_robot_enabled()
        self._head = baxter_interface.Head()
        self.SonarArray = SonarArray()

    """
    Send an image to baxters' face
      - Max screen resolution is 1024x600.
      - Images are always aligned to the top-left corner.
      - Formats: jpg or png
    """
    def set_face_image(self, path):
        rospy.logdebug("set_face_image -- sending custom image to head")
        
        if not os.access(path, os.R_OK):
            rospy.logerr("set_face_image -- Cannot read file at '%s'", path)
            return

        img = cv2.imread(path)
        msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
        pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
        pub.publish(msg)
        rospy.sleep(1)

    """
    Do a single, verticle nod of the head.
      - This is the only possible behavior for the head in the verticle direction
    """
    def nod_head(self):
        self._head.command_nod()

    """
    Set the head to a "looking forward" orientation
    """
    def set_head_orientation_neutral(self):
        self._head.set_pan(0.0)

    """
    Set the orientation of the head in the horizontal direction
      - angle_radians should be between 1.5 and -1.5
      - speed should be betwen 0.0 and 1.0
    """
    def set_head_orientation(self, angle_radians, speed):
        if speed > 1.0 or speed < 0:
            rospy.logerr("set_head_orientation -- Invalid speed specified; must be between 0.0 and 1.0")
            return

        if angle_radians > 1.5 or angle_radians < -1.5:
            rospy.logerr("set_head_orientation -- Invalid angle specified; must be between -1.5 and 1.5 radians")
            return

        control_rate = rospy.Rate(100)
        while (not rospy.is_shutdown() and not (abs(self._head.pan() - angle_radians) <= baxter_interface.HEAD_PAN_ANGLE_TOLERANCE)):
            self._head.set_pan(angle_radians, speed=speed, timeout=0)
            control_rate.sleep()
