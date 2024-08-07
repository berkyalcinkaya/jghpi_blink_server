from curses import baudrate
from board_utils import all_off, configure_leds
import time
import sys

def blink_pin(interval, LED1,leds):
    """Blink the pin on and off with the given interval."""
    try:
        all_off(leds)
        while True:
            LED1.on()
            time.sleep(interval)
            LED1.off()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Keyboard interrupt: turning off lights and closing serial connection")
        all_off(leds)
        serial_conn.close_connection()

if __name__ == "__main__":
    all_off()
    blink_interval = float(sys.argv[-2])  # Blink once a second
    baud_rate = int(sys.argv[-1])

    print("interval: ", blink_interval, "| baud rate:", baud_rate)
    LED1, LED2, LED3, leds, serial_conn = configure_leds(baud_rate)
    time.sleep(0.5)
    blink_pin(blink_interval, LED1,leds)
