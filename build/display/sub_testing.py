from datetime import datetime
import time
import json
import paho.mqtt.client as mqtt

#TODO: timeTableRows should only contain the desired stop and not an arrival and Departure instance or both twice(for P and I trains)
#TODO: the train should also have information about destination


topic = "station/PSL/+/+/Long-distance"

formattedData = {
    "Station": "PSL",
    "trains": []
}
def remove_passed_trains():
    time_now = datetime.utcnow()
    print("AAAAAAAAAAAAAAAAAAAAAa", time_now)
    for train in formattedData["trains"]:
        scheduled_time = train["timeTableRows"][1]["scheduledTime"]
        if train["timeTableRows"][1]["liveEstimateTime"] is None:
            if time_now > datetime.fromisoformat(scheduled_time[:-1]):
                formattedData["trains"].remove(train)
                print("removed train")
        else:
            estimated_time = train["timeTableRows"][1]["liveEstimateTime"]
            if datetime.fromisoformat(estimated_time[:-1]) < time_now:
                formattedData["trains"].remove(train)
                print("removed train")

#adapter method
def get_amount(amount, trains):

    sorted_data = sorted(trains, key=lambda x: x["timeTableRows"][1]["scheduledTime"])
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
    train = json.loads(msg.payload)

    if not has_duplicate(formattedData["trains"], train):
        formattedData["trains"].append(train)
        print("Added new train to list")
    else:
        print("List already contains a duplicate train")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

client.loop_start()

while True:
    remove_passed_trains()
    formattedData["trains"] = get_amount(5, formattedData["trains"])
    print(json.dumps(formattedData))
    time.sleep(10)





