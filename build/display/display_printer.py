import threading
import time
from datetime import datetime
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

# list to store received messages
message_list = []
message_list2 = []


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
    # reactive_display_name.value = trains[0]['stationFullname']
    # print(trains)
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

    sorted_trains = sorted(new_trains, key=lambda x: x[list(x.keys())[0]][0]['timetable'][0]['scheduledTime'])
    next_ten_trains = sorted_trains[:10]

    # final formatting for displays
    formatted = []
    for train in next_ten_trains:
        temp = []
        for train_data in train.values():
            # checks what the displayed train name should be
            if train_data[0]['trainCategory'] == "Commuter":
                temp.insert(3, train_data[0]['commuterLineID'])
            else:
                temp.insert(3, f"{train_data[0]['trainType']}{train_data[0]['trainNumber']}")

            for timetable in train_data[0]["timetable"]:
                temp.insert(4, timetable["destination"])
                if timetable["liveEstimateTime"] is None:
                    temp.insert(0, convertUTCtoEET(timetable["scheduledTime"]))
                else:
                    temp.insert(0, convertUTCtoEET(timetable["liveEstimateTime"]))
                temp.insert(2, timetable['commercialTrack'])
                # Checks the notice of train: Late
                if timetable["cancelled"] is False and timetable['differenceInMinutes'] == 0 or timetable['differenceInMinutes'] is None:
                    temp.insert(1, "")
                elif timetable["cancelled"] is True:
                    temp.insert(1, "Cancelled")
                else:
                    temp.insert(1, "~ " + str(abs(timetable['differenceInMinutes'])) + "min")

        formatted.append(temp)
    print(formatted)
    reactive_trains.value = formatted


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


def addTrains(msg, display_name):
    global message_list, reactive_display_name
    message_list.append(json.loads(msg))
    reactive_display_name.value = display_name


def addTrains2(msg):
    global message_list2
    message_list2.append(json.loads(msg))
