#!/bin/bash
# echo "open camera point"
# source /home/ntujetson/.bashrc
source /opt/ros/noetic/setup.bash 
source ~/catkin_ws/devel/setup.bash 
export PATH=/usr/local/cuda-11.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH
export MVCAM_SDK_PATH=/opt/MVS
export MVCAM_COMMON_RUNENV=/opt/MVS/lib
export LD_LIBRARY_PATH=/opt/MVS/lib/aarch64:$LD_LIBRARY_PATH
LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:/usr/lib/llvm-8/lib:/home/ntujetson/catkin_ws/devel/lib:/opt/ros/noetic/lib:/opt/MVS/lib/aarch64:/usr/local/cuda-11.4/lib64
cd /home/ntujetson/sweeper_audit
sudo chmod 777 /dev/ttyACM0; rosrun nmea_navsat_driver nmea_serial_driver _port:=/dev/ttyACM0 _baud:=9600 
roslaunch hikrobot_camera hikrobot_camera.launch &
python3 main.py
# rqt_image_view

# echo "open gps piont"

