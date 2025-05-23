sudo apt install udev
whoami
# hagi
# OWNER="h***"
sudo usermod -aG video hagi

### USB CAMERA
udevadm info --name=/dev/video4 --attribute-walk

### ARDUINO
udevadm info --name=/dev/ttyACM0 --attribute-walk


sudo cp config/99-arduino.rules /etc/udev/rules.d/
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
# ls -l /dev/video0 has to show "crw-rw----+ 1 ~ video ~ /dev/video0"

sudo udevadm control --reload-rules
sudo udevadm trigger

### when uninstall
sudo rm /etc/udev/rules.d/99-realsense-libusb.rules
sudo rm /etc/udev/rules.d/99-arduino.rules
sudo udevadm control --reload-rules 
sudo udevadm trigger
