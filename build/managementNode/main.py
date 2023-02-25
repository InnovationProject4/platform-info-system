import json
import sys
import time
from datetime import datetime
import paho.mqtt.client as paho
import station_names as station_names
import data_manager as data_manager

client = paho.Client()
if client.connect("localhost", 1883, 60) != 0:
    print("error in connection")
    sys.exit(-1)

MAINDISPLAY_AMOUNT = 10
PLATFORMDISPLAY_AMOUNT = 5
STATION_NAMES = station_names.get_station_names()


list_of_stations = [
    {
        'station': "HKI", 'tracks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    },
    {
        'station': "PSL", 'tracks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    },
]


while True:
    for station in list_of_stations:
        stationName = station['station']
        data = data_manager.get_data(stationName, STATION_NAMES)
        traindata = data_manager.get_commercial_trains(data, MAINDISPLAY_AMOUNT)
        client.publish("station/"+stationName+"/"+"main", json.dumps(traindata), 0)
        print("Published data for :", stationName)

        for track in station['tracks']:
            trackdata = data_manager.get_track_data(data, track, PLATFORMDISPLAY_AMOUNT)
            client.publish("station/" + stationName + "/" + str(track), json.dumps(trackdata), 0)
    time.sleep(30)
        


