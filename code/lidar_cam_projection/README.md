# lidar_cam_projection

```shell
roslaunch lidar_cam_projection livox_cam_fusion.launch
rosrun image_transport republish compressed in:=/hd_cam_40 raw out:=/hd_cam_40
rosbag play 0908_1_2021-09-21-18-28-34.bag --clock
```

```
mkdir -p point_cloud_transport_ws/src
cd point_cloud_transport_ws/src
git clone https://github.com/paplhjak/draco.git
git clone https://github.com/paplhjak/point_cloud_transport.git
git clone https://github.com/paplhjak/draco_point_cloud_transport.git
git clone https://github.com/paplhjak/point_cloud_transport_plugins.git

cd ..

##Generate excutable file
catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release
catkin build  -DPYTHON_EXECUTABLE=/usr/bin/python3 -j9

##Generate lib for other package to use
mkdir install
catkin_make_isolated -j8 -DPYTHON_EXECUTABLE=/usr/bin/python3 --install --install-space ~/robotics/point_cloud_transport_ws/install/

##catkin clean after any failure
```
