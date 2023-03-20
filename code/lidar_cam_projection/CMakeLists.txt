cmake_minimum_required(VERSION 3.0.2)
project(lidar_cam_projection)

add_compile_options(-std=c++14)
SET(CMAKE_BUILD_TYPE Release)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3 ")
SET(EIGEN_INCLUDE_DIR /usr/include/eigen3)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  eigen_conversions
  geometry_msgs
  image_geometry
  message_filters
  message_generation
  message_runtime
  nav_msgs
  pcl_conversions
  pcl_ros
  roscpp
  rospy
  sensor_msgs
  std_msgs
  tf2_ros
)

find_package(PCL REQUIRED)
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
message("PCL library path is ")
message(${PCL_INCLUDE_DIRS})
message(${PCL_LIBRARY_DIRS})

find_package(OpenCV REQUIRED)

catkin_package(
 INCLUDE_DIRS include
 CATKIN_DEPENDS message_filters rospy sensor_msgs message_runtime 
)
include_directories(
 include/LidarCamProjection
${catkin_INCLUDE_DIRS}
${PCL_INCLUDE_DIRS}
${EIGEN_INCLUDE_DIR}

)

add_executable(lidar_projection_node src/lidar_projection_node.cpp)
add_dependencies(lidar_projection_node ${catkin_EXPORTED_TARGETS})
target_link_libraries(lidar_projection_node
  ${catkin_LIBRARIES}
  ${OpenCV_LIBS}
)
