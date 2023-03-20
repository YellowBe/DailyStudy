#include "lidar_camera_projection.hpp"
// int H, W;
// int my_array[100000][3];
// void arrayCallback(const std_msgs::Int32MultiArray::ConstPtr& msg) {
//     // extract the array dimensions
//     H = msg->layout.dim[0].size;
//     W = msg->layout.dim[1].size;
//     // copy the array data into a 2D array
//     for (int i = 0; i < H; i++) {
//         for (int j = 0; j < W; j++) {
//             my_array[i][j] = msg->data[i*W+j];
//         }
//     }

// }


int main(int argc, char **argv) {
  ros::init(argc, argv, "lidar_projection");
  ROS_INFO("Start Projection");
  LidarCamProjection::LidarProjection Process;

  // ros::NodeHandle nh;
  // ros::Subscriber sub = nh.subscribe("/lidar_cam_fusion/depth_array", 100, arrayCallback);
  // // print the array to the console
  // ROS_INFO("Received array:");
  // ROS_INFO("%d ", my_array[0][0]);
  ros::spin();

  return 0;
}