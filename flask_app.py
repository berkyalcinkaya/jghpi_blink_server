from flask import Flask, request, jsonify
import json
import threading
import time
from utils import board_is_on, triggered_remote, update_json_file, get_json_dict
from board_utils import send_command, leds, all_off, blink_all_three_multiples, get_interval_from_freq, switch_on

RUN_LIGHTS = True # keep as false to test API alone
thread = None
stop_event = threading.Event()

app = Flask(__name__)

@app.route('/blink', methods=['POST'])
def handle_blink():
    message = ""
    if board_is_on() and not triggered_remote():
        #return jsonify({'error': 'Board is on from the controller. Contact site to turn board off'}), 400
        message += "Overriding on-site settings.\n"
        stop_blinking_thread()
        all_off(leds)
    
    data = request.json
    print(data)
    rate = data.get('freq')
    try:
        rate = int(rate)
    except:
        rate = rate
    
    if rate is None or not isinstance(rate, int) or rate == 0:
        return jsonify({'error': 'Invalid input, must provide a nonzero integer rate with key name "freq"'}), 400
    
    interval = get_interval_from_freq(rate)
    intrvl_lst = [interval/2, interval, interval*2]
    update_json_file(1, intrvl_lst, True)

    if RUN_LIGHTS:
        start_blinking_thread(interval)
    
    json_dict = get_json_dict() 
    if message:
        json_dict["message"] = message
    return jsonify(json_dict), 200

def start_blinking_thread(interval):
    global thread
    thread = threading.Thread(target=blink_all_three_multiples, args=(interval,))
    thread.start()

def stop_blinking_thread():
    global thread
    stop_event.set()
    thread = None

@app.route("/off")
def turn_off():
    if board_is_on():
        update_json_file(0, [0,0,0], False)
        stop_blinking_thread()
        all_off(leds)
    
        if switch_on():
            return jsonify({"warning": "on/off switch is on. Turn off on board"}), 200
        else:
            return "Board Turned Off Successfuly", 200
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
    send_command("dio mode DO_G0 source")
    update_json_file(0, [0,0,0], False)
    app.run(host='0.0.0.0', port=5000)

    

    