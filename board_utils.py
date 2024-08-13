'''
board_utils.py
Berk Yalcinkaya
6/19/24

Contains utility functions to control light blinking
'''
import time
from comm import SerialConnection

class OutPin():
    def __init__(self, pin, serial_connection, group=0, v=True, byte_mode=True):
        self.pin_num = int(pin)
        self.group_num = group
        self.type = "DO"
        self.is_on = False
        self.ser = serial_connection
        self.byte_mode = byte_mode

        if v:
            print("initiating pin", self.pin_num, "on DO_G0")
    
    def toggle_byte_mode(self):
        self.byte_mode = not self.byte_mode

    def on(self):
        if self.byte_mode:
            command = self.construct_byte_command(action=0x01, state=1)
        else:
            command = f"dio set {self.type}_G{self.group_num} {self.pin_num} active"
        
        self.ser.send_command(command, byte_mode=self.byte_mode)
        print(command)
        self.is_on = True

    def off(self):
        if self.byte_mode:
            command = self.construct_byte_command(action=0x01, state=0)
        else:
            command = f"dio set {self.type}_G{self.group_num} {self.pin_num} inactive"
        
        self.ser.send_command(command, byte_mode=self.byte_mode)
        self.is_on = False
        print(command)

    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()

    def construct_byte_command(self, action, state):
        # Constructing the byte command header
        header = bytearray(8)
        header[0] = 0x01  # Start of frame
        header[1] = 0x00  # DIO command kind
        header[2] = 0x00  # Status (for sending command, it's zero)
        header[3] = 0x00  # Status (for sending command, it's zero)
        header[4] = 0x04  # Length of command data
        header[5] = 0x00  # Reserved
        header[6] = 0x00  # Reserved
        header[7] = 0x00  # Reserved

        # Constructing the command body
        body = bytearray(8)
        body[0] = action  # Action: Set (0x01)
        body[1] = self.group_num  # Target group/bank
        body[2] = self.pin_num  # Pin index
        body[3] = state  # State: 0 for off, 1 for on
        # Bytes 4-7 for edge count (not needed for set, so set to 0)
        body[4:8] = (0).to_bytes(4, byteorder='little')

        return header + body


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

def all_on(leds, sleep=0.005):
    for led in leds:
        led.on()
        time.sleep(sleep)


def all_off(leds, sleep=0.005):
    for led in leds:
        led.off()
        time.sleep(sleep)

def configure_leds(baud_rate):
    serial_conn = SerialConnection(baud_rate=baud_rate)
    LED1 = OutPin(0, serial_conn)
    LED2 = OutPin(1, serial_conn)
    LED3 = OutPin(2, serial_conn)
    leds = [LED1, LED2, LED3]
    return LED1, LED2, LED3, leds, serial_conn