#!/bin/bash
source /home/yifeng/.bashrc
source /opt/ros/noetic/setup.bash
roscore &
rqt_image_view &
rosrun image_transport republish compressed in:=/camera/image_color raw out:=/camera/image_color &
rosbag play -l /home/yifeng/demo3.bag &
#rosrun nmea_navsat_driver nmea_serial_driver _port:=/dev/ttyACM0 _baud:=9600 &
# roslaunch hikrobot_camera hikrobot_camera.launch &
echo "detect cleanness and save to datafile"
sleep 5
cd /home/yifeng/sweeper_audit
python3 main.py 
# rqt_image_view

# echo "open gps piont"
# sudo chmod 777 /dev/ttyACM0; rosrun nmea_navsat_driver nmea_serial_driver _port:=/dev/ttyACM0 _baud:=9600 

