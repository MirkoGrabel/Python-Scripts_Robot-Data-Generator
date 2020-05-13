import requests
import json
import time
from azure.iot.device import IoTHubDeviceClient, Message
import random  # https://pynative.com/python-get-random-float-numbers/ Very helpful guide

# URL where the web server hosting the config file is hosted.
BAXTER_URL = "http://127.0.0.1:5000/api/v1/iotdatasimulator/"
ROBOT_CONFIG = {'robot_mode': 'half'}  # default mode in case the web server is or goes off.

MSG_TXT = '{{"current": {C}, "vibration": {V}, "temp": {T}}}'
TEMPERATURE = 40.0

# Connection string to dump it into correct IoT Hub account
#CONNECTION_STRING = "HostName=mgrabel-IoT-Hub.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=cBARs0vZhk8X1o4qo3dZMLL8bschIVXlJ7G6+LtYV+0="
CONNECTION_STRING = "HostName=IoT-Hub-Fanuc-Robot.azure-devices.net;DeviceId=RobotSimulator;SharedAccessKey=dLV9Yjqim34WdLrHEs7rWS/IAR75LBBbpQOBijV2+zI="


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

# Initialize the client globally, otherwise message sending results in error
client = iothub_client_init()


def create_random_data(argument):
    # This function creates random data based on what mode the robot is in.
    # It uses the global variable TEMPERATURE to show how the temperature is slowly increasing or decreasing.
    # Each robot mode has its own range for all parameters.
    global TEMPERATURE

    if argument['robot_mode'] == 'half':
        print('Executing HALF SPEED program')
        current = round(random.uniform(2, 3), 2)  # Creates random Current between 2 and 3
        vibration = random.randint(100, 300)
        temp_upper_t = 47
        temp_lower_t = 43
    if argument['robot_mode'] == 'full':
        print('Executing FULL SPEED program')
        current = round(random.uniform(2.5, 3.5), 2)  # Creates random Current between 2.5 and 3.5
        vibration = random.randint(100, 600)
        temp_upper_t = 58
        temp_lower_t = 54
    if argument['robot_mode'] == 'error':
        print('Executing ERROR program')
        current = round(random.uniform(3, 4), 2)  # Creates random Current between 3 and 4
        vibration = random.randint(100, 1000)
        temp_upper_t = 65
        temp_lower_t = 61
    if argument['robot_mode'] == 'off':
        print('Executing OFF program')
        current = 0.1
        vibration = 0
        temp_upper_t = 20
        temp_lower_t = 19
    if argument['robot_mode'] == 'disconnected':
        print('Executing DISCONNECTED program - no data will be sent')
        return()

    if TEMPERATURE > temp_upper_t:
        TEMPERATURE = TEMPERATURE - ((TEMPERATURE - temp_upper_t) / 100 + 0.02)
    if TEMPERATURE < temp_lower_t:
        TEMPERATURE = TEMPERATURE + ((temp_lower_t - TEMPERATURE) / 100 + 0.02)
    else:
        TEMPERATURE = TEMPERATURE + round(random.uniform(0, 0.2), 2) - 0.1
    TEMPERATURE = round(TEMPERATURE, 2)  # re-rounding as we saw funny long floats.
    msg_txt_populated = MSG_TXT.format(C=current, V=vibration, T=TEMPERATURE)
    send_data_to_azure(msg_txt_populated)
    return ()


def send_data_to_azure(fake_data):
    # Sends created fake data to Azure
    try:

        fake_data_azure_ready = Message(fake_data)
        print("Sending message: {}".format(fake_data_azure_ready))
        client.send_message(fake_data_azure_ready)
        print("Message successfully sent")
    except:
        print("Error sending message")
    return()


while True:  # loop runs permanently
    try:  # ensures loop doesn't crash is server is unreachable
        get_response = requests.get(url=BAXTER_URL)  # gets back GET response which needs filtering
        ROBOT_CONFIG = json.loads(get_response.text)  # filters text out of response and formats it in JSON
        print("\nThe current Robot configuration from Server is: " + str(ROBOT_CONFIG))
        create_random_data(ROBOT_CONFIG)
    except:
        print("\nServer couldn't be reached. Using last config: " + str(ROBOT_CONFIG))
        create_random_data(ROBOT_CONFIG)
    time.sleep(1)

