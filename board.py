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

BASE_URL = "http://10.2.65.58:5000"

# Event to stop threads
stop_event = threading.Event()

def turn_on_blink_via_api(rate):
    url = f"{BASE_URL}/blink"
    data = {"rate": int(rate)}
    response = requests.post(url, json=data)
    print(response)

def turn_off_blink_via_api():
    url = f"{BASE_URL}/off"
    response = requests.get(url)
    print(response)

last_switch_state = False
switch_state_on = switch_on()
while True:
    last_switch_state = switch_state_on
    switch_state_on = switch_on()
    switch_toggled = last_switch_state != switch_state_on
    if switch_toggled:
        print("switch has been toggled")
        if switch_on() and not board_is_on():
            print("getting rate from switches")
            rate = get_rate_from_switches()
            print("got rate ", rate, "from switches")
            if rate:
                print("turning on via api")
                turn_on_blink_via_api(rate)
        elif (not switch_on()) and board_is_on():
            print("turning off board via API")
            turn_off_blink_via_api()
    time.sleep(1)
