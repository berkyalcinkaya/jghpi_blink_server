''''
board.py
Berk Yalcinkaya
6/19/24

One of two scripts that the Rasberry Pi will always run. Detects changes in the on/off switch and calls
API to start blinking based on upper three switches to determine fps to test
'''
import RPi.GPIO as GPIO  # sudo apt-get install python3-rpi.gpio
import threading
import time
from board_pins import *
from board_utils import get_freq_from_switches, switch_on, blink_all_three_multiples, get_interval_from_switches, all_off
from utils import board_is_on, triggered_remote, update_json_file
import requests

BASE_URL = "http://10.2.64.153:5000"

# Event to stop threads
stop_event = threading.Event()

def turn_on_blink_via_api(freq):
    url = f"{BASE_URL}/blink"
    data = {
        "key1": "value1",
        "key2": "value2"}
    response = requests.post(url, json=data)

def turn_off_blink_via_api():
    url = f"{BASE_URL}/off"
    response = requests.get(url)

def blink_led(led, on_time, off_time):
    while not stop_event.is_set():
        led.on()
        time.sleep(on_time)
        led.off()
        time.sleep(off_time)
    led.off()  # Ensure the LED is off when stopping

def blink(n1, n2, n3):
    thread1 = threading.Thread(target=blink_led, args=(LED1, n1, n1))
    thread2 = threading.Thread(target=blink_led, args=(LED2, n2, n2))
    thread3 = threading.Thread(target=blink_led, args=(LED3, n3, n3))
    
    thread1.start()
    thread2.start()
    thread3.start()
    
    return thread1, thread2, thread3

def stop_blinking():
    stop_event.set()

last_switch_state = False
switch_state_on = switch_on()
while True:
    last_switch_state = switch_state_on
    switch_state_on = switch_on()
    switch_toggled = last_switch_state != switch_state_on
    if switch_toggled:
        print(switch_toggled)
        if switch_on() and not board_is_on():
            print("board on")
            freq = get_freq_from_switches()
            if freq:
                turn_on_blink_via_api(freq)
        elif (not switch_on()) and board_is_on():
            print("board off")
            turn_off_blink_via_api()
