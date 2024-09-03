import time
import sys
import argparse
from board_utils import all_off, all_on, configure_leds

NUM_COMMANDS_PER_LOOP_SINGLE = 2
NUM_COMMANDS_PER_LOOP_MULTIPLE = 7
TIME_FACTOR_SINGLE = 2
TIME_FACTOR_MULTIPLE = 4

def blink_pin(interval, LED1, leds, serial_conn, command_reset):
    """Blink the pin on and off with the given interval."""
    all_off(leds)
    try:
        i = 0
        commands = 0
        while True:
            if commands and commands % command_reset == 0:
                serial_conn.clear_buffer()
            start_time = time.perf_counter()
            
            LED1.on(pwm=False)
            time.sleep(interval)
            
            LED1.off()
            time.sleep(interval)
            
            elapsed_time = time.perf_counter() - start_time
            if elapsed_time < interval * TIME_FACTOR_SINGLE:
                time.sleep(interval * TIME_FACTOR_SINGLE - elapsed_time)
            i += 1
            commands += NUM_COMMANDS_PER_LOOP_SINGLE
    except KeyboardInterrupt:
        print("Keyboard interrupt: turning off lights and closing serial connection")
        all_off(leds)
        time.sleep(0.5)
        serial_conn.close_connection()
    except Exception as e:
        print(f"An error occurred in blink_pin: {e}")
        time.sleep(0.5)
        serial_conn.close_connection()

def blink_all_three_multiples(interval, LED1, LED2, LED3, leds, serial_conn, command_reset):
    all_off(leds)
    all_on(leds)
    try:
        i = 0
        commands = 0
        while True:
            if command_reset and (commands and commands % command_reset == 0):
                serial_conn.clear_buffer()
            start_time = time.perf_counter()
            
            time.sleep(interval)
            LED1.off() 
            time.sleep(interval)
            LED1.on(pwm=False) 
            LED2.off() 
            time.sleep(interval)
            LED1.off() 
            time.sleep(interval)
            LED1.on(pwm=False) 
            LED2.on(pwm=False) 
            LED3.toggle() 

            elapsed_time = time.perf_counter() - start_time
            if elapsed_time < interval * TIME_FACTOR_MULTIPLE:
                time.sleep(interval * TIME_FACTOR_MULTIPLE - elapsed_time)
            i += 1
            commands += NUM_COMMANDS_PER_LOOP_MULTIPLE
    except KeyboardInterrupt:
        print("Keyboard interrupt: turning off lights and closing serial connection")
        all_off(leds)
        time.sleep(0.5)
        serial_conn.close_connection()
    except Exception as e:
        print(f"An error occurred in blink_all_three_multiples: {e}")
        time.sleep(0.5)
        serial_conn.close_connection()

def get_freq_fps_from_interval(interval):
    rate = 1/interval
    freq = rate/2
    return rate, freq

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED Blinking Script")
    parser.add_argument("interval", type=float, help="Blink interval in seconds")
    parser.add_argument("--baud_rate", type=int, default=115200, help="Baud rate for the serial connection (default: 115200)")
    parser.add_argument("--mode", choices=["single", "multiple"], default="single", help="Blink mode: 'single' for blink_pin or 'multiple' for blink_all_three_multiples (default: single)")
    parser.add_argument("--reset_every", type=int, default=None, help="Number of commands before buffer is reset (default: None)")

    args = parser.parse_args()
    reset_every = args.reset_every
    interval = args.interval

    rate, freq = get_freq_fps_from_interval(interval)
    
    print("freq: ", freq, "Hz (fastest light) | interval: ", interval, "| baud rate:", args.baud_rate)
    time.sleep(5)

    LED1, LED2, LED3, leds, serial_conn = configure_leds(args.baud_rate)
    time.sleep(0.05)

    if args.mode == "single":

        if reset_every:
            if reset_every % NUM_COMMANDS_PER_LOOP_SINGLE != 0:
                raise ValueError(f"reset_every must be a multiple of {NUM_COMMANDS_PER_LOOP_SINGLE} for single mode")

            iterations = reset_every / NUM_COMMANDS_PER_LOOP_SINGLE
            time_to_reset = iterations * (TIME_FACTOR_SINGLE * interval)
            print("\n---TIME TO RESET:", time_to_reset, "seconds ----------\n")
            time.sleep(5)
        blink_pin(interval, LED1, leds, serial_conn, reset_every)
    else:
        if reset_every:
            if reset_every % NUM_COMMANDS_PER_LOOP_MULTIPLE != 0:
                raise ValueError(f"reset_every must be a multiple of {NUM_COMMANDS_PER_LOOP_MULTIPLE} for multiple mode")

            iterations = reset_every / NUM_COMMANDS_PER_LOOP_MULTIPLE
            time_to_reset = iterations * (TIME_FACTOR_MULTIPLE * (interval))
            print("\n---TIME TO RESET:", time_to_reset, "seconds ----------\n")
            time.sleep(5)
        blink_all_three_multiples(interval, LED1, LED2, LED3, leds, serial_conn, reset_every)
