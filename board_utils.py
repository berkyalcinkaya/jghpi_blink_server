'''
board_utils.py
Berk Yalcinkaya
6/19/24

Contains utility functions to control light blinking
'''
import time
from comm import SerialConnection

def configure_leds(baud_rate):
    serial_conn = SerialConnection(baud_rate=baud_rate)
    LED1 = OutPin(0, serial_conn)
    LED2 = OutPin(1, serial_conn)
    LED3 = OutPin(2, serial_conn)

    SWITCH_ON = InPin(0, serial_conn)
    SWITCH_50 = InPin(1, serial_conn)
    SWITCH_100 = InPin(2, serial_conn)
    SWITCH_200 = InPin(3, serial_conn)

    leds = [LED1, LED2, LED3]
    return LED1, LED2, LED3, SWITCH_ON, SWITCH_50, SWITCH_100, SWITCH_200, leds, serial_conn

class InPin():
    def __init__(self, pin, serial_connection, group=0, v=False):
        self.pin_num = int(pin)
        self.group_num = group
        self.type = "DI"
        self.ser = serial_connection
        self.v = v
        if v:
            print("initiating pin", self.pin_num, "on DI_G0")
    
    def is_on(self):
        command = f"dio get {self.type}_G{self.group_num} input {self.pin_num}"
        response = self.ser.send_command(command, read=True)
        response_int = int(response.split("\n")[-2])
        if response_int == 1:
            return True
        return False

class OutPin():
    def __init__(self, pin, serial_connection, group=0, v=True, byte_mode=False):
        self.pin_num = int(pin)
        self.group_num = group
        self.type = "DO"
        self.is_on = False
        self.ser = serial_connection
        if v:
            print("initiating pin", self.pin_num, "on DO_G0")
        self.byte_mode = byte_mode

    def on(self, pwm=True, period=1000, duty=50):
        if pwm:
            command = f"dio pwm DO_G{self.group_num} {self.pin_num} {period} {duty}"
        else:
            command = f"dio set {self.type}_G{self.group_num} {self.pin_num} active"
        
        self.ser.send_command(command, byte_mode=self.byte_mode)
        print(command)
        self.is_on = True

    def off(self):
        command = f"dio set {self.type}_G{self.group_num} {self.pin_num} inactive"
        
        self.ser.send_command(command, byte_mode=self.byte_mode)
        self.is_on = False
        print(command)

    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()

def get_interval_from_rate(rate):
    return (1/rate)

def get_rate_from_switches():
    if SWITCH_50.is_on():
        return 50
    if SWITCH_100.is_on():
        return 100
    if SWITCH_200.is_on():
        return 200
    return None

def switch_on():
    return SWITCH_ON.is_on()

def all_on(leds, sleep=0.005):
    for led in leds:
        led.on()
        if sleep:
            time.sleep(sleep)

def all_on_pwm(leds, periods, sleep=0.005):
    for led, period in zip(leds, periods):
        led.on(pwm=True, period=period, duty=50)
        if sleep:
            time.sleep(sleep)

def all_off(leds, sleep=0.005):
    for led in leds:
        led.off()
        if sleep:
            time.sleep(sleep)

LED1, LED2, LED3, SWITCH_ON, SWITCH_50, SWITCH_100, SWITCH_200, leds, serial_conn = configure_leds(115200)