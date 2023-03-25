from datetime import datetime
import time
import json
import paho.mqtt.client as mqtt

#TODO: timeTableRows should only contain the desired stop and not an arrival and Departure instance or both twice(for P and I trains)
#TODO: the train should also have information about destination


topic = "station/PSL/+/DEPARTURE/#"




formattedData = {
    "Station": "PSL",
    "trains": []
}
def remove_passed_trains():
    time_now = datetime.utcnow()
    print("AAAAAAAAAAAAAAAAAAAAAa", time_now)
    for train in formattedData["trains"]:
        scheduled_time = train["timetable"][0]["scheduledTime"]
        if train["timetable"][1]["liveEstimateTime"] is None:
            if time_now > datetime.fromisoformat(scheduled_time[:-1]):
                formattedData["trains"].remove(train)
                print("removed train")
        else:
            estimated_time = train["timetable"][0]["liveEstimateTime"]
            if datetime.fromisoformat(estimated_time[:-1]) < time_now:
                formattedData["trains"].remove(train)
                print("removed train")

#adapter method
def get_amount(amount, trains):

    sorted_data = sorted(trains, key=lambda x: x["timetable"][0]["scheduledTime"])
    return sorted_data[:amount]

#adapter method



def has_duplicate(lst, new_dict):
    for d in lst:
        if d == new_dict:
            return True
    return False



def on_connect(client, userdata, flags, rc):
    print("connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("UUSI JUNAVIESTI ")
    print(msg.topic)
    trains = json.loads(msg.payload)
    print(trains)
    #formattedData["trains"] = trains



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

client.loop_start()

while True:

    #formattedData["trains"] = get_amount(10, formattedData["trains"])
    #formattedData = get_amount(10, formattedData["trains"])
    #print(json.dumps(formattedData))
    print("10sec")
    time.sleep(10)





