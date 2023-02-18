import json
import sys
import time

import paho.mqtt.client as paho

client = paho.Client()

if client.connect("localhost", 1883, 60) != 0:
    print("Error in connection")
    sys.exit(-1)

test_data_pasila_main_display = {
    'station': 'Pasila',
    'trains': [{'time': '17:51', 'notice': '', 'platform': '2', 'train': 'K', 'destination': 'Kerava'},
               {'time': '17:53', 'notice': '', 'platform': '7', 'train': 'IC96B', 'destination': 'Helsinki'},
               {'time': '17:53', 'notice': '', 'platform': '3', 'train': 'H', 'destination': 'Riihimäki'},
               {'time': '17:54', 'notice': '17:56', 'platform': '1', 'train': 'P', 'destination': 'Helsinki'},
               {'time': '17:54', 'notice': '', 'platform': '8', 'train': 'I', 'destination': 'Helsinki'},
               {'time': '17:58', 'notice': '', 'platform': '2', 'train': 'I', 'destination': 'Lentoasema'},
               {'time': '17:59', 'notice': '', 'platform': '8', 'train': 'A', 'destination': 'Helsinki'},
               {'time': '17:59', 'notice': '18:01', 'platform': '9', 'train': 'A', 'destination': 'Lentoasema'},
               {'time': '18:01', 'notice': '', 'platform': '1', 'train': 'K', 'destination': 'Helsinki'},
               {'time': '18:03', 'notice': '', 'platform': '9', 'train': 'P', 'destination': 'Lentoasema'}, ],
}

test_data_pasila_platform_display1 = {
    'platform': '1',
    'trains': [{'time': '17:51', 'notice': '', 'train': 'K', 'destination': 'Kerava'},
               {'time': '17:57', 'notice': '', 'train': 'K', 'destination': 'Helsinki'},
               {'time': '17:59', 'notice': '', 'train': 'I', 'destination': 'Lentoasema'},
               {'time': '18:03', 'notice': '18:06', 'train': 'K', 'destination': 'Helsinki'},
               {'time': '18:07', 'notice': '', 'train': 'I', 'destination': 'Helsinki'},
               {'time': '18:10', 'notice': '', 'train': 'I', 'destination': 'Lentoasema'}]
}

while True:
    client.publish("station/PSL/main", json.dumps(test_data_pasila_main_display), 0)
    client.publish("station/PSL/1", json.dumps(test_data_pasila_platform_display1), 0)
    print("Publishing topics...")
    time.sleep(5)
