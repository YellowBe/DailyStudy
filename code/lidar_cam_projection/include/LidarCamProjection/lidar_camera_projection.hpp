#pragma once
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <message_filters/subscriber.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <message_filters/synchronizer.h>
#include <message_filters/time_synchronizer.h>
#include <ros/ros.h>
#include <sensor_msgs/CameraInfo.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/PointCloud.h>
#include <sensor_msgs/PointCloud2.h>
#include <sensor_msgs/point_cloud_conversion.h>
#include <std_msgs/Int32MultiArray.h>
#include <tf/transform_listener.h>
#include <tf_conversions/tf_eigen.h>
#include <Eigen/Dense>
#include <opencv4/opencv2/highgui/highgui.hpp>
#include <opencv4/opencv2/opencv.hpp>
// #include "LidarCamProjection/ImageLabelDistribution.h"
#include <math.h>
#include <chrono>
#include <fstream>
#include <iostream>
#include <opencv4/opencv2/core/matx.hpp>
#include <tuple>
#include <unordered_map>
#include <omp.h>
// advanced feature: compression
// #include <point_cloud_transport/point_cloud_transport.h>

using namespace std;
using namespace Eigen;
using namespace std::chrono;

namespace LidarCamProjection
{
class LidarProjection
{
public:
  LidarProjection() : nh_("~"),  channel_names_({ { 1, "r" }, { 2, "g" }, { 2, "b" } })
  {
    // ros::NodeHandle nh("~");
    set_params();
    depth_array_pub = nh_.advertise<std_msgs::Int32MultiArray>("depth_array", 100);
    cloud_sub_.subscribe(nh_, cloud_topic_, 5);
    img_sub_.subscribe(nh_, image_topic_, 10);
    sync_2_.reset(new ApproximateSync2(ApproximateSyncPolicy2(10), cloud_sub_, img_sub_));
    sync_2_->registerCallback(boost::bind(&LidarProjection::callback, this, _1, _2));
  }

  void set_params();
  // Getting rostopics and extrinsic matrix from launch file.
  vector<int> depth_color(MatrixXf& depth);

  std::tuple<MatrixXf, MatrixXf> get_cloud_project_results(const MatrixXf& cloud_mat,
                                                                     const MatrixXf& point_cam_mat,
                                                                     const vector<double>& dist_vect,
                                                                     const vector<int>& point_index);

  bool project_points(MatrixXf& cloud_mat);
  // Getting points in camera frame.

  void convert_cloud_to_mat(const sensor_msgs::PointCloud2ConstPtr& cloud_msg);


  void callback(const sensor_msgs::PointCloud2ConstPtr& cloud_msg, const sensor_msgs::ImageConstPtr& img_msg);
  // void make_color_map();



private:
  ros::NodeHandle nh_;
  double lidar_max_range_ = 70;
  double lidar_min_range_ = 0.6;
  string cloud_topic_ = "/rslidar_velo_points";
  string image_topic_ = "/usb_cam/image_raw";
  int horizontal_offset_=40;

  std::map<int, string> channel_names_;

  sensor_msgs::PointCloud Cloud;

  Matrix4f Extrinsic;
  MatrixXf Intrinsic;
  MatrixXf raw_cloud_mat_;
  MatrixXf cloud_pixel_mat_;
  vector<int> color_info_;
  vector<int> point_index_;
  vector<double> dist_vect_;
  ros::Publisher depth_array_pub;
  cv::Mat distort_coeffs_;
  cv::Mat cam_matrix_;

  message_filters::Subscriber<sensor_msgs::PointCloud2> cloud_sub_;
  message_filters::Subscriber<sensor_msgs::Image> img_sub_;

  typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::PointCloud2, sensor_msgs::Image>
      ApproximateSyncPolicy2;
  typedef message_filters::Synchronizer<ApproximateSyncPolicy2> ApproximateSync2;
  boost::shared_ptr<ApproximateSync2> sync_2_;

