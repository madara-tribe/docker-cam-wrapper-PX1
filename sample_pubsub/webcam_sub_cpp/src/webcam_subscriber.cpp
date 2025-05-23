#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>
#include <chrono>
#include <iomanip>
#include <sstream>

class ImageSubscriber : public rclcpp::Node
{
public:
  ImageSubscriber()
  : Node("webcam_sub_cpp")
  {
    sub_ = this->create_subscription<sensor_msgs::msg::Image>(
      "/video_stream", rclcpp::SensorDataQoS(),
      std::bind(&ImageSubscriber::imageCallback, this, std::placeholders::_1));
  }

private:
  void imageCallback(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    try {
      cv::Mat frame = cv_bridge::toCvCopy(msg, "bgr8")->image;

      auto now = std::chrono::system_clock::now();
      std::time_t now_c = std::chrono::system_clock::to_time_t(now);
      std::stringstream filename;
      filename << "/ros2_ws/px4/images/image_"
               << std::put_time(std::localtime(&now_c), "%Y%m%d_%H%M%S") << ".jpg";

      cv::imwrite(filename.str(), frame);
    } catch (const cv_bridge::Exception & e) {
      RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
    }
  }

  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_;
  std::string save_dir_;
};
 
int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ImageSubscriber>());
  rclcpp::shutdown();
  return 0;
}

