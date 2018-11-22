# baxter-playground
Some code to operate a rethink baxter.  Compiling some notes for myself/friends below for reference.

![baxter, starring nick cage](https://gist.githubusercontent.com/devlaf/a7e7ec6738907150b3c364d20200ea5c/raw/b65eaccdeac02f9ca365d990eab9ead5a5aeec7c/baxter.jpg)

### Login
You can SSH directly into the baxter.  Find the ip/hostname via the [Field Service Menu](http://sdk.rethinkrobotics.com/wiki/Field_Service_Menu_(FSM))

**Username:** ruser

**Password:** rethink

**^^ username/password are a rethink thing.**  All development is expected to be done via the ruser account, which has been granted permissions for the two or three services related to starting/enabling the robot. See [here](http://sdk.rethinkrobotics.com/wiki/SSH)

Note: It's probably not worth trying to set up indigo in your dev environment.  I've found old versions of ROS to be a pain in the neck to setup, as package maintenence tends to fall apart really quickly once it's more than two versions old. It's much less hassle to ssh into the system and do your dev work there.

### Setup
Currently all my work and workspace live under ~/devin_stuff/

**Bash Setup**
```
source /opt/ros/indigo/setup.bash
source ~/devin_stuff/ros_ws/baxter.sh
```

### Rethink Tools
There are several useful tools at ~/devin_stuff/ros_ws/src/baxter_tools/scripts that are provided by rethink

- enable/disable robot: `rosrun baxter_tools enable_robot.py`
- tuck/untuck arms for shipping: `rosrun baxter_tools tuck_arms.py`
- also calibration stuff, etc.


### Todo
- Expand on the head sonar-array stuff to do simple human detection
- Update arm class with completion callbacks
- Work out the knobs/buttons on the arms
- Make the gripper camera stuff useful
