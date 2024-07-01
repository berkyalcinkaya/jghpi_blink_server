To install, run
sudo ./install.sh

Depends on spidev, ST7789, smbus, RPi GPIO
Also requires functional ADC and MCU for DIO.

Install sets up to run automatically on boot, with a second service to disable the backlight on shutdown.

If the demo-display script is not working:

Set the following in config.txt or usercfg.txt used for the OS.
dtoverlay=spi4-1cs
dtoverlay=spi3-1cs,cs0_pin=24
dtoverlay=i2c5,pins12_13=on,baudrate=40000
#dtparam=spi=on

Location of demo-display service
/usr/sbin/demo-display