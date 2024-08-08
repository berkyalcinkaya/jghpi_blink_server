import time
import sys
import argparse
from board_utils import all_off, all_on, configure_leds

def blink_pin(interval, LED1, leds, serial_conn):
    """Blink the pin on and off with the given interval."""
    all_off(leds)
    time.sleep(0.5)
    try:
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
        time.sleep(0.5)
        serial_conn.close_connection()
    except Exception as e:
        print(f"An error occurred in blink_pin: {e}")
        time.sleep(0.5)
        serial_conn.close_connection()

def blink_all_three_multiples(interval, leds, serial_conn):
    all_off(leds)
    time.sleep(0.5)
    time_lower = interval * (1 / 2)
    all_on(leds)
    time.sleep(0.5)
    try:
        while True:
            time.sleep(time_lower)
            LED1.off() 
            time.sleep(time_lower)
            LED1.on() 
            LED2.off() 
            time.sleep(time_lower)
            LED1.off() 
            time.sleep(time_lower)
            LED1.on() 
            LED2.on() 
            LED3.toggle() 
    except KeyboardInterrupt:
        print("Keyboard interrupt: turning off lights and closing serial connection")
        all_off(leds)
        time.sleep(0.5)
        serial_conn.close_connection()
    except Exception as e:
        print(f"An error occurred in blink_pin: {e}")
        time.sleep(0.5)
        serial_conn.close_connection()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED Blinking Script")
    parser.add_argument("interval", type=float, help="Blink interval in seconds")
    parser.add_argument("--baud_rate", type=int, default=115200, help="Baud rate for the serial connection (default: 115200)")
    parser.add_argument("--mode", choices=["single", "multiple"], default="single", help="Blink mode: 'single' for blink_pin or 'multiple' for blink_all_three_multiples (default: single)")

    args = parser.parse_args()

    print("interval: ", args.interval, "| baud rate:", args.baud_rate)
    LED1, LED2, LED3, leds, serial_conn = configure_leds(args.baud_rate)
    time.sleep(1)
    
    if args.mode == "single":
        blink_pin(args.interval, LED1, leds, serial_conn)
    else:
        blink_all_three_multiples(args.interval, leds, serial_conn)
