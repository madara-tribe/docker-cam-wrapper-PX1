# bin/bash
ARDUINO_DEV="/dev/video4"

# Check if Arduino device exists
if [ ! -e "$ARDUINO_DEV" ]; then
  echo "Error: $ARDUINO_DEV not found on host."
  exit 1
fi

docker run -it --rm \
  --net=host \
  --privileged \
  --device=$ARDUINO_DEV \
  --group-add video \
  -v <mount_path>:/ros2_ws \
  <image name>:latest

# v4l2-ctl --list-devices
