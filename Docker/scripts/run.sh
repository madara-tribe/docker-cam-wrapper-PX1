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
  --device=/dev/video4 \
  --group-add video \
  -v /home/hagi/Downloads/ggg/workspace/:/ros2_ws \
  test:latest

# v4l2-ctl --list-devices
