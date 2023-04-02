import threading
import time
from datetime import datetime, timedelta
from utils.Event import Reactive
import json
import pytz

# Reactive objects storing information for GUI
# which update the GUI when the value changes
reactive_train_data = Reactive([])
reactive_train_data2 = Reactive([])
reactive_display_name = Reactive('')
reactive_warnings = Reactive([])
reactive_announcements = Reactive([])
reactive_passing = Reactive(False)
passing_train_time = ''

# lists to store received messages
message_list = []
message_list2 = []


topic_info_dict = {
    "station": "",
    "platform": "",
    "transit": "",
    "transport": "",
    "view": ""
}


def convertUTCtoEET(time):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    dt_utc = pytz.timezone("UTC").localize(datetime.strptime(time, date_format))
    dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
    return dt_helsinki.strftime('%H:%M')


def checkPassingTrain():
    try:
        global passing_train_time, reactive_passing
        time_now = datetime.now(pytz.timezone("Europe/Helsinki"))
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        dt_utc = pytz.timezone("UTC").localize(datetime.strptime(passing_train_time, date_format))
        dt_helsinki = dt_utc.astimezone(pytz.timezone("Europe/Helsinki"))
        difference = dt_helsinki - time_now

        # checks if passing train is one minute away from the station
        if dt_helsinki > time_now and dt_helsinki.date() == time_now.date() and (difference.seconds / 60) <= 1:
            print("Passing train incoming. Stay away from the platform")
            reactive_passing.value = True
        else:
            reactive_passing.value = False
    except ValueError:
        pass


def printPassingTrainOnDisplay(msg):
    parsed = json.loads(msg)
    if len(parsed['trains']) >= 1:
        global passing_train_time
        passing_train_time = parsed['trains'][0]['scheduledTime']
        print(passing_train_time)


def printAnnouncementsOnDisplay(msg):
    parsed = json.loads(msg)
    global reactive_announcements
    reactive_announcements.value = parsed
    # Color blue with ANSI code
    print(f"\033[34m{parsed} \033[00m")


def printWarningOnDisplay(msg):
    parsed = json.loads(msg)
    global reactive_warnings
    reactive_warnings.value = parsed
    # Color red with ANSI code
    print(f"\033[91m{parsed} \033[00m")


# function to handle received messages
# Loops through the trains to separate each train with only one timetable into new_trains list
# sorts the list by scheduled time and "next_ten_trains"
def format_train_data(trains, reactive_trains):
    # sorts the train data
    global reactive_display_name
    topic_info_dict["station"] = trains[0]['stationFullname']
    new_trains = []
    for train in trains:
        for schedule in train['schedule']:
            for train_id, train_data in schedule.items():
                for timetable in train_data:
                    for timetable_entry in timetable["timetable"]:
                        new_train = {
                            train_id: [{
                                "trainNumber": timetable["trainNumber"],
                                "trainType": timetable["trainType"],
                                "trainCategory": timetable["trainCategory"],
                                "commuterLineID": timetable["commuterLineID"],
                                "timetable": [timetable_entry]
                            }]
                        }
                        new_trains.append(new_train)

    # Picks 10 first trains which are sorted by scheduledTime
    sorted_trains = sorted(new_trains, key=lambda x: x[list(x.keys())[0]][0]['timetable'][0]['scheduledTime'])
    next_ten_trains = sorted_trains[:10]

    # final formatting for displays
    formatted_train_data = []
    for train in next_ten_trains:
        temp_train_data = []
        for train_data in train.values():
            # checks what the displayed train name should be
            if train_data[0]['trainCategory'] == "Commuter":
                temp_train_data.insert(3, train_data[0]['commuterLineID'])
            else:
                temp_train_data.insert(3, f"{train_data[0]['trainType']}{train_data[0]['trainNumber']}")
            for timetable in train_data[0]["timetable"]:
                temp_train_data.insert(4, timetable["destination"])
                temp_train_data.insert(5, timetable["stop_on_stations"])
                if timetable["liveEstimateTime"] is None:
                    temp_train_data.insert(0, convertUTCtoEET(timetable["scheduledTime"]))
                else:
                    temp_train_data.insert(0, convertUTCtoEET(timetable["liveEstimateTime"]))
                temp_train_data.insert(2, timetable['commercialTrack'])
                # Checks if train is late or cancelled
                if timetable["cancelled"] is False and timetable['differenceInMinutes'] == 0 or timetable['differenceInMinutes'] is None:
                    temp_train_data.insert(1, "")
                elif timetable["cancelled"] is True:
                    temp_train_data.insert(1, "Cancelled")
                else:
                    new_time = datetime.strptime(temp_train_data[0], '%H:%M') + timedelta(minutes=timetable['differenceInMinutes'])
                    temp_train_data.insert(1, "→ " + new_time.strftime('%H:%M'))

        formatted_train_data.append(temp_train_data)
    print(formatted_train_data)
    configureDisplayName()
    reactive_trains.value = formatted_train_data


