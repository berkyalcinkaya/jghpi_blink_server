from flask import Flask, request, jsonify
import json
import threading
import time
from utils import board_is_on, triggered_remote, update_json_file, get_json_dict
from board_utils import (all_off, get_interval_from_rate, switch_on, all_on, all_on_pwm, configure_leds, 
                         LED1, LED2, LED3, LED4, leds, serial_conn)

MIN_RATE = 50
BAUD_RATE = 115200
PWM_SLEEP = 0.005
RUN_LIGHTS = True # keep as false to test API alone
thread = None
stop_event = threading.Event()

def blink_all_three_multiples(periods):
    all_off(leds + [LED4])
    all_on_pwm(leds, periods, sleep=PWM_SLEEP)
    while not stop_event.is_set():
        continue
    all_off(leds)

app = Flask(__name__)

@app.route('/blink', methods=['POST'])
def test_fps():
    message = ""
    if board_is_on() and not triggered_remote():
        #return jsonify({'error': 'Board is on from the controller. Contact site to turn board off'}), 400
        message += "Overriding on-site settings.\n"
        stop_blinking_thread()
        all_off(leds)
    
    data = request.json
    rate = data.get('rate')
    try:
        rate = float(rate)
    except:
        rate = rate
    
    if rate is None or not isinstance(rate, float) or rate == 0:
        LED4.on(pwm=False)
        time.sleep(0.001)
        return jsonify({'error': 'Invalid input, must provide a nonzero integer rate with key name "freq"'}), 400
    
    if rate < MIN_RATE:
        LED4.on(pwm=False)
        time.sleep(0.001)
        return jsonify({"Error":'You gotta be quicker than that, buddy.'}), 400
    
    LED4.off()
    
    # pin 0 is top: fastest
    # pin 1 is middle: target  freq
    # pin 2 is bottom: slowest

    freq = rate/2
    freqs = [freq*2, freq, freq/2]
    
    interval = get_interval_from_rate(rate)
    intrvl_lst = [interval/2, interval, interval*2] # smallest interval first, highest freq
    
    period_lst = [i*2 for i in intrvl_lst]
    period_micro_lst = [int(seconds * 1000000) for seconds in period_lst]

    update_json_file(1, freqs, True)
    message+=f"Testing Frame Rate: {str(rate)} fps | Blink Frequencies (Hz) Top to Bottom: {','.join([str(freq) for freq in freqs])} | Blink Periods (s): {','.join([str(i) for i in period_lst])} | Blink Periods (us): {','.join([str(i) for i in period_micro_lst])}"

    if RUN_LIGHTS:
        start_blinking_thread(period_micro_lst)
    
    json_dict = get_json_dict() 
    if message:
        json_dict["message"] = message
    return jsonify(json_dict), 200

def start_blinking_thread(period_lst):
    global thread, stop_event
    stop_event.clear() 
    thread = threading.Thread(target=blink_all_three_multiples, args=(period_lst,))
    thread.start()

def stop_blinking_thread():
    global thread, stop_event
    stop_event.set()
    if thread is not None:
        thread.join()
        thread = None
        
@app.route("/off")
def turn_off():
    LED4.off()
    if board_is_on():
        update_json_file(0, [0,0,0], False)
        stop_blinking_thread()
        all_off(leds)
        
        if switch_on():
            return jsonify({"warning": "on/off switch is on. Turn off on board"}), 200
        else:
            return "Board Turned Off Successfully", 200
    else:
        return "Board Already Off", 200

@app.route("/debug")
def debug():
    try:
        with open('status.json', 'r') as file:
            status_data = json.load(file)
        return jsonify(status_data), 200
    except FileNotFoundError:
        return jsonify({"error": "status.json file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from status.json"}), 500

if __name__ == '__main__':
    all_off(leds)
    update_json_file(0, [0,0,0], False)
    app.run(host='0.0.0.0', port=5000)

    

    