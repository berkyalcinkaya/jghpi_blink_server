'''
board_utils.py
Berk Yalcinkaya
6/19/24

Contains utility functions to control light blinking
'''
import RPi.GPIO as GPIO 
from .board import *

def get_interval_from_switches():
    if GPIO.input(SWITCH_200) == ON:
        return 1 / 200
    if GPIO.input(SWITCH_100) == ON:
        return 1/ 100
    if GPIO.input(SWITCH_50) == ON:
        return 1 / 50
    return None

def switch_on():
    return GPIO.input(SWITCH_ON) == ON

def all_on(leds):
    for led in leds:
        GPIO.output(led, ON)

def all_off(leds):
    for led in leds:
        GPIO.output(led, OFF)

def blink_all_three_multiples(interval):
    all_off(leds)
    time_lower = interval * (1 / 2)
    all_on(leds)
    while True:
        time.sleep(time_lower)
        GPIO.output(LED1, OFF)
        time.sleep(time_lower)
        GPIO.output(LED1, ON)
        GPIO.output(LED2, OFF)
        time.sleep(time_lower)
        GPIO.output(LED1, OFF)
        time.sleep(time_lower)
        GPIO.output(LED1, ON)
        GPIO.output(LED2, ON)
        GPIO.output(LED3, not GPIO.input(LED3))