# start a thread to handle received messages
def message_handler(stop_event):
    global message_list, message_list2

    while not stop_event.is_set():
        # wait for messages to arrive
        time.sleep(1)
        # check if any new messages have arrived in the last second
        last_message_time = time.time()
        while time.time() - last_message_time < 10 and len(message_list) == 0:
            time.sleep(1)
        # collect messages received during the last 10 seconds into a list
        if len(message_list) != 0:
            messages = message_list
            message_list = []
            try:
                format_train_data(messages, reactive_train_data)
            except Exception as e:
                print("Error formatting train data: ", e)
        if len(message_list2) != 0:
            messages = message_list2
            message_list2 = []
            try:
                format_train_data(messages, reactive_train_data2)
            except Exception as e:
                print("Error formatting train data: ", e)


stop_event = threading.Event()
thread = threading.Thread(target=message_handler, args=(stop_event,))
thread.start()


def stop_threads():
    # Stop all running threads
    global stop_event
    global thread

    stop_event.set()
    thread.join(timeout=0.1)


def addTrains(msg, dict):
    global message_list, topic_info_dict
    if dict.get("station") is not None:
        topic_info_dict["station"] = dict.get("station")
    if dict.get("platform") is not None:
        topic_info_dict["platform"] = dict.get("platform")
    if dict.get("transit") is not None:
        topic_info_dict["transit"] = dict.get("transit")
    if dict.get("transport") is not None:
        topic_info_dict["transport"] = dict.get("transport")
    if dict.get("view") is not None:
        topic_info_dict["view"] = dict.get("view")
    message_list.append(json.loads(msg))


def addTrains2(msg):
    global message_list2
    message_list2.append(json.loads(msg))


def configureDisplayName():
    global topic_info_dict, reactive_display_name
    name_dict = {
        "DEPARTURE": "departing ",
        "ARRIVAL": "arriving ",
        "Commuter": "commuter ",
        "Long-distance": "long distance ",
        "": ""
    }
    if topic_info_dict["view"] == "platformview":
        reactive_display_name.value = "Platform " + topic_info_dict["platform"]
        return
    if topic_info_dict["transit"] == "+" or topic_info_dict.get("transit") is None:
        topic_info_dict["transit"] = ""
    if topic_info_dict["transport"] == "#" or topic_info_dict.get("transport") is None:
        topic_info_dict["transport"] = ""
    if topic_info_dict["platform"] != "":
        reactive_display_name.value = "Platform " + topic_info_dict["platform"] + " " + name_dict[topic_info_dict['transit']] + name_dict[topic_info_dict['transport']] + "trains"
    else:
        reactive_display_name.value = topic_info_dict["station"] + " " + name_dict[topic_info_dict['transit']] + name_dict[topic_info_dict['transport']] + "trains"

