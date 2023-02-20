import requests
import json
import pprint
import paho.mqtt.client as paho
import sys
import time
from datetime import datetime
import pytz

# parameter "include_nonstopping" set as true below shows passing trains also
# next 5 arriving trains at kirkkonummi station, if you want to change station replace "KKN" with other stationshortcode (KKN appears 3 times in the code)
url = "https://rata.digitraffic.fi/api/v1/live-trains/station/KKN?arrived_trains=0&arriving_trains=5&departed_trains=0&departing_trains=0&include_nonstopping=true"
stationNames = "https://rata.digitraffic.fi/api/v1/metadata/stations"
client = paho.Client()

if client.connect("localhost", 1883, 60) != 0:
    print("Error in connection")
    sys.exit(-1)

passing_train_check_time = 60


# Simple train class to store info of a train (maybe unnecessary)
class Train:
    def __init__(self, trainNumber,  track, isStopping, scheduledTime):
        self.trainNumber = trainNumber
        self.track = track
        self.isStopping = isStopping
        self.scheduledTime = scheduledTime


# Helper to see what the index of trains stops is departure from current station.
def checkIndex(data):
    i = 0
    for x in data:
        i + 1
        if x['stationShortCode'] == "KKN" and x['type'] == "DEPARTURE":
            return i


stationData = ""
stationsResponse = requests.get(stationNames)
if stationsResponse.status_code == 200:
    stationData = json.loads(stationsResponse.text)
else:
    stationData = None


def getStationName(shortCode):
    if stationData != None:
        for x in stationData:
            if x['stationShortCode'] == shortCode:
                return x['stationName']
    else:
        print("No data")
        return None


def makeRequest(topic, quality):
    response = requests.get(url)

    if response.status_code == 200:
        trainData = json.loads(response.text)

        passing_train_detected = False

        trains = []

        for x in trainData:
            stops = x['timeTableRows']
            endStation = stops[-1]
            thisStop = stops[-2]

            track = thisStop['commercialTrack']
            isStopping = thisStop['trainStopping']
            for stop in stops:
                if stop['stationShortCode'] == "KKN" and stop['type'] == "ARRIVAL":
                    scheduledTime = stop['scheduledTime']

            train = Train(x['trainNumber'], track, isStopping, scheduledTime)
            trains.append(train)

        # Check if there are any passing trains within the next minute, need to remove timezone changes here so its only for the display
        for t in trains:
            if not t.isStopping:
                scheduled_datetime = datetime.strptime(t.scheduledTime, "%Y-%m-%dT%H:%M:%S.%fZ")
                scheduled_datetime = scheduled_datetime.replace(tzinfo=pytz.utc)
                gmt2_timezone = pytz.timezone('Europe/Helsinki')
                scheduled_datetime = scheduled_datetime.astimezone(gmt2_timezone)

                current_time = datetime.now(gmt2_timezone)
                time_difference = (scheduled_datetime - current_time).total_seconds()

                if time_difference <= passing_train_check_time and time_difference > 0:
                    client.publish(topic, "Avoid the passing train!", quality)
                    passing_train_detected = True
                    time.sleep(passing_train_check_time)

        if not passing_train_detected:
            # Publish the next 5 arriving trains, sorted by scheduled time
            client.publish(topic, "Next 5 arriving trains:", quality)
            sorted_trains = sorted([t for t in trains if t.isStopping], key=lambda t: t.scheduledTime)[:5]
            for t in sorted_trains:
                scheduled_datetime = datetime.strptime(t.scheduledTime, "%Y-%m-%dT%H:%M:%S.%fZ")
                scheduled_datetime = scheduled_datetime.replace(tzinfo=pytz.utc)
                gmt2_timezone = pytz.timezone('Europe/Helsinki')
                scheduled_datetime_gmt2 = scheduled_datetime.astimezone(gmt2_timezone)
                message = f'Train number: {t.trainNumber}, Track: {t.track}, Scheduled time of arrival: {scheduled_datetime_gmt2.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
                client.publish(topic, message, quality)

    else:
        print(f"Error: {response.status_code}")


while True:
    makeRequest("topic/test", 0)
    time.sleep(30)
