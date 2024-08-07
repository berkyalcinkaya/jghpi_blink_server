from curses import baudrate
from board_utils import all_off, configure_leds
import time
import sys

def blink_pin(interval, LED1, leds, serial_conn):
    """Blink the pin on and off with the given interval."""
    try:
        all_off(leds)
        time.sleep(1)
        while True:
            start_time = time.perf_counter()
            
            LED1.on()
            time.sleep(interval)
            
            LED1.off()
            time.sleep(interval)
            
            elapsed_time = time.perf_counter() - start_time
            if elapsed_time < interval * 2:
                time.sleep(interval * 2 - elapsed_time)
    except KeyboardInterrupt:
        print("Keyboard interrupt: turning off lights and closing serial connection")
        all_off(leds)
        serial_conn.close_connection()
    except Exception as e:
        print(f"An error occurred in blink_pin: {e}")
        serial_conn.close_connection()

if __name__ == "__main__":
    blink_interval = float(sys.argv[-2])  # Blink once a second
    baud_rate = int(sys.argv[-1])

    print("interval: ", blink_interval, "| baud rate:", baud_rate)
    LED1, LED2, LED3, leds, serial_conn = configure_leds(baud_rate)
    time.sleep(1)
    blink_pin(blink_interval, LED1,leds, serial_conn)
