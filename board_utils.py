'''
board_utils.py
Berk Yalcinkaya
6/19/24

Contains utility functions to control light blinking
'''
from comm import SerialConnection
    
class OutPin():
    def __init__(self, pin, serial_connection, group = 0, v = True):
        self.pin_num = int(pin)
        self.group_num = group
        self.type = "DO"
        self.is_on = False
        self.ser = serial_connection

        if v:
            print("initiating pin", self.pin_num, "on DO_G0")
    
    def on(self):
        command = f"dio set {self.type}_G{self.group_num} {self.pin_num} active"

        self.ser.send_command(command)
        print(command)
        self.is_on = True
    
    def off(self):
        command = f"dio set {self.type}_G{self.group_num} {self.pin_num} inactive"
        self.ser.send_command(command)
        self.is_on = False
        print(command)
    
    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()

def get_interval_from_freq(freq):
    return 1/freq

def get_freq_from_switches():
    intrvl = get_interval_from_freq()
    if intrvl:
        return 1/intrvl
    return None

def get_interval_from_switches():
    # if GPIO.input(SWITCH_200) == ON:
    #     return 1 / 200
    # if GPIO.input(SWITCH_100) == ON:
    #     return 1/ 100
    # if GPIO.input(SWITCH_50) == ON:
    #     return 1 / 50
    return None

def switch_on():
    #return GPIO.input(SWITCH_ON) == ON
    return False

def all_on(leds):
    for led in leds:
        led.on()

def all_off(leds):
    for led in leds:
        led.off()

def configure_leds(baud_rate):
    serial_conn = SerialConnection(baud_rate=baud_rate)
    LED1 = OutPin(0, serial_conn)
    LED2 = OutPin(1, serial_conn)
    LED3 = OutPin(2, serial_conn)
    leds = [LED1, LED2, LED3]
    return LED1, LED2, LED3, leds, serial_conn