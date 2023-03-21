#! /bin/bash
# Install hicrobot camera SDK and ros driver
echo "Install hicrobot camera SDK MVS"
sudo apt install -y apt-utils

sudo tar xzvf ./MVS-2.1.1_aarch64_20220511.tar.gz
cd ./MVS-2.1.1_aarch64_20220511
sudo ./setup.sh

echo "Install ROS REQUIRED COMPONENTS packages"
sudo apt install ros-noetic-cv-bridge ros-noetic-image-common
sudo apt install ros-noetic-rqt ros-noetic-rqt-graph ros-noetic-rqt-common-plugins
sudo apt install ros-noetic-image-transport-plugins
sudo apt install ros-noetic-nmea-navsat-driver
echo "Install python dependences"
python3 -m pip install -r requirements.txt

echo "Install GPS driver"
sudo apt install ros-noetic-nmea-navsat-driver libgps-dev 

echo "Install hicrobot camera ROS driver and our program"
mkdir ~/catkin_ws
sudo cp -R ./hikrobot_camera ~/catkin_ws/src
sudo chmod -R 777 ~/catkin_ws
cd ~/catkin_ws
catkin_make

# add hic_ws into env
echo "source ~/catkin_ws/devel/setup.bash " >> ~/.bashrc
