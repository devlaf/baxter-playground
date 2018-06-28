import os
import sys
import argparse
import time
import pickle
import rospy
import baxter_libs.robot_utils
from baxter_libs.baxter import Baxter

_baxter = 0
_waypoints = []

def playback_waypoints(filepath):
    waypoints = read_waypoints_from_file(filepath)

    _baxter.LeftArm.set_joint_speed(0.75)
    _baxter.RightArm.set_joint_speed(0.75)

    for waypoint in waypoints:
        if waypoint[0] == 'l':
            _baxter.LeftArm.set_pose(waypoint[1])
        else:
            _baxter.RightArm.set_pose(waypoint[1])

def record_waypoints(filepath):
    _baxter.LeftArm.Gripper.DashButton.register_on_pressed_handler(cuff_pressed)
    _baxter.RightArm.Gripper.DashButton.register_on_pressed_handler(cuff_pressed)
    _baxter.LeftArm.Gripper.DotButton.register_on_pressed_handler(cuff_pressed)
    _baxter.RightArm.Gripper.DotButton.register_on_pressed_handler(cuff_pressed)

    raw_input("Press Enter to stop and save...")

    write_waypoints_to_file(filepath)

def write_waypoints_to_file(filename):
    with open(filename, 'wb') as fp:
        pickle.dump(_waypoints, fp)

def read_waypoints_from_file(filename):
    with open (filename, 'rb') as fp:
        return pickle.load(fp)

def cuff_pressed():
    left_pose = _baxter.LeftArm.get_current_pose()
    right_pose = _baxter.RightArm.get_current_pose()
    _waypoints.append(('l', left_pose))
    _waypoints.append(('r', right_pose))
    

def main():
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,description=main.__doc__)
    parser.add_argument('-o', '--operaiton', dest='operation', default="save", help='operation: save or playback')
    parser.add_argument('-f', '--filepath', dest='filepath', help='filepath of waypoint file')
    args = parser.parse_args(rospy.myargv()[1:])

    robot_utils.startup()
    
    global _baxter 
    _baxter = Baxter()

    if args.operation == "playback":
        time.sleep(7)
        playback_waypoints(args.filepath)
    else:
        record_waypoints(args.filepath)

    robot_utils.shutdown()
    return 0

if __name__ == '__main__':
    sys.exit(main())

