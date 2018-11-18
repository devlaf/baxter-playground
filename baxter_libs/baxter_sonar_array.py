import os
import sys
import rospy
import cv2
import cv_bridge
import baxter_interface
import robot_utils
from collections import defaultdict

from baxter_neglected_msgs.msg import (
    PointCloud,
)

class SonarArray(object):
    def __init__(self):
        robot_utils.ensure_robot_enabled()
        self._head = baxter_interface.Head()
        self._sonar_state = defaultdict(list)
        self.listen_for_sonar_info()

    def enable_sonar_array(self, enable):
        rospy.logdebug("enable_sonar_array -- %s the head-mounted sonar array", "enabling" if enable else "disabling")
        
        msg = 0 if enable else 4095
        pub = rospy.Publisher('/robot/sonar/head_sonar/set_sonars_enabled', PointCloud, latch=True, queue_size=1)
        pub.publish(msg)
        rospy.sleep(1)
   
    def listen_for_sonar_info(self):
        rospy.Subscriber('/robot/sonar/head_sonar/state', PointCloud, self.on_sonar_info)
        rospy.spin()

    def on_sonar_info(self, data):
        readings = self.decode_point_cloud_msg(data)
    
        for pos in range(0, len(readings)):
            rospy.loginfo(readings[pos]);
            #self._sonar_state = 
            

        #self.listen_for_sonar_info()

    def decode_point_cloud_msg(self, data):
        keys = list(filter(lambda x: x.name == "SensorId", data.channels))[0].values
        values = list(filter(lambda x: x.name == "Distance", data.channels))[0].values
        return list(zip(keys, values))
        


'''
PointCloud msg:

---
header: 
  seq: 2050
  stamp: 
    secs: 1541885950
    nsecs: 876019297
    frame_id: base
    points: 
    - 
      x: -0.000968988519162
      y: 1.08999955654
      z: 0.816999971867
    - 
      x: 0.638904750347
      y: 1.10914409161
      z: 0.816999971867
    - 
      x: 1.22290360928
      y: 2.12297129631
      z: 0.816999971867
    channels: 
    - 
      name: SensorId
      values: [9.0, 10.0, 10.0]
    -                                                                - 
      name: Distance
      values: [1.090000033378601, 1.2799999713897705, 2.450000047683716]
---
'''
