import json
import sys
import time
from datetime import datetime
import paho.mqtt.client as paho
import station_names as station_names
import data_manager as data_manager
import passing_train

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

def publish_station_data(station, data):
    topic = "station/"+station+"/"+"main"
    train_data = data_manager.get_commercial_trains(data, MAINDISPLAY_AMOUNT)
    formatted_data = {
        "station": station,
        "trains": train_data
    }
    client.publish(topic, json.dumps(formatted_data), 0
    )

def publish_platform_data(station, track, data):
    topic = "station/" +station + "/" + str(track)
    track_data = data_manager.get_track_data(data, track, PLATFORMDISPLAY_AMOUNT)

    formatted_data = {
        "platform": track,
        "trains": track_data
    }
    client.publish(topic, json.dumps(formatted_data), 0)


def publish_passing_train_data(station, track):
    topic = "station/" + station + "/" + str(track) + "/passing"
    passing_train_data = passing_train.get_passing_train(station)

    if passing_train_data:
        formatted_data = {
            "station": station,
            "trains": passing_train_data
        }
        client.publish(topic, json.dumps(formatted_data), 0)


while True:
    for station in list_of_stations:
        station_name = station['station']
        data = data_manager.get_data(station_name, STATION_NAMES)
        publish_station_data(station_name, data)

        for track in station['tracks']:
            t = str(track)
            publish_platform_data(station_name, t, data)
            publish_passing_train_data(station_name, track)

        print("Published data for :", station)

    time.sleep(30)
