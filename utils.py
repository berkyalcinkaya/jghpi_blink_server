'''
Berk Yalcinkaya
utils.py
6/19/24

Contains utility function update_json_file which stores current blinking status in status.json
'''

import json

JSON_PATH = 'status.json'

def get_json_obj():
    with open(JSON_PATH, 'r') as file:
        data = json.load(file)
    return data

def get_json_dict():
    with open(JSON_PATH, 'r') as file:
        data = json.load(file)
    return dict(data)

def board_is_on():
    # Check the status field
    return get_json_obj().get('status') == 1

def triggered_remote():
    return get_json_obj().get("triggered_remote")

def update_json_file(status=None, rates_hz=None, triggered_remote=False):
    data = get_json_obj()
    
    # Update the fields if new values are provided
    if status is not None:
        data['status'] = status
    if rates_hz is not None:
        if len(rates_hz) != 3:
            raise ValueError("rates_hz must be a list of 3 elements")
        data['rates_hz'] = rates_hz
    if triggered_remote is not None:
        data["triggered_remote"] = triggered_remote

    # Write the updated JSON data back to the file
    with open(JSON_PATH, 'w') as file:
        json.dump(data, file, indent=4)