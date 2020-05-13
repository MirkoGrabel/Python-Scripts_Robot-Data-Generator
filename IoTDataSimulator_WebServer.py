import flask
from flask import request, jsonify
import json

app = flask.Flask(__name__)
SIMULATOR_CONFIG = {'robot_mode': 'half', 'robot_auto_state_change': 'on'}
ALLOWED_ROBOT_MODES = ['half', 'full', 'error', 'off', 'disconnected']
ALLOWED_AUTO_STATE_CHANGE_STATE = ['on', 'off']


@app.route('/api/v1/iotdatasimulator/', methods=['POST', 'GET'])
def api_robot_config():
    global SIMULATOR_CONFIG

    if request.method == "POST":
        global ALLOWED_ROBOT_MODES
        global ALLOWED_AUTO_STATE_CHANGE_STATE
        if request.args.get('robot_mode') in ALLOWED_ROBOT_MODES:
            SIMULATOR_CONFIG.update(robot_mode=request.args.get('robot_mode'))
            print('New Configuration: ' + str(SIMULATOR_CONFIG))
            return jsonify(SIMULATOR_CONFIG)
        elif request.args.get('robot_auto_state_change') in ALLOWED_AUTO_STATE_CHANGE_STATE:
            SIMULATOR_CONFIG.update(robot_auto_state_change=request.args.get('robot_auto_state_change'))
            print('New Configuration: ' + str(SIMULATOR_CONFIG))
            return jsonify(SIMULATOR_CONFIG)
        else:
            return jsonify('Invalid args: ' + json.dumps(request.args) + '   Invalid body: ' + json.dumps(request.form))

    if request.method == "GET":
        return jsonify(SIMULATOR_CONFIG)


app.run(host="0.0.0.0")