  string sub_tp;
  string pub_tp;
  const float MIN_DIS = 0;
  const float MAX_DIS = 120;
  int WIDTH = 1280;
  int HEIGHT = 720;

public:
  EIGEN_MAKE_ALIGNED_OPERATOR_NEW;
  
};  // namespace LidarCamProjection

void LidarProjection::set_params()
{

  vector<double> extrinsic_param = {7.671987157338411301e-03, -9.999704625971905791e-01, -4.631913413258859080e-04, 1.522593101275518564e-02, 2.958423300492940555e-02, 6.899787237559795727e-04, -9.995620526444923826e-01, 3.840039838516234177e-02, 9.995328477696808767e-01, 7.654924070283619653e-03, 2.958865267142996025e-02, -3.900169224954055242e-02, 0.000000000000000000e+00, 0.000000000000000000e+00, 0.000000000000000000e+00, 1.000000000000000000e+00} ;
  vector<double> intrinsic_param = {503.9118983001055, 0, 671.2958449975808, 0, 501.51746060696, 360.3375255194335, 0, 0, 1};
  vector<double> distort_coeffs = {-0.01685027548055526, -0.02370727310509031, 0.0006342716911730475, -0.002358264692816827, 0};

  Extrinsic.setIdentity();
  for (int i = 0; i < extrinsic_param.size(); i++)
  {
    Extrinsic(i / 4, i % 4) = extrinsic_param[i];
  }
  std::cout << "Lidar to Cam Extrinsic calibration mat is \n" << std::endl << Extrinsic << std::endl;

  Matrix3f Intrinsic3x3;
  for (int i = 0; i < intrinsic_param.size(); i++)
  {
    Intrinsic3x3(i / 3, i % 3) = intrinsic_param[i];
  }

  Intrinsic.resize(4, 4);
  Intrinsic.setIdentity();
  Intrinsic.block(0, 0, 3, 3) = Intrinsic3x3;
  std::cout << "Cam Intrinsic K mat is \n" << std::endl << Intrinsic << std::endl;

  cam_matrix_ = (cv::Mat_<double>(3, 3) << intrinsic_param[0], intrinsic_param[1],
                             intrinsic_param[2], intrinsic_param[3], intrinsic_param[4],
                             intrinsic_param[5], intrinsic_param[6], intrinsic_param[7],
                             intrinsic_param[8]);

  distort_coeffs_ = (cv::Mat_<double>(1, 5) << distort_coeffs[0], distort_coeffs[1],
                                     distort_coeffs[2], distort_coeffs[3], distort_coeffs[4]);

  std::cout << "Cam Distortion coeffs is \n" << std::endl << distort_coeffs_ << std::endl;
}

// ----------------------------- get parameters finished ------------------------------------

void LidarProjection::convert_cloud_to_mat(const sensor_msgs::PointCloud2ConstPtr& cloud_msg)
{
  //因为点云矩阵raw_cloud_mat_在赋值之前必须设定矩阵size，所以需要先统计可用点云数
  sensor_msgs::convertPointCloud2ToPointCloud(*cloud_msg, Cloud);
  // raw_cloud_mat_.resize(3, Cloud.points.size());

  vector<int> in_range;
  int count = 0;
  //清空上一帧的点云深度信息
  dist_vect_.clear();
  // cout<<"Cloud size: "<<Cloud.points.size()<<endl;
  // 筛选在设定lidar距离内的点，记录其index，并记录选定点云数
  // //#pragma omp parallel for
  for (int i = 0; i < Cloud.points.size(); i++)
  {
    if (!std::isnan(Cloud.points[i].x) and !std::isnan(Cloud.points[i].y) and !std::isnan(Cloud.points[i].z))
    {
      //计算点的距离
      double pt_dist = sqrt(pow(Cloud.points[i].x, 2) + pow(Cloud.points[i].y, 2) + pow(Cloud.points[i].z, 2));
      // set minimum observe distance
      if (pt_dist >= lidar_min_range_ and pt_dist <= lidar_max_range_)
      {
        in_range.push_back(i);  //记录点云索引
        count += 1;             //用以统计被选点云数量
        dist_vect_.push_back(pt_dist);
      }
    }
  }

  //根据选定index的点云数量，设定点云矩阵大小
  raw_cloud_mat_.resize(3, count);
  // 点云矩阵按index vector赋值
  //#pragma omp parallel for
  for (auto i = 0; i < in_range.size(); i++)
  {
    raw_cloud_mat_(0, i) = Cloud.points[in_range[i]].x;
    raw_cloud_mat_(1, i) = Cloud.points[in_range[i]].y;
    raw_cloud_mat_(2, i) = Cloud.points[in_range[i]].z;
  }
  // cout<<"raw_cloud_mat_ size: "<<raw_cloud_mat_.size()<<endl;
}

// cloud_mat is the raw_cloud_mat
bool LidarProjection::project_points(MatrixXf& cloud_mat)
{
  // block（x,y, x-length, y-length） 从起点开始多大的矩形
  MatrixXf x = cloud_mat.block(0, 0, 1, cloud_mat.cols());
  MatrixXf y = cloud_mat.block(1, 0, 1, cloud_mat.cols());
  MatrixXf z = cloud_mat.block(2, 0, 1, cloud_mat.cols());

  // //批量计算点云至原点的距离 1xN
  // // MatrixXf dist_mat = (x.array().pow(2) + y.array().pow(2) + z.array().pow(2)).array().pow(0.5);

  vector<int> point_index;
  MatrixXf point_cam_mat;  //齐次坐标: 4 x point.cols, 4XN
  MatrixXf point_dist_mat;

  //转成齐次形式以进行乘法运算
  // Mat: 4 x cloud_mat.cols, 每个col对应一个点, 4XN
  // x..........
  // y..........
  // z..........
  // 1..........
  point_cam_mat.resize(4, cloud_mat.cols());
  point_cam_mat.block(0, 0, 3, cloud_mat.cols()) = cloud_mat;
  point_cam_mat.block(3, 0, 1, cloud_mat.cols()) = MatrixXf::Constant(1, cloud_mat.cols(), 1);
  point_cam_mat = Intrinsic * Extrinsic * point_cam_mat;
  // cout<<"cloud_mat.cols():"<<cloud_mat.cols()<<endl;
  // //#pragma omp parallel for
  for (size_t i = 0; i < cloud_mat.cols(); i++)
  {
    if (point_cam_mat(0, i) / point_cam_mat(2, i) >= horizontal_offset_ and point_cam_mat(0, i) / point_cam_mat(2, i) < WIDTH - 1 - horizontal_offset_ and
        point_cam_mat(1, i) / point_cam_mat(2, i) >= 0 and point_cam_mat(1, i) / point_cam_mat(2, i) < HEIGHT - 1)
    {
      point_index.push_back(i);  //记录位于图像中的点在point矩阵中的索引
    }
  }

  point_index_.clear();
  point_index_ = point_index;
  std::tuple<MatrixXf, MatrixXf> cloud_projection_results =
      get_cloud_project_results(cloud_mat, point_cam_mat, dist_vect_, point_index_);
  std::tie(cloud_pixel_mat_, point_dist_mat) = cloud_projection_results;
  color_info_ = depth_color(point_dist_mat);
  return true;
}

//按true rows的索引构造新的point matrix
std::tuple<MatrixXf, MatrixXf> LidarProjection::get_cloud_project_results(const MatrixXf& cloud_mat,
                                                                                    const MatrixXf& point_cam_mat,
                                                                                    const vector<double>& dist_vect,
                                                                                    const vector<int>& point_index)
{
  MatrixXf cloud_pixel_mat;
  cloud_pixel_mat.resize(2, point_index.size());

  MatrixXf point_dist_mat;
  point_dist_mat.resize(1, point_index.size());

  //#pragma omp parallel for
  for (size_t i = 0; i < point_index.size(); i++)
  {
    cloud_pixel_mat(0, i) = point_cam_mat(0, point_index[i]) / point_cam_mat(2, point_index[i]);
    cloud_pixel_mat(1, i) = point_cam_mat(1, point_index[i]) / point_cam_mat(2, point_index[i]);

    point_dist_mat(0, i) = dist_vect[point_index[i]];
  }
  return std::make_tuple(cloud_pixel_mat, point_dist_mat);  // 2xN
}

//把depth映射成颜色
vector<int> LidarProjection::depth_color(MatrixXf& depth)
{
  // cout << depth.rows() << " " << depth.cols() << endl;
  vector<int> color;
  for (int i = 0; i < depth.cols(); i++)
  {
    if (depth(0, i) < MIN_DIS)
      color.push_back(MIN_DIS);
    else if (depth(0, i) > MAX_DIS)
      color.push_back(round(MAX_DIS * MAX_DIS / 70));
    else
      color.push_back(round(depth(0, i) * MAX_DIS / 70));
  }

  return color;
}

void LidarProjection::callback(const sensor_msgs::PointCloud2ConstPtr& cloud_msg,
                               const sensor_msgs::ImageConstPtr& img_msg)
{
  if (cloud_msg->width * cloud_msg->height == 0)
  {
    ROS_WARN("Received empty cloud");
    return;
  }
  // ROS_INFO("lidar callback!");
  high_resolution_clock::time_point start_time = high_resolution_clock::now();
  ros::Time curr_t = ros::Time::now();

  convert_cloud_to_mat(cloud_msg);  //设置点云矩阵

  if (!project_points(raw_cloud_mat_))
  {
    return;
  }

  // Projection visulization
  cv::Mat raw_image = cv_bridge::toCvCopy(img_msg, "bgr8")->image;
  cv::Mat image;
  cv::undistort(raw_image, image, cam_matrix_, distort_coeffs_);
  cv::Size dsize = cv::Size(WIDTH, HEIGHT);
  cv::resize(image, image, dsize, 0, 0, cv::INTER_AREA);
  cv::cvtColor(image, image, cv::COLOR_BGR2HSV);
  // //#pragma omp parallel for
  for (size_t j = 0; j < color_info_.size(); j++)
  {
    cv::circle(image, cv::Point(round(cloud_pixel_mat_(0, j)), round(cloud_pixel_mat_(1, j))), 4,
               cv::Scalar(color_info_[j], 255, 255), -1);
  }
  cv::cvtColor(image, image, cv::COLOR_HSV2BGR);
  cv::imshow("Projection Image", image);
  cv::waitKey(1);

  // write pixel result to publish
  int H = color_info_.size();
  int W = 3;
  int pixel_result[H][W];
  for (size_t j = 0; j < color_info_.size(); j++)
  { 
    pixel_result[j][0] = round(cloud_pixel_mat_(0, j));
    pixel_result[j][1] = round(cloud_pixel_mat_(1, j));
    pixel_result[j][2] = color_info_[j];
    // cout << "cloud_pixel_mat is " << pixel_result[j][2] << endl;
  }

  std_msgs::Int32MultiArray msg;
  msg.layout.dim.push_back(std_msgs::MultiArrayDimension());
  msg.layout.dim[0].size = H;
  msg.layout.dim[0].stride = W * H;
  msg.layout.dim[0].label = "rows";
  msg.layout.dim.push_back(std_msgs::MultiArrayDimension());
  msg.layout.dim[1].size = W;
  msg.layout.dim[1].stride = W;
  msg.layout.dim[1].label = "cols";
  int size = H * W;
  msg.data.resize(size);
  // copy array data to the message
  for (int i = 0; i < H; i++) {
      for (int j = 0; j < W; j++) {
          msg.data[i * W + j] = pixel_result[i][j];
      }
  }
  depth_array_pub.publish(msg);

  high_resolution_clock::time_point end_time = high_resolution_clock::now();
  auto proc_duration = duration_cast<microseconds>(end_time - start_time).count();
  cout << "processing time: " << proc_duration / 1000.0 << " ms" << endl;
}
}