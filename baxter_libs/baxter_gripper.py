import rospy
import baxter_interface
import baxter_external_devices
import robot_utils
from robot_utils import Side
from baxter_button import BaxterButton
from baxter_interface import CHECK_VERSION

class BaxterGripper(object):

    def __init__(self, side):
        robot_utils.ensure_robot_enabled()

        if side != Side.LEFT and side != Side.RIGHT:
            side = Side.LEFT

        self.DashButton = BaxterButton('%s_upper_button' %(side))
        self.DotButton =  BaxterButton('%s_lower_button' %(side))

        self._gripper = baxter_interface.Gripper(side, CHECK_VERSION)
        self._ensure_gripper_calibration()

    def get_current_position(self):
        return self._gripper.position()

    def set_position(self, position):
        if position > 100 or position < 0:
            rospy.logerror("BaxterArms.set_position(...) -- Invalid position arg; must be between 0 and 100")
            return
        
        if self._gripper.type() != 'electric':
            _capability_warning(self._gripper, 'command_position')
            return
        
        # Emprical: grippers seem to require a really high tolerance even immediatly after calibration. 
        # I've decided to use 3/100 here.
        gripper_tolerance = 3

        control_rate = rospy.Rate(100)
        while (not rospy.is_shutdown() and not (abs(self.get_current_position() - position) <= 5)):
            self._gripper.command_position(position)
            control_rate.sleep()

    def open(self):
        self.set_position(100)

    def close(self):
        self.set_position(0)

    def set_speed(self, speed):
        if speed > 100 or speed < 0:
            rospy.logerror("BaxterArms.set_speed(...) -- Invalid speed arg; must be between 0 and 100")
            return

        if self._gripper.type() != 'electric':
            _capability_warning(self._gripper, 'command_position')
            return

        self._gripper.set_velocity(speed)
    
    def set_holding_force(self, force):
        if speed > 100 or speed < 0:
            rospy.logerror("BaxterArms.set_holding_force(...) -- Invalid force arg; must be between 0 and 100")
            return
        
        if self._gripper.type() != 'electric':
            _capability_warning(self._gripper, 'command_position')
            return
        
        self._gripper.set_holding_force(speed)

    def _ensure_gripper_calibration(self):
        if not (self._gripper.calibrated() or self._gripper.calibrate() == True):
            rospy.logwarn("%s (%s) calibration failed.", self._gripper.name.capitalize(), self._gripper.type())

    def _capability_warning(self, gripper, cmd):
        msg = ("%s %s - not capable of '%s' command" %(gripper.name, self._gripper.type(), cmd))
        rospy.logwarn(msg)
