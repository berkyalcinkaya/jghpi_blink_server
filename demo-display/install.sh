#!/bin/bash

sudo cp -r images /opt/demo-images
sudo cp demo-display /usr/sbin/
sudo cp fr202-i2c /usr/sbin/
sudo cp *.service /etc/systemd/system/

sudo chmod +x /usr/sbin/demo-display
sudo chmod +x /usr/sbin/fr202-i2c

sudo apt update
sudo apt install -y python3-rpi.gpio python3-pip python3-pil python3-numpy python3-smbus python3-serial fonts-liberation
sudo apt install -y python3-spidev
sudo pip install spidev
sudo pip install st7789

sudo systemctl enable demo-display
sudo systemctl start demo-display
sudo systemctl enable disable-backlight
#sudo systemctl start disable-backlight

