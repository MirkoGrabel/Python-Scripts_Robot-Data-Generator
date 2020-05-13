import requests
import json
import time
import random

# URL where the web server hosting the config file is hosted.
BAXTER_URL = "http://127.0.0.1:5000/api/v1/iotdatasimulator/"
SIMULATOR_CONFIG = {'robot_auto_state_change': 'on', 'robot_mode': 'half'}
AUTO_STATE_CHANGE_STATE = {'robot_auto_state_change': 'on'}
ALLOWED_ROBOT_MODES = ['half', 'full', 'error', 'off']

def change_state():
    global ALLOWED_ROBOT_MODES
    new_mode = str(random.choice(ALLOWED_ROBOT_MODES))
    # While loop ensures the new mode is not the old mode = enforces state change
    while SIMULATOR_CONFIG['robot_mode'] == new_mode:
        new_mode = str(random.choice(ALLOWED_ROBOT_MODES))
    new_state = 'robot_mode=' + new_mode
    print('Trying to change state from: "' + str(SIMULATOR_CONFIG['robot_mode']) + '" to: "' + str(new_mode) + '"')
    try:
        posting_response = requests.post(url=BAXTER_URL, params=new_state)
        print('Response from Server: ' + posting_response.text)
    except:
        print('Error posting to server')
    return()


while True:  # loop runs permanently and sleeps for x seconds.
    REACHABLE = True  # required to separate try requests.get from try change_state.
    try:  # ensures loop doesn't crash if server is unreachable
        r = requests.get(url=BAXTER_URL)  # gets back GET response which needs filtering
        SIMULATOR_CONFIG = json.loads(r.text)  # filters text out of response and formats it in JSON
        print("\nThe current Robot configuration from Server is: " + str(SIMULATOR_CONFIG))
        AUTO_STATE_CHANGE_STATE.update(robot_auto_state_change=SIMULATOR_CONFIG['robot_auto_state_change'])

    except:  # If server is unreachable, print last known config.
        print("\nServer couldn't be reached, not trying to change state. Last known config: " + str(SIMULATOR_CONFIG))
        REACHABLE = False

    # the IF statements go through all possible states: reachable + change on, reachable + change off, unreachable.
    if REACHABLE:
        if AUTO_STATE_CHANGE_STATE['robot_auto_state_change'] == 'on':
            change_state()
        else:
            print('Auto State Change DISABLED, retrying soon.')
    else:
        print('Server unreachable, retrying soon.')
    # Ensures the state change happens at random between 5 minutes and 15 minutes
    SLEEP = random.randint(300, 900)
    print('Retrying to change state in ' + str(SLEEP) + ' Seconds')
    time.sleep(SLEEP)

