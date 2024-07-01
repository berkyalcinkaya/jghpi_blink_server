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
from .board_pins import *
from .board_utils import switch_on, blink_all_three_multiples, get_interval_from_switches, all_off
from .utils import update_json_file

# Event to stop threads
stop_event = threading.Event()

def blink_led(led, on_time, off_time):
    while not stop_event.is_set():
        GPIO.output(led, ON)
        time.sleep(on_time)
        GPIO.output(led, OFF)
        time.sleep(off_time)
    GPIO.output(led, OFF)  # Ensure the LED is off when stopping

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

while True:
    thread = None
    thread_on = False
    if switch_on():
        interval = get_interval_from_switches()
        if interval:
            thread = threading.Thread(target=blink_led, args=(interval))
            thread.start()
            update_json_file(1, [interval/2, interval, interval*2])
            thread_on = True
    else:
        if thread_on:
            stop_blinking()
            thread = None
            update_json_file(0, [0,0,0])
        all_off()
