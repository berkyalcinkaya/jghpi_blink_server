''''
board.py
Berk Yalcinkaya
6/19/24

One of two scripts that the Rasberry Pi will always run. Detects changes in the on/off switch and calls
API to start blinking based on upper three switches to determine fps to test
'''
import threading
import time
from board_utils import LED1, LED2, LED3, get_rate_from_switches, switch_on
from utils import board_is_on
import requests

BASE_URL = "http://10.2.44.165:5000"

# Event to stop threads
stop_event = threading.Event()

def turn_on_blink_via_api(rate):
    url = f"{BASE_URL}/blink"
    data = {"rate": int(rate)}
    response = requests.post(url, json=data)
    print(response.text)

def turn_on_blue_via_api():
    url = f"{BASE_URL}/blink"
    data = {"blue": 0}
    response = requests.post(url, json=data)
    print(response.text)

def turn_off_blink_via_api():
    url = f"{BASE_URL}/off"
    response = requests.get(url)
    print(response.text)

last_switch_state = False
switch_state_on = switch_on()
while True:
    last_switch_state = switch_state_on
    switch_state_on = switch_on()
    switch_toggled = last_switch_state != switch_state_on
    if switch_toggled:
        if switch_on() and not board_is_on():
            rate = get_rate_from_switches()
            if rate:
                turn_on_blink_via_api(rate)
            else:
                turn_on_blue_via_api()
        elif (not switch_on()): #and board_is_on():
            turn_off_blink_via_api()

