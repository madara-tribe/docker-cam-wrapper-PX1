import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import subprocess
import os

do_publish = None

def free_camera_device(device_path: str):
    try:
        # Get PIDs using the camera device
        result = subprocess.run(
            ["fuser", device_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        pids = result.stdout.strip().split()
        if not pids:
            print(f"[INFO] {device_path} is free.")
            return

        print(f"[INFO] {device_path} is used by: {' '.join(pids)}")
        for pid in pids:
            print(f"[INFO] Killing PID {pid}...")
            subprocess.run(["sudo", "kill", "-9", pid], check=False)
    except Exception as e:
        print(f"[WARN] Could not free {device_path}: {e}")

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.declare_parameter('device_path', '/dev/video4')
        device_path = self.get_parameter('device_path').get_parameter_value().string_value

        # Free the device before trying to open it
        free_camera_device(device_path)

        self.cap = cv2.VideoCapture(device_path)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

        if not self.cap.isOpened():
            self.get_logger().error(f"Failed to open camera at {device_path}")
            self.valid = False
            return
        else:
            self.valid = True

        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
        self.timer = self.create_timer(1/30.0, self.timer_callback)
        self.bridge = CvBridge()
        self.get_logger().info(f"Camera opened at {device_path}")

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warn("Failed to capture frame")
            return

        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        if do_publish:
            self.publisher_.publish(msg)
        else:
            cv2.imwrite('/ros2_ws/forgit/sample.png', frame)
            self.get_logger().info(f"Published frame: {frame.shape}")

    def destroy_node(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
            self.get_logger().info("Camera released.")
        super().destroy_node()

def main():
    rclpy.init()
    node = CameraPublisher()
    if not getattr(node, 'valid', True):
        node.destroy_node()
        rclpy.shutdown()
        return

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

