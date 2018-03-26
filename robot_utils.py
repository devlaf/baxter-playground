import rospy
import baxter_interface
from baxter_interface import CHECK_VERSION

class Side:
    LEFT = "left"
    RIGHT = "right"

def startup():
    rospy.init_node('silly_baxter', anonymous=True)
    ensure_robot_enabled()

def shutdown():
    shutdown_robot()

def ensure_robot_enabled():
    
    rs = baxter_interface.RobotEnable(CHECK_VERSION)

    if not rs.state().enabled:
        rospy.loginfo("ensure_robot_enabled -- Enabling robot")
        print("Enabling robot... ")
        rs.enable()

def shutdown_robot():
    rospy.loginfo("shutdown_robot -- Disabling robot")

    # maybe we should call the tuck script here?
    
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    if rs.state().enabled:
        rs.disable()

