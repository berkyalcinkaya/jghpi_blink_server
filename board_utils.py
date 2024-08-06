'''
board_utils.py
Berk Yalcinkaya
6/19/24

Contains utility functions to control light blinking
'''
import time
import serial

def send_command(command, device="/dev/ttyACM0", read=False, read_wait=0.5):
    print(command)
    try:
        with serial.Serial(device, 115200, timeout=1) as ser:
            # Send the command
            ser.write((command + '\n').encode())
            if read:
                time.sleep(read_wait)  # Wait for the device to process the command
                response = ser.read_all().decode()
                return response
            else:
                return None
            
    except Exception as e:
        print(e)
        return f"An error occurred: {e}"
    
class OutPin():
    def __init__(self, pin, group = 0):
        self.pin_num = int(pin)
        self.group_num = group
        self.type = "DO"
        self.is_on = False
        print("initiating pin", self.pin_num, "on DO_G0")
    
    def on(self):
        command = f"dio set {self.type}_G{self.group_num} {self.pin_num} active"
        send_command(command)
        print(command)
        self.is_on = True
    
    def off(self):
        command = f"dio set {self.type}_G{self.group_num} {self.pin_num} inactive"
        send_command(command)
        self.is_on = False
        print(command)
    
    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()

LED1 = OutPin(0)
LED2 = OutPin(1)
LED3 = OutPin(2)
leds = [LED1, LED2, LED3]

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

