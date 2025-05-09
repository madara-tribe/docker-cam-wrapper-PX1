# Use camera in docker from outside of docker through ros2

This repository is launch camera by ros2 node.
You can have own customized way of using camera for example publish image, plot or save image.

# Architecture





## How to use
### Setup
1. setup udev to recognize camera path
```
$ udevadm info --name=/dev/video0 --attribute-walk
$ sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
# ls -l /dev/video0 has to show "crw-rw----+ 1 ~ video ~ /dev/video0"
$ sudo udevadm control --reload-rules && sudo udevadm trigger
```

2. enter inside Docker by connecting with outside camera
$ cd Docker and ./run.sh

Setup ros2 package using this codes after enter the docker.


### Launch camera 
run this command with camera path speified.
```
$ ros2 run my_camera_pkg camera_publisher --ros-args -p device_path:=<camera path>
```

