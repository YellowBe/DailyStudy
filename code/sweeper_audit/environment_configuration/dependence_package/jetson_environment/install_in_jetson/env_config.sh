#!/bin/bash
echo "Install ROS"
./envconfig_ros.sh 

echo "Install python dependence"
python3 -m pip install -r requirements.txt

echo "Install Pytorch"
./envconfig_pytorch.sh

echo "Install ROS packages"
./envconfig_camsdk.sh


