# create
mkdir -p ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_camera_pkg --dependencies rclpy sensor_msgs cv_bridge

cp -r my_camera_pkg src/
colcon build

# launch
ros2 run my_camera_pkg camera_publisher --ros-args -p device_path:=/dev/video0
# each time, you need to kill camera PID
./kill_camera_users.sh
