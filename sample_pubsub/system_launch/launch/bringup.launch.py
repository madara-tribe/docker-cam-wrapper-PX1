from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Camera publisher node
        Node(
            package='webcam_publisher',
            executable='webcam_pub',
            name='webcam_pub_node',
            output='screen',
            parameters=[{'device_path': '/dev/video4'}]
        ),

        # Camera subscriber node
        Node(
            package='webcam_sub_cpp',
            executable='webcam_sub_cpp',
            name='webcam_sub_cpp_node',
            output='screen'
        )
    ])

