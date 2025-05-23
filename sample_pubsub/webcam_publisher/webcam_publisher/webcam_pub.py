import rclpy
from rclpy.qos import qos_profile_sensor_data
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImagePublisher(Node):
    def __init__(self):
        super().__init__("webcam_pub")
        self.bridge = CvBridge()
        self.declare_parameter("device_path", "/dev/video4")
        device_path = self.get_parameter("device_path").get_parameter_value().string_value
        self.cap = cv2.VideoCapture(device_path)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.pub = self.create_publisher(Image, "/video_stream", qos_profile_sensor_data)
        # self.rgb8pub = self.create_publisher(Image, "/image/rgb", 10)
        # self.bgr8pub = self.create_publisher(Image, "/image/bgr", 10)
        # self.mono8pub = self.create_publisher(Image, "/image/mono", 10)

    def run(self):
        while True:
            try:
                r, frame = self.cap.read()
                if not r:
                    self.get_logger().warn("Failed to capture frame")
                    return
                self.pub.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))

                # # BGR8
                # self.bgr8pub.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))

                # # RGB8
                # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # self.rgb8pub.publish(self.bridge.cv2_to_imgmsg(frame_rgb, "rgb8"))

                # # MONO8
                # frame_mono = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #self.pub.publish(self.bridge.cv2_to_imgmsg(frame, "mono8"))

            except CvBridgeError as e:
                print(e)
        self.cap.release()

def main(args=None):
    rclpy.init(args=args)

    ip = ImagePublisher()
    print("Publishing...")
    ip.run()

    ip.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

