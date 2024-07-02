'''
board_pins.py
6/19/24
Berk Yalcinkaya

Stores hardcoded pin input and output values as well as other neccessary constants
Configures Pins as input and outputs. Imported from board.py
'''

import RPi.GPIO as GPIO  # sudo apt-get install python3-rpi.gpio

# Setting up GPIO pins
SWITCH_200 = 3
SWITCH_100 = 4
SWITCH_50 = 5
SWITCH_ON = 2

# Constants
ON = 1
OFF = 0

# Setting up GPIO pins
LED1 = 6
LED2 = 7
LED3 = 8


# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_200, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SWITCH_100, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SWITCH_50, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SWITCH_ON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)

# convenience list
leds = [LED1, LED2, LED3]