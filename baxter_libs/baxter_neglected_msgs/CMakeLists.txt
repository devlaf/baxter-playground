cmake_minimum_required(VERSION 2.8.3)
project(baxter_neglected_msgs)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files(DIRECTORY msg FILES
  ChannelFloat32.msg
  Header.msg
  Point32.msg
  PointCloud.msg
)

generate_messages(DEPENDENCIES
  std_msgs
)

catkin_package(CATKIN_DEPENDS
  std_msgs
)
