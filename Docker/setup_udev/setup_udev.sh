sudo apt install udev
udevadm info --name=/dev/video0 --attribute-walk
#   # SUBSYSTEMS=="video4linux"
    # ATTRS{idProduct}=="b805"
    # ATTRS{idVendor}=="04f2"
    
#SUBSYSTEM=="video4linux" – matches video devices like /dev/video0.
#ATTR{name} – matches the device's descriptive name (Integrated Camera: Integrated C).
#ATTRS{idVendor}=="04f2" and ATTRS{idProduct}=="b805" – ensures you're targeting your specific USB camera.
#MODE="0666" – sets read/write permissions for all users.
#GROUP="video" – assigns the device to the video group (standard for video hardware).

whoami
# hagi
# OWNER="hagi"

sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
# ls -l /dev/video0 has to show "crw-rw----+ 1 hagi video ~ /dev/video0"
sudo udevadm control --reload-rules && sudo udevadm trigger


### when uninstall
sudo rm /etc/udev/rules.d/99-realsense-libusb.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
