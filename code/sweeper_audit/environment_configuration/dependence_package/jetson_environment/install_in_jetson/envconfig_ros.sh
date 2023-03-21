#! /bin/bash
# Install Robot Operating System (ROS) on NVIDIA Jetson AGX Xavier
# Maintainer of ARM builds for ROS is http://answers.ros.org/users/1034/ahendrix/
# Information from:
# http://wiki.ros.org/melodic/Installation/UbuntuARM

ROS_PKG=ros-base
ROS_DISTRO=noetic
ROS_ROOT=/opt/ros/$ROS_DISTRO
ROS_PYTHON_VERSION=3

# #install python & pip
# sudo apt install --no-install-recommends -y \
#     python3.8 \
#     python3.8-distutils \
#     python3.8-dev \
#     python3.8-venv \
#     python3-pip 

# # build new soft link
# sudo rm -rf /usr/bin/pip3
# sudo rm -rf /usr/bin/python3
# sudo ln -s /usr/local/bin/python3.8 /usr/bin/python3
# sudo ln -s /usr/local/bin/pip3.8 /usr/bin/pip3

#==============================install ros neotic=============
echo "Adding repository"
sudo apt install \
        git \
		cmake \
		build-essential \
		curl \
		wget \
		gnupg2 \
		lsb-release \
		ca-certificates \
		ffmpeg \
echo "Setup source list"
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
echo "Setup keys"
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# install bootstrap dependencies
echo "Updating apt"
sudo apt update

echo "Installing ROS"
sudo apt install ros-$ROS_DISTRO-$ROS_PKG

echo "Installing dependencies and rosdep"
sudo apt install python3-rosdep \
     python3-rosinstall \
     python3-rosinstall-generator \
     python3-wstool

echo "Initializaing rosdep"
sudo rosdep init
rosdep update


ros_env_setup="/opt/ros/$ROS_DISTRO/setup.bash"
echo "sourcing   $ros_env_setup"
# bash -c "source "$ros_env_setup""
# echo "ROS_ROOT   $ROS_ROOT"
# echo "ROS_DISTRO $ROS_DISTRO"

# add ros into env
grep -q -F 'source $ros_env_setup' ~/.bashrc || echo "source $ros_env_setup" >> ~/.bashrc
source ~/.bashrc
